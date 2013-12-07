"""
Launching all doctests in a specific directory
with globals and setup enhancement
"""
from pyramid import testing
import unittest
import doctest
import os.path
from collective.generic.webbuilder.tests import utils

CGWG_ZCMLS = ['configure.zcml', 'plone.zcml']


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UTILITIES AND GLOBBALS SUPPORT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_globs():
    import os
    import re
    from copy import deepcopy
    from pprint import pprint
    from zope.configuration import xmlconfig
    from StringIO import StringIO
    import pkg_resources
    import zope
    from zope.interface.verify import verifyObject
    from zope import interface, schema
    from zope.component import adapts, getMultiAdapter, getAdapter, getAdapters
    from collective.generic.webbuilder import interfaces
    from collective.generic.webbuilder.models import root
    from collective.generic.webbuilder import paster as gpaster
    from collective.generic.webbuilder.tests.utils import launch_server
    from zope.testbrowser.browser import Browser
    from lxml.html import fromstring as htmlS
    cwd = os.path.dirname(__file__)
    zcmlContext = None

    def _callFUT(name, package=None, context=None):
        if not context:
            context = zcmlContext
        result = xmlconfig.file(
            context=context,
            name=name,
            package=package
        )
        return result

    globs = globals()
    globs.update(locals())
    return globs


# ~~~~~~~~~~~~~~~
# setUp/tearDown
# ~~~~~~~~~~~~~~~
def layer_setUp(self):
    """ cleanUp() is required to clear out the application registry
    between tests (done in setUp for good measure too)
    """
    testing.cleanUp()
    config = testing.setUp()
    config.include('pyramid_zcml')
    for zcml in CGWG_ZCMLS:
        config.load_zcml('collective.generic.webbuilder:%s' % zcml)


def layer_tearDown(self):
    """ cleanUp() is required to clear out the application registry
    between tests
    """
    for s in utils._LAUNCHED_SERVERS:
        s.tearDown()
    testing.cleanUp()


def test_doctests_suite(directory=None,
                        globs=None,
                        suite=None,
                        testklass=None,
                        setUp=None, tearDown=None):
    """A doctest suite launcher.
    You can even launch doctests from others packages with the
    webbuilder setup with embedding this test suite
    You can even add others globals in those tests.
    No need to copy and duplicate this file, it is useless.
    directory: where to find files to test
    globs: A dictionnary to setup test globals from.
    suite: a TestSuite object
    testklass: only useful if you are inside a Zope2 environment,
    because ztc comes from there.
    Note that in this case, setUp and tearDown are useless.
    Indeed modern application relys more on the setUp and tearDown functions.
    tearDown: tearDown code to run
    setUp: setUp code to run
    """
    if not directory:
        directory, _f = os.path.split(os.path.abspath(__file__))
    elif os.path.isfile(directory):
        directory = os.path.dirname(directory)
    if not globs:
        globs = get_globs()
    if not suite:
        suite = unittest.TestSuite()
    files = [
        os.path.join(directory, f) for f in os.listdir(directory)
        if f.endswith('.txt')
        #and f.endswith('browser.txt')
    ]
    if files:
        options = (doctest.REPORT_ONLY_FIRST_FAILURE |
                   doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
        for test in files:
            ft = None
            if not setUp:
                setUp = layer_setUp
            if not tearDown:
                tearDown = layer_tearDown
            ft = doctest.DocFileSuite(
                test,
                optionflags=options,
                globs=globs,
                setUp=setUp,
                tearDown=tearDown,
                module_relative=False)
            if ft:
                suite.addTest(ft)
    return suite


def test_suite():
    """."""
    suite = unittest.TestSuite()
    return test_doctests_suite(suite=suite)

# vim:set ft=python:
