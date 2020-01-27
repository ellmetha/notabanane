"""
    Blog shortcuts
    ==============

    This module provides shortcut functions allowing to manipulate and check data related to the
    blog application.

"""

import facebook
from django.core.cache import cache

from main.common.cache.constants import SHORT_TTL

from .conf import settings as blog_settings


def get_instagram_media_feed(limit=8):
    """ Returns the Instagram media feed associated with the blog application. """
    cache_key = f'instagram-media-feed-{limit}-limit'
    media_feed = cache.get(cache_key)

    if media_feed is None:
        graph = facebook.GraphAPI(access_token=blog_settings.INSTAGRAM_ACCESS_TOKEN)
        media_feed = graph.get_object(
            id=f'{blog_settings.INSTAGRAM_ACCOUNT_ID}/media',
            fields='media_url,permalink',
            limit=limit
        )['data']
        cache.set(cache_key, media_feed, 10 * SHORT_TTL)

    return media_feed
