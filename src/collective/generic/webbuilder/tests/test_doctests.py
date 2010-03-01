"""
Launching all doctests in a specific directory with globals and setup enhancement

It will try to load user defined objects in ``collective.generic.webbuilder.tests.user_`` prefixed python modules.

goal is to regenerate the test infrastructure without impacting user-specific test boilerplate.
If you need to edit something in this file, you must have better to do it in 'an user specific' file.
Files/Object that you can edit and get things overidden are:

    - collective.generic.webbuilder.tests.user_testcase:

        * method: collective_generic_webbuilder_setUp

            Default tearDown function

        * method: collective_generic_webbuilder_tearDown
            Default setUp function

        * class:  DocTestCase

            Default Zope2 testCase class

    - collective.generic.webbuilder.tests.user_utils:

        utilities functions to register as a global in tests

    - collective.generic.webbuilder.tests.user_globals:

        Any variable added in there will be available in relative tests as a global
        Example:
        # Add in user_globals.py
        from for import bar
        and in your doctests, you can do without importing bar:
        >>> bar.something


"""
import unittest
import doctest
import os.path

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UTILITIES AND GLOBBALS SUPPORT / EDIT .user_utils.py or .user.globals.py to overidde
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# if you have plone.reload out there add an helper to use in doctests while programming
# just use preload(module) in pdb :)
# it would be neccessary for you to precise each module to reload, this method is also not recursive.
# eg: (pdb) from foo import bar;preload(bar)
# see utils.py for details

from collective.generic.webbuilder.tests.utils import *
try:from collective.generic.webbuilder.tests.user_utils import *
except:pass
from collective.generic.webbuilder.tests.globals import *
try:from collective.generic.webbuilder.tests.user_globals import *
except:pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# setUp/tearDown in a non-Zope2 environement / EDIT .user_testcase.{setUp, tearDown} to overidde
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def collective_generic_webbuilder_setUp(test):pass
def collective_generic_webbuilder_tearDown(test):pass
try:from collective.generic.webbuilder.tests.user_testcase import collective_generic_webbuilder_setUp
except:pass
try:from collective.generic.webbuilder.tests.user_testcase import collective_generic_webbuilder_tearDown
except:pass

def test_doctests_suite(directory=None,
                        globs=None,
                        suite=None,
                        testklass=None,
                        setUp=None, tearDown=None
                       ):
    """A doctest suite launcher.
    You can even launch doctests from others packages with the
    webbuilder setup with embedding this test suite
    You can even add others globals in those tests.
    No need to copy and duplicate this file, it is useless.

      #Example : This snippet will launch all txt doctests in the other package directory
      >>> from collective.generic.webbuilder.tests.test_setup import test_doctests_suite as ts
      >>> def test_suite():
      ...     globs = globals()
      ...     return ts(__file__, globs)

    directory: where to find files to test
    globs: A dictionnary to setup test globals from.
    suite: a TestSuite object
    testklass: only useful if you are inside a Zope2 environment, because ztc comes from there.
               Note that in this case, setUp and tearDown are useless.
    Indeed modern application relys more on the setUp and tearDown functions.
    tearDown: tearDown code to run
    setUp: setUp code to run
    """
    if not directory:
        directory, _f = os.path.split(os.path.abspath(__file__))
    elif os.path.isfile(directory):
        directory = os.path.dirname(directory)
    if not globs: globs={}
    g = globals()
    for key in g: globs.setdefault(key, g[key])
    if not suite: suite = unittest.TestSuite()
    files = [os.path.join(directory, f) for f in os.listdir(directory)
             if f.endswith('.txt')
             #and f.endswith('browser.txt')
            ]
    if files:
        options = doctest.REPORT_ONLY_FIRST_FAILURE |\
                  doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        for test in files:
            ft = None
            if not setUp:
                setUp=collective_generic_webbuilder_setUp
            if not tearDown:
                tearDown=collective_generic_webbuilder_tearDown
            ft = doctest.DocFileSuite(
                test,
                optionflags=options,
                globs=globs,
                setUp=setUp,
                tearDown=tearDown,
                module_relative = False,
            )
            if ft: suite.addTest(ft)
    return suite

def test_suite():
    """."""
    suite = unittest.TestSuite()
    return test_doctests_suite(suite=suite)

# vim:set ft=python:
