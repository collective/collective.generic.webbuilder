from Testing import ZopeTestCase as ztc
import transaction
from OFS.Folder import Folder

import unittest2 as unittest

from zope.configuration import xmlconfig

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting as BIntegrationTesting, FunctionalTesting as BFunctionalTesting
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing.selenium_layers import SELENIUM_FUNCTIONAL_TESTING as SELENIUM_TESTING
from plone.testing import zodb, zca, z2

TESTED_PRODUCTS = (\
#with_ploneproduct_ldap
    'LDAPMultiPlugins',
    'LDAPUserFolder',
    'PloneLDAP',
    'plone.app.ldap',
)

from plone.app.testing import (
    TEST_USER_ROLES,
    TEST_USER_NAME,
    TEST_USER_ID,
    SITE_OWNER_NAME,
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

class FooBarMyothereggLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )
    """Layer to setup the myotheregg site"""
    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def setUpZope(self, app, configurationContext):
        """Set up the additional products required for the foo.bar) site myotheregg.
        until the setup of the Plone site testing layer.
        """
        self.app = app
        self.browser = Browser(app)
        # old zope2 style products
        for product in TESTED_PRODUCTS:
            z2.installProduct(product)

        # ----------------------------------------------------------------------
        # Import all our python modules required by our packages
        # ---------------------------------------------------------------------
        #with_ploneproduct_dexterity
        import plone.app.dexterity
        self.loadZCML('configure.zcml', package=plone.app.dexterity)
        #with_ploneproduct_cgallery
        import collective.gallery
        self.loadZCML('configure.zcml', package=collective.gallery)
        #with_ploneproduct_ldap
        import Products.PloneLDAP
        self.loadZCML('configure.zcml', package=Products.PloneLDAP)
        import plone.app.ldap
        self.loadZCML('configure.zcml', package=plone.app.ldap)
        #with_ploneproduct_patheming
        import plone.app.theming
        self.loadZCML('configure.zcml', package=plone.app.theming)
        import plone.app.themingplugins
        self.loadZCML('configure.zcml', package=plone.app.themingplugins)
        #with_ploneproduct_cz3cformnorobots
        import collective.z3cform.norobots
        self.loadZCML('configure.zcml', package=collective.z3cform.norobots)

        # -----------------------------------------------------------------------
        # Load our own myotheregg
        # -----------------------------------------------------------------------
        import foo.bar.myotheregg
        self.loadZCML('configure.zcml', package=foo.bar.myotheregg)

        # ------------------------------------------------------------------------
        # - Load the python packages that are registered as Zope2 Products
        #   which can't happen until we have loaded the package ZCML.
        # ------------------------------------------------------------------------

        #with_ploneproduct_patheming
        z2.installProduct(app, 'plone.app.theming')
        z2.installProduct(app, 'plone.app.themingplugins')
        z2.installProduct(app, 'foo.bar.myotheregg')

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
        applyProfile(portal, 'foo.bar.myotheregg:default')


class LayerMixin(object):
    defaultBases = (FooBarMyothereggLayer() ,)

    def testSetUp(self):
        self.add_user(
            self['portal'],
            PLONE_MANAGER_ID,
            PLONE_MANAGER_NAME,
            PLONE_MANAGER_PASSWORD,
            ['Menager']+TEST_USER_ROLES)

    def add_user(self, portal, id, username, password, roles=None):
        if not roles: roles = TEST_USER_ROLES[:]
        self.loginAsPortalOwner()
        pas = portal['acl_users']
        pas.source_users.addUser(id, username, password)
        setRoles(portal, id, roles)
        self.logout()

    def loginAsPortalOwner(self):
        z2.login(self['app']['acl_users'], SITE_OWNER_NAME)

    def logout(self):
        logout()

class IntegrationTesting(LayerMixin, BIntegrationTesting):
    def testSetUp(self):
        BIntegrationTesting.testSetUp(self)
        LayerMixin.testSetUp(self)

class FunctionalTesting(LayerMixin, BFunctionalTesting):
    def testSetUp(self):
        BFunctionalTesting.testSetUp(self)
        LayerMixin.testSetUp(self) 

FOO_BAR_MYOTHEREGG_FIXTURE             = FooBarMyothereggLayer()
FOO_BAR_MYOTHEREGG_INTEGRATION_TESTING = IntegrationTesting(name = "FooBarMyotheregg:Integration")
FOO_BAR_MYOTHEREGG_FUNCTIONAL_TESTING  = FunctionalTesting( name = "FooBarMyotheregg:Functional")
FOO_BAR_MYOTHEREGG_SELENIUM_TESTING    = FunctionalTesting(bases = (SELENIUM_TESTING, FOO_BAR_MYOTHEREGG_FUNCTIONAL_TESTING,), name = "FooBarMyotheregg:Selenium")

# vim:set ft=python:
