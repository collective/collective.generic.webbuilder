import sys
import os

import pkg_resources
from zope.component import getGlobalSiteManager

from paste.script.serve import ServeCommand
from paste.deploy.loadwsgi import loadobj, _Server

from webob import Request, exc

from pyramid.config import Configurator

from collective.generic.webbuilder import utils


def wsgi_app_factory(global_config, **local_config):
    """
    A paste.httpfactory to wrap a django WSGI based application.
    """
    dn = 'collective.generic.webbuilder'
    wconf = global_config.copy()
    wconf.update(**local_config)
    debug = False
    if global_config.get('debug', 'False').lower() == 'true':
        debug = True
        wconf['pyramid.debug_authorization'] = 'true'
        wconf['pyramid.debug_notfound'] = 'true'
        wconf['pyramid.reload_templates'] = 'true'
    wconf['zcmls' ] = utils.splitstrip(wconf['zcmls'])
    if not wconf['zcmls']:
        wconf['zcmls'] = []
    wconf['zcmls'].insert(0, 'configure.zcml')
    for i, zcml in enumerate(wconf['zcmls']):
        if os.path.sep in zcml:
            zcml = os.path.abspath(zcml)
        else:
            zcml = pkg_resources.resource_filename(dn, zcml)
        wconf['zcmls'][i] = zcml 

    globalreg = getGlobalSiteManager() 
    config = Configurator(registry=globalreg)
    config.setup_registry(settings=wconf)
    config.include('pyramid_zcml')
    config.hook_zca()
    for z in wconf['zcmls']:
        config.load_zcml(z)  
    app = config.make_wsgi_app()
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

