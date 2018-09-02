"""
    Blog routes
    ===========

    This module defines "routes" for blog pages. A "route" is a concept introduced by the Wagtail
    CMS allowing to define multiple sub-urls for a page.

"""

from django.db.models import Q
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page


class BlogRoutes(RoutablePageMixin):
    """ Defines the main "routes" associated with a ``BlogPage`` instance. """

    @route(r'^category/(?P<category>[-\w]+)/$')
    def entries_by_category(self, request, category, *args, **kwargs):
        """ Generates a page containing all the entries associated with a specific category. """
        self.filter_type = 'category'
        self.filter_value = category
        self.entries = self.get_entries().filter(
            Q(entry_categories__category__slug=category) |
            Q(entry_categories__category__parent__slug=category)
        )
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def entries_list(self, request, *args, **kwargs):
        """ Generates a page containing all the entries of the blog. """
        self.entries = self.get_entries()
        return Page.serve(self, request, *args, **kwargs)
