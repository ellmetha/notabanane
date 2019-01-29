"""
    Blog routes
    ===========

    This module defines "routes" for blog pages. A "route" is a concept introduced by the Wagtail
    CMS allowing to define multiple sub-urls for a page.

"""

from django.db.models import Q
from django.shortcuts import redirect
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
            Q(entrypage__entry_categories__category__slug=category) |
            Q(entrypage__entry_categories__category__parent__slug=category) |
            Q(recipepage__recipe_categories__category__slug=category) |
            Q(recipepage__recipe_categories__category__parent__slug=category)
        )
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def entries_list(self, request, *args, **kwargs):
        """ Generates a page containing all the entries of the blog. """
        self.featured_entries = self.get_entries()[:3]
        self.latest_recipes = self.get_recipes()[:3]
        self.latest_articles = self.get_articles()[:3]
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def entries_search(self, request, *args, **kwargs):
        """ Generates a page containing all the entries associated with a specific search. """
        self.search_query = request.GET.get('q', None)
        if self.search_query:
            self.filter_type = 'search'
            self.filter_value = self.search_query
            self.entries = self.get_entries().search(self.search_query)
            Query.get(self.search_query).add_hit()
            return Page.serve(self, request, *args, **kwargs)
        return redirect(self.url)
