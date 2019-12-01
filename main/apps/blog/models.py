"""
    Blog models
    ===========

    This module defines the main models associated with the blog application. Most of them make use
    of the functionalities provided by Wagtail.

"""

import datetime as dt

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from main.common.db.models.fields import ChoiceArrayField
from main.common.widgets import ShortDurationSelectWidget

from .routes import BlogRoutes


class BlogPage(BlogRoutes, Page):
    """ Represents a blog page.

    Basically the blog page will correspond to the blog's index page. It should be noted that the
    ``BlogPage`` model inherits from the ``RoutablePageMixin``. Thus blog pages are associated with
    multiple routes allowing to retrieve blog entries by date, month or year.

    """

    description = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Description'),
        help_text=_('This is the description of your blog'),
    )

    ###############################
    # EDITOR PANELS CONFIGURATION #
    ###############################

    content_panels = Page.content_panels + [
        FieldPanel('description', classname='full'),
    ]

    ####################################
    # PARENT PAGE / SUBPAGE TYPE RULES #
    ####################################

    subpage_types = ['blog.ArticlePage', 'blog.RecipePage', 'blog.SimplePage']

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

    def get_context(self, request, *args, **kwargs):
        """ Returns a dictionary of variables to bind into the template. """
        context = super().get_context(request, *args, **kwargs)

        # Inserts the top-level blog page into the context; that is 'self' in that case.
        context['blog_page'] = self

        # Update context to include only published posts, ordered by reverse publication dates. The
        # list of entries (if any) is paginated.
        if hasattr(self, 'entries'):
            paginator = Paginator(self.entries, 12)
            page = request.GET.get('page', 1)
            try:
                paginated_entries = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                paginated_entries = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                paginated_entries = paginator.page(paginator.num_pages)  # type: ignore
            context['paginated_entries'] = paginated_entries

        # Includes filter-related values into the context.
        context['filter_type'] = getattr(self, 'filter_type', None)
        context['filter_value'] = getattr(self, 'filter_value', None)

        return context  # type: ignore

    def get_entries(self):
        """ Returns all the live entries of the blog. """
        return (
            self.get_children()
            .prefetch_related('articlepage', 'recipepage')
            .select_related('articlepage__header_image', 'recipepage__header_image')
            .live()
        )

    def get_articles(self):
        """ Returns all the live articles of the blog ordered by reverse publication date. """
        return (
            ArticlePage.objects
            .select_related('header_image')
            .live()
            .order_by('-date')
        )

    def get_recipes(self):
        """ Returns all the live articles of the blog ordered by reverse publication date. """
        return (
            RecipePage.objects.select_related('header_image').live().order_by('-date')
        )


class ArticlePage(Page):
    """ Represents a blog article page.

    This Page subclass provide a way to define blog article pages through the Wagtail's admin.
    It defines the basic fields and information that are generally associated with blog pages.

    """

    # Basically a blog article page is characterized by a body field (the actual content of the blog
    # post), a date and a title (which is provided by the wagtail's Page model).
    body = RichTextField(verbose_name=_('Introduction'))
    date = models.DateField(verbose_name=_('Post date'), default=dt.datetime.today)

    # A blog article page can have an header image that'll be used when rendering the blog post.
    # It'll also be displayed if the blog post is featured in the home page.
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Header image'),
        help_text=_('Header image displayed when rendering the page.'),
    )

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
    ]

    ####################################
    # PARENT PAGE / SUBPAGE TYPE RULES #
    ####################################

    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def get_context(self, request, *args, **kwargs):
        """ Returns a dictionary of variables to bind into the template. """
        context = super().get_context(request, *args, **kwargs)

        # Inserts the top-level blog page into the context.
        context['blog_page'] = self.get_parent().specific

        return context


