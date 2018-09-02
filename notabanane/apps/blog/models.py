"""
    Blog models
    ===========

    This module defines the main models associated with the blog application. Most of them make use
    of the functionalities provided by Wagtail.

"""

import datetime as dt

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from treebeard.al_tree import AL_Node
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .routes import BlogRoutes


class BlogPage(BlogRoutes, Page):
    """ Represents a blog page.

    Basically the blog page will correspond the blog's index page. It should be noted that the
    ``BlogPage`` model inherits from the ``RoutablePageMixin``. Thus blog pages are associated with
    multiple routes allowing to retrieve blog entries by date, month or year.

    """

    description = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Description'),
        help_text=_('This is the description of your blog'),
    )

    header_image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Header image'),
        help_text=_(
            'Default header image used if the featured article does not provide any header image'
        ),
    )

    # The following fields can be used to configure the behavior of the blog.
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

    def get_context(self, request):
        """ Returns a dictionary of variables to bind into the template. """
        # Update context to include only published posts, ordered by reverse publication dates.
        context = super(BlogPage, self).get_context(request)
        paginator = Paginator(self.entries, 12)
        page = request.GET.get('page')
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            blogpages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            blogpages = paginator.page(paginator.num_pages)
        context['blogpages'] = blogpages

        # Includes the featured article (if any) into the context.
        context['featured_article'] = self.entries.first()

        # Includes the categories into the context.
        context['categories'] = Category.objects.filter(parent__isnull=True).order_by('name')

        # Includes filter-related values into the context.
        context['filter_type'] = getattr(self, 'filter_type', None)
        context['filter_value'] = getattr(self, 'filter_value', None)

        return context

    def get_entries(self):
        """ Returns all the live entries of the blog. """
        return (
            EntryPage.objects.select_related('header_image').live().order_by('-first_published_at')
        )


class EntryPage(Page):
    """ Represents a blog entry page.

    This Page subclass provide a way to define blog entry pages through the Wagtail's admin.
    It defines the basic fields and information that are generally associated with blog pages.

    """

    # Basically a blog entry page is characterized by a body field (the actual content of the blog
    # post), a date and a title (which is provided by the wagtail's Page model).
    body = RichTextField(verbose_name=_('Body'))
    date = models.DateField(verbose_name=_('Post date'), default=dt.datetime.today)

    # A blog entry page can have an header image that'll be used when rendering the blog post. It'll
    # also be displayed if the blog post is featured in the home page.
    header_image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Header image'),
        help_text=_(
            'Header image displayed when rendering the article or if the article is featured on '
            'the home page'
        ),
    )

    # A blog entry can be associated with many categories if necessary.
    categories = models.ManyToManyField(
        'blog.Category', through='blog.CategoryEntryPage', blank=True,
    )

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
        ImageChooserPanel('header_image'),
        InlinePanel('entry_categories', label=_('Categories')),
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


@register_snippet
class Category(AL_Node):
    """ Represents a blog category. """

    # A category is basically defined by a name, a slug (that will be used in URLs) and a
    # description.
    name = models.CharField(max_length=80, unique=True, verbose_name=_('Category name'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))

    # A tree of categories can be created using the parent relation (thus allowing to build
    # adjacency list trees).
    parent = models.ForeignKey(
        'self', blank=True, null=True, db_index=True, related_name='children_set',
        on_delete=models.SET_NULL, verbose_name=_('Parent category'),
    )

    node_order_by = ['name', ]

    class Meta:
        ordering = ['name', ]
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class CategoryEntryPage(models.Model):
    """ Represents a category entry page. """

    category = models.ForeignKey(
        Category, related_name='+', on_delete=models.CASCADE, verbose_name=_('Category'),
    )
    page = ParentalKey('EntryPage', related_name='entry_categories')

    ###############################
    # EDITOR PANELS CONFIGURATION #
    ###############################

    panels = [
        FieldPanel('category'),
    ]
