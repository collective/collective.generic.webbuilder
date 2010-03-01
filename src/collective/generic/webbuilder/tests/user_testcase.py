import unittest

from repoze.bfg import testing, includes
from collective.generic import webbuilder
from globals import _callFUT

from collective.generic.webbuilder.tests.utils import _LAUNCHED_SERVERS

import pkg_resources

CGWG_ZCMLS = ['configure.zcml', 
              'plone3.zcml', 
              'plone4.zcml',
             ]

def collective_generic_webbuilder_setUp(self):
    """ cleanUp() is required to clear out the application registry
    between tests (done in setUp for good measure too)
    """
    testing.cleanUp()
    testing.registerRoutesMapper()
    context = None 
    for zcml in CGWG_ZCMLS:
        context = _callFUT(zcml, webbuilder)

def collective_generic_webbuilder_tearDown(self):
    """ cleanUp() is required to clear out the application registry
    between tests
    """
    for s in _LAUNCHED_SERVERS:
        s.tearDown()
    testing.cleanUp()

