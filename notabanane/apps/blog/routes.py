"""
    Blog routes
    ===========

    This module defines "routes" for blog pages. A "route" is a concept introduced by the Wagtail
    CMS allowing to define multiple sub-urls for a page.

"""

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page


class BlogRoutes(RoutablePageMixin):
    """ Defines the main "routes" associated with a ``BlogPage`` instance. """

    @route(r'^category/(?P<category>[-\w]+)/$')
    def entries_by_category(self, request, category, *args, **kwargs):
        self.filter_type = 'category'
        self.filter_value = category
        self.entries = self.get_entries().filter(entry_categories__category__slug=category)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def entries_list(self, request, *args, **kwargs):
        self.entries = self.get_entries()
        return Page.serve(self, request, *args, **kwargs)
