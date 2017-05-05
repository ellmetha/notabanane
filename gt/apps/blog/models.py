import datetime as dt

from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class BlogPage(Page):
    """ Represents a blog page.

    Basically the blog page will correspond the blog's index page. It should be noted that the
    ``BlogPage`` model inherits from the ``RoutablePageMixin``. Thus blog pages are associated with
    multiple routes allowing to retrieve blog entries by date, month or year.
    """

    description = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Description'),
        help_text=_('This is the description of your blog'))

    header_image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Header image'))

    # The following fields can be used to configure the way the behavior of the blog.
    show_tags = models.BooleanField(default=True, verbose_name=_('Show tags'))

    ###############################
    # EDITOR PANELS CONFIGURATION #
    ###############################

    content_panels = Page.content_panels + [
        FieldPanel('description', classname='full'),
        ImageChooserPanel('header_image'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('show_tags'),
    ]

    ####################################
    # PARENT PAGE / SUBPAGE TYPE RULES #
    ####################################

    subpage_types = ['blog.EntryPage', ]


class EntryPage(Page):
    """ Represents a blog entry page.

    This Page subclass provide a way to define blog entry pages through the Wagtail's admin.
    It defines the basic fields and information that are generally associated with blog pages.
    """

    # Basically a blog entry page is characterized by a body field (the actual content of the blog
    # post), a date and a title (which is provided by the wagtail's Page model).
    body = RichTextField(verbose_name=_('Body'))
    date = models.DateField(verbose_name=_('Post date'), default=dt.datetime.today)

    # A blog entry can be associated with many tags if necessary.
    tags = ClusterTaggableManager(through='blog.TagEntryPage', blank=True)

    ##############################
    # SEARCH INDEX CONFIGURATION #
    ##############################

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    ###############################
    # EDITOR PANELS CONFIGURATION #
    ###############################

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname='full'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    ####################################
    # PARENT PAGE / SUBPAGE TYPE RULES #
    ####################################

    parent_page_types = ['blog.BlogPage']
    subpage_types = []


class TagEntryPage(TaggedItemBase):
    """ Represents a simple tag. """

    content_object = ParentalKey('EntryPage', related_name='entry_tags')