class RecipePage(Page):
    """ Represents a blog recipe page.

    This Page subclass provide a way to define blog recipe pages through the Wagtail's admin.
    It defines the basic fields and information that are generally associated with recipes showcased
    in the context of a blog application.

    """

    # Like any blog article, a recipe has a date and a title. But it has no body: instead it only
    # has an introduction field to contain a small content to be displayed before the recipe
    # details.
    introduction = RichTextField(verbose_name=_('Introduction'))
    date = models.DateField(verbose_name=_('Post date'), default=dt.datetime.today)

    # A blog recipe page can have an header image that'll be used when rendering the blog post.
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Header image'),
        help_text=_('Header image displayed when rendering the page.'),
    )

    # The following fields define basic meta-information regarding a recipe (times, yiels, etc).
    preparation_time = models.DurationField(
        blank=True,
        null=True,
        verbose_name=_('Preparation time'),
    )
    cook_time = models.DurationField(
        blank=True,
        null=True,
        verbose_name=_('Cook time'),
    )
    fridge_time = models.DurationField(
        blank=True,
        null=True,
        verbose_name=_('Fridge time'),
    )
    rest_time = models.DurationField(
        blank=True,
        null=True, verbose_name=_('Rest time'),
    )
    recipe_yield = models.CharField(
        max_length=127,
        blank=True,
        verbose_name=_('Yield'),
        help_text=_('Enter a yield indication such as "4 persons", "3 servings", etc.'),
    )

    # A recipe is defined by at least one dish type.
    DISH_TYPE_APPETIZERS = 'appetizers'
    DISH_TYPE_BEVERAGES = 'beverages'
    DISH_TYPE_BREAKFAST = 'breakfast'
    DISH_TYPE_DESSERTS = 'desserts'
    DISH_TYPE_MAIN_COURSE = 'main-course'
    DISH_TYPE_SAUCES_SALAD_DRESSINGS = 'sauces+salad-dressings'
    DISH_TYPE_SOUPS = 'soups'
    DISH_TYPE_VEGETABLES_SALADS = 'vegetables+salads'
    DISH_TYPE_CHOICES = (
        (DISH_TYPE_APPETIZERS, _('Appetizers')),
        (DISH_TYPE_BEVERAGES, _('Beverages')),
        (DISH_TYPE_BREAKFAST, _('Breakfast')),
        (DISH_TYPE_DESSERTS, _('Desserts')),
        (DISH_TYPE_MAIN_COURSE, _('Main course')),
        (DISH_TYPE_SAUCES_SALAD_DRESSINGS, _('Sauces and salad dressings')),
        (DISH_TYPE_SOUPS, _('Soups')),
        (DISH_TYPE_VEGETABLES_SALADS, _('Vegetables and salads')),
    )
    dish_types = ChoiceArrayField(
        models.CharField(max_length=64, choices=DISH_TYPE_CHOICES),
        size=3,
        default=list,
        verbose_name=_('Dish types')
    )

    # A recipe is associated with at least one season.
    SEASON_WINTER = 'winter'
    SEASON_SPRING = 'spring'
    SEASON_SUMMER = 'summer'
    SEASON_AUTUMN = 'autumn'
    SEASON_CHOICES = (
        (SEASON_WINTER, _('Winter')),
        (SEASON_SPRING, _('Spring')),
        (SEASON_SUMMER, _('Summer')),
        (SEASON_AUTUMN, _('Autumn')),
    )
    seasons = ChoiceArrayField(
        models.CharField(max_length=6, choices=SEASON_CHOICES),
        size=4,
        default=list,
        verbose_name=_('Seasons')
    )

    ##############################
    # SEARCH INDEX CONFIGURATION #
    ##############################

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.FilterField('date'),
    ]

    ###############################
    # EDITOR PANELS CONFIGURATION #
    ###############################

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname='full'),
        FieldPanel('dish_types', widget=CheckboxSelectMultiple),
        FieldPanel('seasons', widget=CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel('preparation_time', widget=ShortDurationSelectWidget),
                FieldPanel('cook_time', widget=ShortDurationSelectWidget),
                FieldPanel('fridge_time', widget=ShortDurationSelectWidget),
                FieldPanel('rest_time', widget=ShortDurationSelectWidget),
                FieldPanel('recipe_yield'),
            ],
            heading=_('Recipe information'),
        ),
        InlinePanel('ingredients_sections', label=_('Recipe ingredients sections')),
        InlinePanel('instructions_sections', label=_('Recipe instructions sections')),
        ImageChooserPanel('header_image'),
        FieldPanel('date'),
    ]

    ####################################
    # PARENT PAGE / SUBPAGE TYPE RULES #
    ####################################

    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    @property
    def verbose_dish_types(self):
        """ Returns verbose names of dish types. """
        dish_types_choices = dict(self.DISH_TYPE_CHOICES)
        return [dish_types_choices[d] for d in self.dish_types]

    def get_context(self, request, *args, **kwargs):
        """ Returns a dictionary of variables to bind into the template. """
        context = super().get_context(request, *args, **kwargs)

        # Inserts the top-level blog page into the context.
        context['blog_page'] = self.get_parent().specific

        return context


