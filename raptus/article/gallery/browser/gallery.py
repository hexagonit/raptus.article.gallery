from zope import interface, component

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

try:  # Plone 4 and higher
    from Products.ATContentTypes.interfaces.image import IATImage
except:  # BBB Plone 3
    from Products.ATContentTypes.interface.image import IATImage

from raptus.article.core.config import MANAGE_PERMISSION
from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core import interfaces
from raptus.article.images.interfaces import IImages, IImage


class IGalleryLeft(interface.Interface):
    """ Marker interface for the gallery left viewlet
    """


class ComponentLeft(object):
    """ Component which lists the images on the left side
    """
    interface.implements(interfaces.IComponent, interfaces.IComponentSelection)
    component.adapts(interfaces.IArticle)

    title = _(u'Gallery left')
    description = _(u'Gallery of the images contained in the article on the left side.')
    image = '++resource++gallery_left.gif'
    interface = IGalleryLeft
    viewlet = 'raptus.article.gallery.left'

    def __init__(self, context):
        self.context = context


class ViewletLeft(ViewletBase):
    """ Viewlet listing the images on the left side
    """

    index = ViewPageTemplateFile('gallery.pt')
    css_class = "componentLeft gallery-left"
    thumb_size = "galleryleft"
    component = "gallery.left"
    type = "left"

    def _class(self, brain, i, l):
        # TODO: why is brain needed here?
        cls = []
        if i == 0:
            cls.append('first')
        if i == l - 1:
            cls.append('last')
        if i % 2 == 0:
            cls.append('odd')
        if i % 2 == 1:
            cls.append('even')
        return ' '.join(cls)

    @property
    def show_description(self):
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty('gallery_%s_description' % self.type, False)

    @property
    @memoize
    def images(self):
        # prepare tools
        manageable = interfaces.IManageable(self.context)

        # get all images for editors, but only visible ones for viewers
        images = self.get_visible_images()

        # get specific info for displaying
        # management links (view, edit, show, hide, etc.)
        items = manageable.getList(images, self.component)

        l = len(items)
        for i, item in enumerate(items):

            # get an ATImage object wrapped with raptus.article.images IImage
            # adapter that gives it getImageURL, getImageTag, getSize and getCaption
            image = IImage(item['obj'])

            # add information like CSS class, image caption, etc.
            item = self.add_display_information(item, image, i, l)

            # if any thumb size is smaller than the image itself,
            # then display the lightbox overlay
            item = self.add_lightbox_information(item, image)

        return items

    def check_display_lightbox(self, item, image):
        """Check whether we should display lightbox overlay for this image and
        if positive, adds relevant information to the item dict.
        """
        # get image and thumb sizes
        w, h = item['obj'].getSize()
        tw, th = image.getSize(self.thumb_size)

        rel, url = None, None
        # if any thumb size is smaller than the image itself,
        # then activate the lightbox
        if (tw < w and tw > 0) or (th < h and th > 0):
            rel = 'lightbox[%s]' % self.css_class,
            url = image.getImageURL(size="popup")

        item.update({'rel': rel,
                     'url': url})
        return item

    def add_display_information(self, item, image, i, l):
        """Add more information for displaying this item in HTML."""

        # use IImage adapter's getCaption
        caption = image.getCaption()

        # get CSS class for this item
        cls = self._class(item['brain'], i, l)  # TODO: brain is probably not needed
        cls += self.is_item_hidden(item)

        # use IImage adapter's getImageTag to get HTML img tab of image's thumb
        img_tag = image.getImage(self.thumb_size)

        # get Description from the brain
        description = item['brain'].Description

        item.update({'caption': caption,
                     'class': cls,
                     'img': img_tag,
                     'description': description})
        return item

    def is_item_hidden(self, item):
        """Returns CSS class for hidden image, if applicable."""
        if 'show' in item and item['show']:
            # if item has a 'show' link and that link is not empty,
            # then this Image must be marked hidden
            return ' hidden'
        return ''

    def get_visible_images(self):
        """If user can manage images then display all images. otherwise display
        only images that are marked as 'show'."""
        provider = IImages(self.context)
        mship = getToolByName(self.context, 'portal_membership')

        if mship.checkPermission(MANAGE_PERMISSION, self.context):
            # return images directly contained in this Article
            return provider.getImages()
        else:
            # return images directly contained in this Article (self.context)
            # but filter out those that don't have this component (self.component)
            # in their 'component' field -> this meands that the Image is hidden
            # for this component
            return provider.getImages(component=self.component)


class IGalleryRight(interface.Interface):
    """ Marker interface for the gallery right viewlet
    """


class ComponentRight(object):
    """ Component which lists the images on the right side
    """
    interface.implements(interfaces.IComponent, interfaces.IComponentSelection)
    component.adapts(interfaces.IArticle)

    title = _(u'Gallery right')
    description = _(u'Gallery of the images contained in the article on the right side.')
    image = '++resource++gallery_right.gif'
    interface = IGalleryRight
    viewlet = 'raptus.article.gallery.right'

    def __init__(self, context):
        self.context = context


class ViewletRight(ViewletLeft):
    """ Viewlet listing the images on the right side
    """
    css_class = "componentRight gallery-right"
    thumb_size = "galleryright"
    component = "gallery.right"
    type = "right"


class IGalleryColumns(interface.Interface):
    """ Marker interface for the gallery columns viewlet
    """


class ComponentColumns(object):
    """ Component which lists the articles in multiple columns
    """
    interface.implements(interfaces.IComponent, interfaces.IComponentSelection)
    component.adapts(interfaces.IArticle)

    title = _(u'Gallery columns')
    description = _(u'Gallery of the images contained in the article arranged in columns.')
    image = '++resource++gallery_columns.gif'
    interface = IGalleryColumns
    viewlet = 'raptus.article.gallery.columns'

    def __init__(self, context):
        self.context = context


class ViewletColumns(ViewletLeft):
    """ Viewlet listing the images in multiple columns
    """
    css_class = "columns gallery-columns"
    thumb_size = "gallerycolumns"
    component = "gallery.columns"
    type = "columns"

    def _class(self, brain, i, l):
        # TODO: I belive brain is not needed here also
        # 'l' is not needed
        props = getToolByName(self.context, 'portal_properties').raptus_article
        i = i % props.getProperty('gallery_columns', 3)
        return super(ViewletColumns, self)._class(brain, i, props.getProperty('gallery_columns', 3))
