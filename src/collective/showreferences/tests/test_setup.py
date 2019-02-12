# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.showreferences.testing import COLLECTIVE_SHOWREFERENCES_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.showreferences is properly installed."""

    layer = COLLECTIVE_SHOWREFERENCES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.showreferences is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.showreferences'))

    def test_browserlayer(self):
        """Test that ICollectiveShowreferencesLayer is registered."""
        from collective.showreferences.interfaces import (
            ICollectiveShowreferencesLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveShowreferencesLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_SHOWREFERENCES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.showreferences'])

    def test_product_uninstalled(self):
        """Test if collective.showreferences is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.showreferences'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveShowreferencesLayer is removed."""
        from collective.showreferences.interfaces import \
            ICollectiveShowreferencesLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           ICollectiveShowreferencesLayer,
           utils.registered_layers())