class RecipeIngredientsSection(Orderable, ClusterableModel, models.Model):
    """ Represents a section of ingredients of a recipe. """

    page = ParentalKey('RecipePage', related_name='ingredients_sections')

    # An ingredient section is basically defined by a list of ingredients and by an optional label.
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Label'))
    ingredients = models.TextField(
        verbose_name=_('Ingredients'),
        help_text=_(
            'Each new line generates a new numbered ingredient. Blank lines are allowed to '
            'separate ingredients from each others too.'
        ),
    )

    panels = [
        FieldPanel('label'),
        FieldPanel('ingredients'),
    ]

    class Meta:
        ordering = ['sort_order', ]
        verbose_name = _('Recipe ingredients section')
        verbose_name_plural = _('Recipe ingredients sections')

    @property
    def ingredients_list(self):
        """ Returns the list of ingredients as standard list. """
        return [i for i in (self.ingredients or '').splitlines() if i]


class RecipeInstructionsSection(Orderable, ClusterableModel, models.Model):
    """ Represents a section of instructions of a recipe. """

    page = ParentalKey('RecipePage', related_name='instructions_sections')

    # An instruction section is basically defined by a list of instructions and by an optional
    # label.
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Label'))
    instructions = models.TextField(
        verbose_name=_('Instructions'),
        help_text=_(
            'Each new line generates a new numbered instruction. Blank lines are allowed to '
            'separate instructions from each others too.'
        ),
    )

    panels = [
        FieldPanel('label'),
        FieldPanel('instructions'),
    ]

    class Meta:
        ordering = ['sort_order', ]
        verbose_name = _('Recipe instructions section')
        verbose_name_plural = _('Recipe instructions sections')

    @property
    def instructions_list(self):
        """ Returns the list of instructions as a standard list. """
        return [i for i in (self.instructions or '').splitlines() if i]


class SimplePage(Page):
    """ Represents a simple page. """

    # A simple page has a single body field, which degines the actual content of the page.
    body = RichTextField(verbose_name=_('Body'))

    # A simple page can have an header image that'll be used when rendering the page.
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Header image'),
        help_text=_('Header image displayed when rendering the page.'),
    )

    # It is possible to block indexation for a specific page by setting the "noindex" option to
    # true.
    noindex = models.BooleanField(default=False, verbose_name=_('Disable robots indexation'))

    ###############################
    # EDITOR PANELS CONFIGURATION #
    ###############################

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
        ImageChooserPanel('header_image'),
    ]

    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('seo_title'),
                FieldPanel('show_in_menus'),
                FieldPanel('search_description'),
                FieldPanel('noindex'),
            ],
            _('Common page configuration')
        ),
    ]

    ####################################
    # PARENT PAGE / SUBPAGE TYPE RULES #
    ####################################

    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    class Meta:
        verbose_name = _('Simple page')
        verbose_name_plural = _('Simple pages')

    def get_context(self, request, *args, **kwargs):
        """ Returns a dictionary of variables to bind into the template. """
        context = super().get_context(request, *args, **kwargs)

        # Inserts the top-level blog page into the context.
        context['blog_page'] = self.get_parent().specific

        return context

    def get_sitemap_urls(self, request=None):
        """ Returns URLs to include in sitemaps. """
        return [] if self.noindex else super().get_sitemap_urls(request=request)
