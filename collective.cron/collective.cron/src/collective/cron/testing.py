from Testing import ZopeTestCase as ztc
import transaction
from OFS.Folder import Folder

import unittest2 as unittest

from zope.configuration import xmlconfig

from plone.app.testing import (
    FunctionalTesting as BFunctionalTesting,
    IntegrationTesting as BIntegrationTesting, 
    login,
    PLONE_FIXTURE,
    PloneSandboxLayer,
    setRoles,
    SITE_OWNER_NAME,
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


from plone.app.testing.helpers import (
    login,
    logout,
)

PLONE_MANAGER_NAME = 'Plone_manager'
PLONE_MANAGER_ID = 'plonemanager'
PLONE_MANAGER_PASSWORD = 'plonemanager'

def print_contents(browser, dest='~/.browser.html'):
    """Print the browser contents somewhere for you to see its context
    in doctest pdb, type print_contents(browser) and that's it, open firefox
    with file://~/browser.html."""
    import os
    open(os.path.expanduser(dest), 'w').write(browser.contents)

class Browser(z2.Browser):
    def print_contents(browser, dest='~/.browser.html'):
        return print_contents(browser, dest)

class CollectiveCronLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )
    """Layer to setup the cron site"""
    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def setUpZope(self, app, configurationContext):
        """Set up the additional products required for the collective) site cron.
        until the setup of the Plone site testing layer.
        """
        self.app = app
        self.browser = Browser(app)
        # old zope2 style products
        z2.installProduct(app, 'Products.PythonScripts')
        for product in TESTED_PRODUCTS:
            z2.installProduct(product)

        # ----------------------------------------------------------------------
        # Import all our python modules required by our packages
        # ---------------------------------------------------------------------
        #with_ploneproduct_dexterity
        import plone.app.dexterity
        self.loadZCML('configure.zcml', package=plone.app.dexterity)
        #with_ploneproduct_patheming
        import plone.app.theming
        self.loadZCML('configure.zcml', package=plone.app.theming)
        import plone.app.themingplugins
        self.loadZCML('configure.zcml', package=plone.app.themingplugins)

        # -----------------------------------------------------------------------
        # Load our own cron
        # -----------------------------------------------------------------------
        import collective.cron
        self.loadZCML('configure.zcml', package=collective.cron)

        # ------------------------------------------------------------------------
        # - Load the python packages that are registered as Zope2 Products
        #   which can't happen until we have loaded the package ZCML.
        # ------------------------------------------------------------------------

        #with_ploneproduct_patheming
        z2.installProduct(app, 'plone.app.theming')
        z2.installProduct(app, 'plone.app.themingplugins')
        z2.installProduct(app, 'collective.cron')

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
        self.applyProfile(portal, 'collective.cron:default')


class LayerMixin(Layer):
    defaultBases = (CollectiveCronLayer() ,)

    def testTearDown(self):
        self.loginAsPortalOwner()
        if 'test-folder' in self['portal'].objectIds():
            self['portal'].manage_delObjects('test-folder')
        self['portal'].portal_membership.deleteMembers([PLONE_MANAGER_NAME])
        self.setRoles()
        self.login()

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
        logout()

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


COLLECTIVE_CRON_SIMPLE              = SimpleLayer(name='CollectiveCron:Simple')

COLLECTIVE_CRON_FIXTURE             = CollectiveCronLayer()
COLLECTIVE_CRON_INTEGRATION_TESTING = IntegrationTesting(name = "CollectiveCron:Integration")
COLLECTIVE_CRON_FUNCTIONAL_TESTING  = FunctionalTesting( name = "CollectiveCron:Functional")
COLLECTIVE_CRON_SELENIUM_TESTING    = FunctionalTesting(bases = (SELENIUM_TESTING, 
                                                          COLLECTIVE_CRON_FUNCTIONAL_TESTING,), 
                                                 name = "CollectiveCron:Selenium")

# vim:set ft=python:
