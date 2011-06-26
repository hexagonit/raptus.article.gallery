# -*- coding: utf-8 -*-
"""Tests for the galleries components."""

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.gallery.tests.base import RAGalleryIntegrationTestCase

import mock
import unittest2 as unittest


class TestCheckDisplayLightBox(unittest.TestCase):
    """Edge-cases unit tests for check_display_lightbox() of ViewletLeft."""

    def makeViewletLeft(self):
        """Prepare an instance of ViewletLeft"""
        from raptus.article.gallery.browser.gallery import ViewletLeft
        context = mock.Mock(spec=''.split())
        request = mock.Mock(spec=''.split())
        return ViewletLeft(context, request, None)

    @mock.patch('raptus.article.gallery.browser.gallery.IImage')
    def test_thumb_size_zero(self, IImage):
        """Don't display light box if thumb_size is zero."""
        item = dict(obj=mock.Mock(spec='getSize'.split()))
        item['obj'].getSize.return_value = (100, 100)
        IImage.return_value.getSize.return_value = (0, 0)

        viewlet = self.makeViewletLeft()
        item = viewlet.check_display_lightbox(item)
        item['rel'] = None
        item['url'] = None

    @mock.patch('raptus.article.gallery.browser.gallery.IImage')
    def test_thumb_size_equal(self, IImage):
        """Don't display light box if image thumb size is the same as
        image original size.
        """
        item = dict(obj=mock.Mock(spec='getSize'.split()))
        item['obj'].getSize.return_value = (100, 100)
        IImage.return_value.getSize.return_value = (100, 100)

        viewlet = self.makeViewletLeft()
        item = viewlet.check_display_lightbox(item)
        item['rel'] = None
        item['url'] = None

    @mock.patch('raptus.article.gallery.browser.gallery.IImage')
    def test_thumb_size_ok(self, IImage):
        """Display light box if image thumb size is lower than
        image original size, but higher than 0.
        """
        item = dict(obj=mock.Mock(spec='getSize getImageUrl'.split()))
        item['obj'].getSize.return_value = (50, 50)
        item['obj'].getImageUrl.return_value = 'http://foo'
        IImage.return_value.getSize.return_value = (100, 100)

        viewlet = self.makeViewletLeft()
        item = viewlet.check_display_lightbox(item)
        item['rel'] = 'lightbox[componentLeft gallery-left]'
        item['url'] = 'http://foo'


class TestAddDisplayInformation(unittest.TestCase):
    """Edge-cases unit tests for add_display_information() of ViewletLeft."""

    def makeViewletLeft(self):
        """Prepare an instance of ViewletLeft"""
        from raptus.article.gallery.browser.gallery import ViewletLeft
        context = mock.Mock(spec=''.split())
        request = mock.Mock(spec=''.split())
        return ViewletLeft(context, request, None)

    @mock.patch('raptus.article.gallery.browser.gallery.ViewletLeft._class')
    @mock.patch('raptus.article.gallery.browser.gallery.IImage')
    def test_caption(self, IImage, _class):
        """Test setting Image caption."""
        item = dict(brain=mock.Mock(), obj=None)
        _class.return_value = ''
        IImage.return_value.getCaption.return_value = 'foo'

        viewlet = self.makeViewletLeft()
        item = viewlet.add_display_information(item, 0, 0)
        item['caption'] = 'foo'

    @mock.patch('raptus.article.gallery.browser.gallery.ViewletLeft._class')
    @mock.patch('raptus.article.gallery.browser.gallery.IImage')
    def test_class(self, IImage, _class):
        """Test setting Image class with _class() method."""
        item = dict(brain=mock.Mock(), obj=None)
        _class.return_value = 'foo'

        viewlet = self.makeViewletLeft()
        item = viewlet.add_display_information(item, 0, 0)
        item['class'] = 'foo'

    @mock.patch('raptus.article.gallery.browser.gallery.ViewletLeft._class')
    @mock.patch('raptus.article.gallery.browser.gallery.IImage')
    def test_hidden(self, IImage, _class):
        """Test that 'hidden' is appended to class if Image is hidden."""
        item = dict(brain=mock.Mock(), obj=None, show='http://show_this_image')
        _class.return_value = 'foo'

        viewlet = self.makeViewletLeft()
        item = viewlet.add_display_information(item, 0, 0)
        item['class'] = 'foo hidden'

    @mock.patch('raptus.article.gallery.browser.gallery.ViewletLeft._class')
    @mock.patch('raptus.article.gallery.browser.gallery.IImage')
    def test_tag(self, IImage, _class):
        """Test setting Image html tag with _getImage() method."""
        item = dict(brain=mock.Mock(), obj=None)
        _class.return_value = ''
        IImage.return_value.getImage.return_value = '<img src="foo" />'

        viewlet = self.makeViewletLeft()
        item = viewlet.add_display_information(item, 0, 0)
        item['tag'] = '<img src="foo" />'

    @mock.patch('raptus.article.gallery.browser.gallery.ViewletLeft._class')
    @mock.patch('raptus.article.gallery.browser.gallery.IImage')
    def test_description(self, IImage, _class):
        """Test setting Image description."""
        item = dict(brain=mock.Mock(), obj=None)
        item['brain'].Description = 'foo'
        _class.return_value = ''

        viewlet = self.makeViewletLeft()
        item = viewlet.add_display_information(item, 0, 0)
        item['description'] = 'foo'


class TestIsItemHidden(unittest.TestCase):
    """Edge-cases unit tests for is_item_hidden() of ViewletLeft."""

    def makeViewletLeft(self):
        """Prepare an instance of ViewletLeft"""
        from raptus.article.gallery.browser.gallery import ViewletLeft
        context = mock.Mock(spec=''.split())
        request = mock.Mock(spec=''.split())
        return ViewletLeft(context, request, None)

    def test_hidden(self):
        """Test hidden is returned if item has 'show' url set."""
        item = dict(show='http://show_this_image')
        viewlet = self.makeViewletLeft()
        self.assertEquals(' hidden', viewlet.is_item_hidden(item))

    def test_not_hidden(self):
        """Test empty string returned if item does not have 'show' url set."""
        item = dict()
        viewlet = self.makeViewletLeft()
        self.assertEquals('', viewlet.is_item_hidden(item))


class TestGetVisibleImages(unittest.TestCase):
    """Edge-cases unit tests for get_visible_images() of ViewletLeft."""

    def makeViewletLeft(self):
        """Prepare an instance of ViewletLeft"""
        from raptus.article.gallery.browser.gallery import ViewletLeft
        context = mock.Mock(spec=''.split())
        request = mock.Mock(spec=''.split())
        return ViewletLeft(context, request, None)

    @mock.patch('raptus.article.gallery.browser.gallery.getToolByName')
    @mock.patch('raptus.article.gallery.browser.gallery.IImages')
    def test_only_visible_images_for_reader(self, IImages, getToolByName):
        """Test that all images are returned if user can not edit the Article."""
        viewlet = self.makeViewletLeft()
        getToolByName.return_value.checkPermission.return_value = False
        viewlet.get_visible_images()
        IImages.return_value.getImages.assert_called_once_with(component='gallery.left')

    @mock.patch('raptus.article.gallery.browser.gallery.getToolByName')
    @mock.patch('raptus.article.gallery.browser.gallery.IImages')
    def test_all_images_for_editor(self, IImages, getToolByName):
        """Test that all images are returned if user can edit the Article."""
        viewlet = self.makeViewletLeft()
        getToolByName.return_value.raptus_article.getProperty.return_value = True
        viewlet.get_visible_images()
        IImages.return_value.getImages.assert_called_once_with()


class TestViewletLeftClass(unittest.TestCase):
    """Edge-cases unit tests for _class() of ViewletLeft."""

    def makeViewletLeft(self):
        """Prepare an instance of ViewletLeft"""
        from raptus.article.gallery.browser.gallery import ViewletLeft
        context = mock.Mock(spec=''.split())
        request = mock.Mock(spec=''.split())
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
        context = mock.Mock(spec=''.split())
        request = mock.Mock(spec=''.split())
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
        self.portal.article.invokeFactory('Image', 'image1')

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

    def test_show_description(self):
        """Test the main method of ViewletLeft."""
        from raptus.article.gallery.browser.gallery import ViewletLeft
        viewlet = ViewletLeft(self.portal.article, self.layer['request'], None)
        self.portal.portal_properties.raptus_article.gallery_left_description = True

        self.assertEquals(viewlet.show_description, True)

    def test_images(self):
        """Test the main method of ViewletLeft."""

        # add additional test image, with more metadata set
        self.portal.article.invokeFactory('Image', 'image2',
                                            title='Image 2',
                                            description='Image 2 description')

        from raptus.article.gallery.browser.gallery import ViewletLeft
        viewlet = ViewletLeft(self.portal.article, self.layer['request'], None)
        images = viewlet.images

        self.assertEquals(len(images), 2)
        image = images[1]  # take the second image

        self.assertEquals(image['id'], 'image2')
        self.assertEquals(image['obj'], self.portal.article.image2)
        self.assertEquals(image['anchor'], 'gallery.leftimage2')
        self.assertEquals(image['class'], 'last even')
        self.assertEquals(image['caption'], 'Image 2 description')
        self.assertEquals(image['description'], 'Image 2 description')

        self.assertEquals(image['view'], 'http://nohost/plone/article/image2/view')
        self.assertEquals(image['edit'], 'http://nohost/plone/article/image2/edit')
        self.assertEquals(image['delete'], 'http://nohost/plone/article/image2/delete_confirmation')

        self.assertEquals(image['up'], 'http://nohost/plone/article/article_moveitem?anchor=gallery.leftimage2&delta=-1&item_id=image2')
        self.assertEquals(image['down'], None)

        self.assertEquals(image['show'], None)
        self.assertEquals(image['hide'], 'http://nohost/plone/article/@@article_showhideitem?anchor=gallery.leftimage2&action=hide&uid=%s&component=gallery.left' % self.portal.article.image2.UID())
