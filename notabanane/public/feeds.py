"""
    Top-level feeds
    ===============

    This module defines global feeds of the application.

"""

from django.contrib.syndication.views import Feed
from django.utils.html import strip_tags
from django.utils.text import Truncator

from notabanane.apps.blog.models import RecipePage


class LatestEntriesFeed(Feed):
    """ Defines latest blog entries feed. """

    link = '/'

    def get_feed(self, obj, request):
        """ Returns the feed. """
        self.blog_page = request.site.root_page.specific
        return super().get_feed(obj, request)

    def title(self, obj):
        """ Returns the title of the feed. """
        return self.blog_page.title

    def description(self, obj):
        """ Returns the description of the feed. """
        return self.blog_page.description

    def items(self):
        """ Returns the items to include in the feed. """
        recipes = self.blog_page.get_recipes()[:50]
        articles = self.blog_page.get_articles()[:50]
        return sorted(list(recipes) + list(articles), key=lambda e: e.date, reverse=True)

    def item_title(self, item):
        """ Returns the title of an item. """
        return item.title

    def item_description(self, item):
        """ Returns the description of an item. """
        description = item.introduction if isinstance(item, RecipePage) else item.body
        return item.search_description or Truncator(strip_tags(description)).chars(150)

    def item_link(self, item):
        """ Returns the link of an item. """
        return item.url

    def item_author_name(self, item):
        """ Returns the author name of an item. """
        return item.owner.first_name or item.owner.username
