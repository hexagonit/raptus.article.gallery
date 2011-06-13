# -*- coding: utf-8 -*-
"""Layers and TestCases for our tests."""

from __future__ import with_statement

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2

import unittest2 as unittest


class RaptusArticleGalleryLayer(PloneSandboxLayer):
    """Layer for Raptus Article Gallery tests."""

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Prepare Zope."""
        import raptus.article.gallery
        self.loadZCML(package=raptus.article.gallery)
        z2.installProduct(app, 'raptus.article.core')
        z2.installProduct(app, 'raptus.article.images')
        z2.installProduct(app, 'raptus.article.gallery')

    def setUpPloneSite(self, portal):
        """Install into Plone site using portal_setup."""
        applyProfile(portal, 'raptus.article.gallery:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'raptus.article.core')
        z2.uninstallProduct(app, 'raptus.article.images')
        z2.uninstallProduct(app, 'raptus.article.gallery')

# FIXTURES
RAPTUS_ARTICLE_GALLERY_FIXTURE = RaptusArticleGalleryLayer()

# LAYERS
INTEGRATION_TESTING = IntegrationTesting(
    bases=(RAPTUS_ARTICLE_GALLERY_FIXTURE, ),
    name="raptus.article.gallery:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RAPTUS_ARTICLE_GALLERY_FIXTURE,),
    name="raptus.article.gallery:Functional")


# TESTCASES
class RAGalleryIntegrationTestCase(unittest.TestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    layer = INTEGRATION_TESTING


class RAGalleryFunctionalTestCase(unittest.TestCase):
    """We use this base class for all functional tests in this package -
    tests that require a full-blown Plone instance for testing.
    """
    layer = FUNCTIONAL_TESTING
