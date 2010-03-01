import sys
import os
import threading
from StringIO import StringIO

import pkg_resources

from paste.script.serve import ServeCommand
from paste.deploy.loadwsgi import loadobj, _Server

from webob import Request, exc

import zope.component
from zope.component import getGlobalSiteManager
from zope.component import getSiteManager
from zope.configuration.xmlconfig import xmlconfig

from repoze.bfg.router import make_app
from repoze.bfg.threadlocal import get_current_registry

from collective.generic.webbuilder.models import get_root
from collective.generic.webbuilder import utils
import collective.generic.webbuilder

_loaded_zcmls = {}
def load_zcml(app, zcml, force=False, lock=threading.Lock()):
    if force or (not zcml in _loaded_zcmls):
        fd = open(zcml)
        lock.acquire()
        app.threadlocal_manager.push(
            {'registry': app.registry,
             'request': None}
        )
        try:
            getSiteManager.sethook(get_current_registry)
            zope.component.getGlobalSiteManager = get_current_registry
            xmlconfig(fd)
            fd.close()
            _loaded_zcmls[zcml] = zcml
        finally:
            # intentional: do not call getSiteManager.reset(); executing
            # this function means we're taking over getSiteManager for the
            # lifetime of this process
            zope.component.getGlobalSiteManager = getGlobalSiteManager
            lock.release()
            app.threadlocal_manager.pop()

def load_zcmls(app, zcmls, force=False, lock=threading.Lock()):
    for zcml in zcmls:
        load_zcml(app, zcml, force, lock)

def wsgi_app_factory(global_config, **local_config):
    """
    A paste.httpfactory to wrap a django WSGI based application.
    """
    wconf = global_config.copy()
    wconf.update(**local_config)
    debug = False
    if global_config.get('debug', 'False').lower() == 'true':
        debug = True
        wconf['debug_authorization'] = 'true'
        wconf['debug_notfound'] = 'true'
        wconf['reload_templates'] = 'true'
    wconf['zcmls' ] = utils.splitstrip(wconf['zcmls'])
    if wconf['zcmls']:
        for i, zcml in enumerate(wconf['zcmls']):
            if os.path.sep in zcml:
                zcml = os.path.abspath(zcml)
            else:
                zcml = pkg_resources.resource_filename(
                    'collective.generic.webbuilder',
                    zcml
                )
            wconf['zcmls'][i] = zcml
    app = make_app(None, collective.generic.webbuilder, options=wconf)
    # load extra zcmls if any
    if wconf['zcmls']:
        load_zcmls(app, wconf['zcmls'])
    def webbuilder_app(environ, start_response):
        req = Request(environ)
        try:
            resp = req.get_response(app)
            return resp(environ, start_response)
        except Exception, e:
            if not debug:
                return exc.HTTPServerError(str(e))(environ, start_response)
            else:
                raise
    return webbuilder_app

class WBServeCommand(ServeCommand):
    def __init__(self, *args, **kwargs):

        ServeCommand.__init__(self, *args, **kwargs)
        self.parser.add_option('--host',
                               dest='host',
                               metavar='HOST',
                               help="host server address")
        self.parser.add_option('--port',
                               dest='port',
                               default=8080,
                               metavar='PORT',
                               help="Http server port")
        self.parser.add_option('--generation-path',
                               dest='generation_path',
                               default=os.path.join(os.getcwd(), 'generated_projects'),
                               metavar='GENERATIONPATH',
                               help="where to generate projects")

        self.parser.add_option('--debug',
                               dest='debug',
                               action="store_true",
                               metavar='DEBUG',
                               help="Run cgwb in debug mode")

    def parse_args(self, *a, **k):
        ServeCommand.parse_args(self, *a, **k)
        if self.options.debug:
            self.args.append('debug=true')
        self.args.append('generation_path=%s'%self.options.generation_path)



    def loadserver(self, server_spec, name, relative_to, **kw):
         class _HServer(_Server):
             def invoke(klass, context):
                 context.local_conf['port'] = self.options.port
                 context.local_conf['host'] = self.options.host
                 return _Server.invoke(klass, context)
         HSERVER = _HServer()
         return loadobj(HSERVER, 'config:%s'%self.args[0], name=name, **kw)

def main():
    """"""
    config = os.path.join(os.path.dirname(__file__), 'cgwb.ini')
    argv = []
    if len(sys.argv)>1:
        argv = sys.argv[1:]
    argv = argv + [config]
    cmd = WBServeCommand('foo')
    cmd.run(argv)

