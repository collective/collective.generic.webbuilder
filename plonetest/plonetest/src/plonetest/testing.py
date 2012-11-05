from Testing import ZopeTestCase as ztc
import transaction
from OFS.Folder import Folder

import unittest2 as unittest

from zope.configuration import xmlconfig

from plone.app.testing import (
    FunctionalTesting as BFunctionalTesting,
    IntegrationTesting as BIntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
    helpers,
    setRoles,
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    TEST_USER_ID,
    TEST_USER_NAME,
    TEST_USER_NAME,
    TEST_USER_ROLES,
)
from plone.app.testing.selenium_layers import (
    SELENIUM_FUNCTIONAL_TESTING as SELENIUM_TESTING
)
from plone.testing import Layer, zodb, zca, z2

TESTED_PRODUCTS = (\
)

PLONE_MANAGER_NAME = 'Plone_manager'
PLONE_MANAGER_ID = 'plonemanager'
PLONE_MANAGER_PASSWORD = 'plonemanager'
GENTOO_FF_UA = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20090912 Gentoo Shiretoko/3.5.3'

class PlonetestLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )
    """Layer to setup the plonetest site"""
    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def setUpZope(self, app, configurationContext):
        """Set up the additional products required for the ) site plonetest.
        until the setup of the Plone site testing layer.
        """
        self.app = app
        self.browser = Browser(app)
        # old zope2 style products
        z2.installProduct(app, 'Products.PythonScripts')
        for product in TESTED_PRODUCTS:
            z2.installProduct(app, product)

        # ----------------------------------------------------------------------
        # Import all our python modules required by our packages
        # ---------------------------------------------------------------------
        #with_ploneproduct_dexterity
        import plone.app.dexterity
        self.loadZCML('configure.zcml', package=plone.app.dexterity)

        # -----------------------------------------------------------------------
        # Load our own plonetest
        # -----------------------------------------------------------------------
        import plonetest
        self.loadZCML('configure.zcml', package=plonetest)

        # ------------------------------------------------------------------------
        # - Load the python packages that are registered as Zope2 Products
        #   which can't happen until we have loaded the package ZCML.
        # ------------------------------------------------------------------------

        z2.installProduct(app, 'plonetest')

        # -------------------------------------------------------------------------
        # support for sessions without invalidreferences if using zeo temp storage
        # -------------------------------------------------------------------------
        app.REQUEST['SESSION'] = self.Session()
        if not hasattr(app, 'temp_folder'):
            tf = Folder('temp_folder')
            app._setObject('temp_folder', tf)
            transaction.commit()
        ztc.utils.setupCoreSessions(app)

    def setUpPloneSite(self, portal):
        self.portal = portal
        # Plone stuff. Workflows, portal content. Members folder, etc.
        self.applyProfile(portal, 'Products.CMFPlone:plone')
        self.applyProfile(portal, 'Products.CMFPlone:plone-content')
        self.applyProfile(portal, 'plonetest:default')


class LayerMixin(Layer):
    defaultBases = (PlonetestLayer() ,)

    def testTearDown(self):
        self.loginAsPortalOwner()
        if 'test-folder' in self['portal'].objectIds():
            self['portal'].manage_delObjects('test-folder')
        self['portal'].portal_membership.deleteMembers([PLONE_MANAGER_NAME])
        self.setRoles()
        self.login()
        transaction.commit()

    def testSetUp(self):
        if not self['portal']['acl_users'].getUser(PLONE_MANAGER_NAME):
            self.loginAsPortalOwner()
            self.add_user(
                self['portal'],
                PLONE_MANAGER_ID,
                PLONE_MANAGER_NAME,
                PLONE_MANAGER_PASSWORD,
                ['Manager']+TEST_USER_ROLES)
            self.logout()
        self.login(TEST_USER_NAME)
        self.setRoles(['Manager'])
        if not 'test-folder' in self['portal'].objectIds():
            self['portal'].invokeFactory('Folder', 'test-folder')
        self['test-folder'] = self['folder'] = self['portal']['test-folder']
        self.setRoles(TEST_USER_ROLES)
        transaction.commit()

    def add_user(self, portal, id, username, password, roles=None):
        if not roles: roles = TEST_USER_ROLES[:]
        self.loginAsPortalOwner()
        pas = portal['acl_users']
        pas.source_users.addUser(id, username, password)
        self.setRoles(roles, id)
        self.logout()

    def setRoles(self, roles=None, id=None):
        if roles is None:
            roles = TEST_USER_ROLES
        if id is None:
            id = TEST_USER_ID
        setRoles(self['portal'], id, roles)

    def loginAsPortalOwner(self):
        self.login(SITE_OWNER_NAME)

    def logout(self):
        helpers.logout()

    def login(self, id=None):
        if not id:
            id = TEST_USER_NAME
        try:
            z2.login(self['app']['acl_users'], id)
        except:
            z2.login(self['portal']['acl_users'], id)

class IntegrationTesting(LayerMixin, BIntegrationTesting):
    def testSetUp(self):
        BIntegrationTesting.testSetUp(self)
        LayerMixin.testSetUp(self)

class FunctionalTesting(LayerMixin, BFunctionalTesting):
    def testSetUp(self):
        BFunctionalTesting.testSetUp(self)
        LayerMixin.testSetUp(self)


class SimpleLayer(Layer):
    defaultBases = tuple()


PLONETEST_SIMPLE              = SimpleLayer(name='Plonetest:Simple')

PLONETEST_FIXTURE             = PlonetestLayer()
PLONETEST_INTEGRATION_TESTING = IntegrationTesting(name = "Plonetest:Integration")
PLONETEST_FUNCTIONAL_TESTING  = FunctionalTesting( name = "Plonetest:Functional")
PLONETEST_SELENIUM_TESTING    = FunctionalTesting(bases = (SELENIUM_TESTING,
                                                          PLONETEST_FUNCTIONAL_TESTING,),
                                                 name = "Plonetest:Selenium")



class Browser(z2.Browser): # pragma: no cover
    """Patch the browser class to be a little more like a webbrowser."""

    def __init__(self, app, url=None, headers=None):
        if headers is None: headers = []
        z2.Browser.__init__(self, app, url)
        self.mech_browser.set_handle_robots(False)
        for h in headers:
            k, val = h
            self.addHeader(k, val)
        if url is not None:
            self.open(url)

    def print_contents_to_file(self, dest='~/.browser.html'):

        fic = open(os.path.expanduser(dest), 'w')
        fic.write(self.contents)
        return fic

    @property
    def print_contents(self):
        """Print the browser contents somewhere for you to see its
        context in doctest pdb, t
        ype browser.print_contents(browser) and that's it,
        open firefox with file://~/browser.html."""
        return self.print_contents_to_file()

    @classmethod
    def new(cls, url, user=None, passwd=None, headers=None, login=False):
        """instantiate and return a testbrowser for convenience """
        if headers is None: headers = []
        if user: login = True
        if not user: user = PLONE_MANAGER_NAME
        if not passwd: passwd = PLONE_MANAGER_PASSWORD
        if login:
            auth = 'Basic %s:%s' % (user, passwd)
            headers.append(('Authorization', auth))
        headers.append(('User-agent' , GENTOO_FF_UA))
        browser = cls(PLONETEST_FUNCTIONAL_TESTING['app'],
                      url, headers=headers)
        return browser



# vim:set ft=python:
