"""
    Blog routes
    ===========

    This module defines "routes" for blog pages. A "route" is a concept introduced by the Wagtail
    CMS allowing to define multiple sub-urls for a page.

"""

from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.search.models import Query


class BlogRoutes(RoutablePageMixin):
    """ Defines the main "routes" associated with a ``BlogPage`` instance. """

    @route(r'^$')
    def entries_list(self, request, *args, **kwargs):
        """ Generates a home page containing relevant entries of the blog. """
        self.latest_recipes = self.get_recipes()[:6]
        self.latest_article = self.get_articles().first()
        return Page.serve(self, request, *args, **kwargs)

    @route(_(r'^search/$'))
    def entries_search(self, request, *args, **kwargs):
        """ Generates a page containing all the entries associated with a specific search. """
        self.search_query = request.GET.get('q', None)
        response = None
        if self.search_query:
            self.filter_type = 'search'
            self.filter_value = self.search_query
            self.entries = self.get_entries().search(self.search_query, operator='or')
            Query.get(self.search_query).add_hit()
            response = Page.serve(self, request, *args, **kwargs)
        return response or redirect(self.url)

    @route(_(r'^articles/$'))
    def articles_list(self, request, *args, **kwargs):
        """ Generates a page containing all the articles of the blog. """
        self.filter_type = 'pagetype'
        self.filter_value = 'article'
        self.entries = self.get_articles()
        return Page.serve(self, request, *args, **kwargs)

    @route(_(r'^recipes/$'))
    def recipes_list(self, request, *args, **kwargs):
        """ Generates a page containing all the recipes of the blog. """
        self.filter_type = 'pagetype'
        self.filter_value = 'recipe'
        return Page.serve(self, request, *args, **kwargs)
