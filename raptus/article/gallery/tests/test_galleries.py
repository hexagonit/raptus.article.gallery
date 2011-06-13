# -*- coding: utf-8 -*-
"""Tests for the galleries components."""

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.gallery.tests.base import RAGalleryIntegrationTestCase

import mock
import unittest2 as unittest


class TestViewletLeftClass(unittest.TestCase):
    """Edge-cases unit tests for _class() of ViewletLeft."""

    def makeViewletLeft(self):
        """Prepare an instance of ViewletLeft"""
        from raptus.article.gallery.browser.gallery import ViewletLeft
        context = mock.Mock(spec=''.split)
        request = mock.Mock(spec=''.split)
        return ViewletLeft(context, request, None)

    def test_first(self):
        """Test that correct CSS classes are set for first image."""
        viewlet = self.makeViewletLeft()
        self.assertEquals('first', viewlet._class(None, 0, 0).split()[0])
        self.assertTrue('first' not in viewlet._class(None, 1, 0))
        self.assertTrue('first' not in viewlet._class(None, 2, 0))

    def test_last(self):
        """Test that correct CSS classes are set for last image."""
        viewlet = self.makeViewletLeft()
        self.assertEquals('last', viewlet._class(None, 3, 4).split()[0])
        self.assertTrue('last' not in viewlet._class(None, 1, 4))
        self.assertTrue('last' not in viewlet._class(None, 1, 1))

    def test_even(self):
        """Test that correct CSS classes are set for even images."""
        viewlet = self.makeViewletLeft()
        self.assertEquals('even', viewlet._class(None, 1, 0))
        self.assertEquals('even', viewlet._class(None, 3, 0))
        self.assertNotEquals('even', viewlet._class(None, 2, 0))

    def test_odd(self):
        """Test that correct CSS classes are set for odd images."""
        viewlet = self.makeViewletLeft()
        self.assertEquals('odd', viewlet._class(None, 2, 0))
        self.assertEquals('odd', viewlet._class(None, 4, 0))
        self.assertNotEquals('odd', viewlet._class(None, 3, 0))


class TestViewletColumnsClass(unittest.TestCase):
    """Edge-cases unit tests for _class() of ViewletColumns."""

    def makeViewletColumns(self):
        """Prepare an instance of ViewletColumns"""
        from raptus.article.gallery.browser.gallery import ViewletColumns
        context = mock.Mock(spec=''.split)
        request = mock.Mock(spec=''.split)
        return ViewletColumns(context, request, None)

    @mock.patch('raptus.article.gallery.browser.gallery.ViewletLeft._class')
    @mock.patch('raptus.article.gallery.browser.gallery.getToolByName')
    def test_columns_divider(self, getToolByName, super_class):
        """Test that correct CSS classes are set for first image."""
        viewlet = self.makeViewletColumns()
        getToolByName.return_value.raptus_article.getProperty.return_value = 5

        viewlet._class(None, 3, 0)
        super_class.called_with(None, 3, 5)

        viewlet._class(None, 4, 0)
        super_class.called_with(None, 4, 5)

        viewlet._class(None, 5, 0)
        super_class.called_with(None, 0, 5)


class TestGalleriesIntegration(RAGalleryIntegrationTestCase):
    """Test classes and viewlets of r.a.gallery components."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')
        self.portal.article.invokeFactory('Image', 'image')

    def test_component_left(self):
        """Test default attributes of ComponentLeft."""

        from raptus.article.gallery.browser.gallery import IGalleryLeft
        from raptus.article.gallery.browser.gallery import ComponentLeft
        component = ComponentLeft(self.portal.article)

        self.assertEquals(component.title, 'Gallery left')
        self.assertEquals(component.description, 'Gallery of the images contained in the article on the left side.')
        self.assertEquals(component.image, '++resource++gallery_left.gif')
        self.assertEquals(component.interface, IGalleryLeft)
        self.assertEquals(component.viewlet, 'raptus.article.gallery.left')
        self.assertEquals(component.context, self.portal.article)

    def test_component_right(self):
        """Test default attributes of ComponentRight."""

        from raptus.article.gallery.browser.gallery import IGalleryRight
        from raptus.article.gallery.browser.gallery import ComponentRight
        component = ComponentRight(self.portal.article)

        self.assertEquals(component.title, 'Gallery right')
        self.assertEquals(component.description, 'Gallery of the images contained in the article on the right side.')
        self.assertEquals(component.image, '++resource++gallery_right.gif')
        self.assertEquals(component.interface, IGalleryRight)
        self.assertEquals(component.viewlet, 'raptus.article.gallery.right')
        self.assertEquals(component.context, self.portal.article)

    def test_component_columns(self):
        """Test default attributes of ComponentColumns."""

        from raptus.article.gallery.browser.gallery import IGalleryColumns
        from raptus.article.gallery.browser.gallery import ComponentColumns
        component = ComponentColumns(self.portal.article)

        self.assertEquals(component.title, 'Gallery columns')
        self.assertEquals(component.description, 'Gallery of the images contained in the article arranged in columns.')
        self.assertEquals(component.image, '++resource++gallery_columns.gif')
        self.assertEquals(component.interface, IGalleryColumns)
        self.assertEquals(component.viewlet, 'raptus.article.gallery.columns')
        self.assertEquals(component.context, self.portal.article)
