"""
Checking specifics portal settings.
This package must run in a cron package (needs app_config.py)
"""

import unittest2 as unittest

from base import IntegrationTestCase

from Products.CMFCore.utils import getToolByName

# adapt if any need to your testing utils module.
from collective.cron.tests.globals import *

class TestSetup(IntegrationTestCase):
    """Check Policy."""

    def test_Noop(self):
        self.assertEquals(True, True)

def test_suite():
    """."""
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.defaultTestLoader.loadTestsFromName(
            __name__))
    return suite  

