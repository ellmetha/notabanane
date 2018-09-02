"""
    Blog routes
    ===========

    This module defines "routes" for blog pages. A "route" is a concept introduced by the Wagtail
    CMS allowing to define multiple sub-urls for a page.

"""

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.search.models import Query


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

    @route(r'^search/$')
    def entries_search(self, request, *args, **kwargs):
        """ Generates a page containing all the entries associated with specific search. """
        self.search_query = request.GET.get('q', None)
        self.entries = self.get_entries()
        if self.search_query:
            self.is_search = True
            self.entries = self.get_entries().search(self.search_query)
            Query.get(self.search_query).add_hit()
        return Page.serve(self, request, *args, **kwargs)
