import os
import pkg_resources
from zope.component import getGlobalSiteManager
from pyramid.config import Configurator
from collective.generic.webbuilder import utils

dn = 'collective.generic.webbuilder'
here = pkg_resources.resource_filename(dn, '/')

def main(global_config, **local_config):
    """
    A paste.httpfactory to wrap a pyramid WSGI based application.
    """
    wconf = global_config.copy()
    wconf.update(**local_config)
    if global_config.get('debug', 'False').lower() == 'true':
        wconf['pyramid.debug_authorization'] = 'true'
        wconf['pyramid.debug_notfound'] = 'true'
        wconf['pyramid.reload_templates'] = 'true'
        wconf['debugtoolbar.eval_exc'] = 'true'
        wconf['debugtoolbar.enabled'] = 'true'
    wconf['zcmls'] = utils.splitstrip(wconf['zcmls'])
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
    config.include('pyramid_debugtoolbar')
    config.include('pyramid_chameleon')
    config.include('pyramid_zcml')
    config.add_static_view(name='resources', path=here + '/templates/static')
    config.add_translation_dirs('collective.generic.webbuilder:locale')
    config.hook_zca()
    for z in wconf['zcmls']:
        config.load_zcml(z)
    return config.make_wsgi_app()
