# -*- coding: utf-8 -*-
"""Tests for installation and setup of this package."""

from Products.CMFCore.utils import getToolByName
from raptus.article.gallery.tests.base import RAGalleryIntegrationTestCase

import unittest2 as unittest


class TestInstall(RAGalleryIntegrationTestCase):
    """Test installation of raptus.article.gallery into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_product_installed(self):
        """Test if raptus.article.gallery is installed with
        portal_quickinstaller.
        """
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('raptus.article.gallery'))

    def test_dependencies_installed(self):
        """Test if raptus.article.images' dependencies are installed with
        portal_quickinstaller.
        """
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('raptus.article.core'))
        self.assertTrue(qi.isProductInstalled('raptus.article.images'))

    # propertiestool.xml
    def test_article_properties(self):
        """Test if raptus_article properties are correctly set."""

        article_props = self.portal.portal_properties.raptus_article
        self.assertEquals(article_props.images_galleryleft_width, 200)
        self.assertEquals(article_props.images_galleryleft_height, 0)
        self.assertEquals(article_props.images_galleryright_width, 200)
        self.assertEquals(article_props.images_galleryright_height, 0)
        self.assertEquals(article_props.images_gallerycolumns_width, 200)
        self.assertEquals(article_props.images_gallerycolumns_height, 0)
        self.assertEquals(article_props.gallery_columns, 3)
        self.assertEquals(article_props.gallery_columns_cropheight, 130)
        self.assertEquals(article_props.gallery_columns_cropwidth, 0)
        self.assertEquals(article_props.gallery_left_cropheight, 130)
        self.assertEquals(article_props.gallery_left_cropwidth, 0)
        self.assertEquals(article_props.gallery_right_cropheight, 130)
        self.assertEquals(article_props.gallery_right_cropwidth, 0)
        self.assertEquals(article_props.gallery_left_description, False)
        self.assertEquals(article_props.gallery_right_description, False)
        self.assertEquals(article_props.gallery_columns_description, False)

    # cssregistry.xml
    def test_css_registered(self):
        """Test if CSS files are registered with portal_css."""
        resources = self.portal.portal_css.getResources()

        ids = [r.getId() for r in resources]

        self.assertTrue('raptus.article.gallery.css' in ids,
                        'raptus.article.gallery.css not found in portal_css')

    # skins.xml
    def test_skins_folder_registered(self):
        """Test if raptus.article.core skins folders is registered."""
        skins = getToolByName(self.portal, 'portal_skins')
        skin_layer = skins.getSkinPath('Plone Default')

        self.assertTrue('raptus_article_gallery' in skin_layer,
                        'raptus_article_gallery skin folder is not registered')

    def test_viewlets_registered(self):
        """Test that all gallery viewlets are registered."""
        # TODO
        pass


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
