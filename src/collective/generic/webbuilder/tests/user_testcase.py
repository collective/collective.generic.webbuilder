from pyramid import testing
from collective.generic import webbuilder
from globals import _callFUT

from collective.generic.webbuilder.tests.utils import _LAUNCHED_SERVERS

CGWG_ZCMLS = ['configure.zcml', 
              'plone3.zcml', 
              'plone4.zcml',
             ]

def collective_generic_webbuilder_setUp(self):
    """ cleanUp() is required to clear out the application registry
    between tests (done in setUp for good measure too)
    """
    testing.cleanUp()
    config = testing.setUp()
    config.include('pyramid_zcml')
    #testing.registerRoutesMapper()
    context = None 
    for zcml in CGWG_ZCMLS:
        config.load_zcml('collective.generic.webbuilder:%s'%zcml)

def collective_generic_webbuilder_tearDown(self):
    """ cleanUp() is required to clear out the application registry
    between tests
    """
    for s in _LAUNCHED_SERVERS:
        s.tearDown()
    testing.cleanUp()

