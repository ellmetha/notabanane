"""
    Blog application settings
    =========================

    This file defines settings that can be overriden in the Django project's settings module.

"""

from django.conf import settings


INSTAGRAM_ACCOUNT_ID = getattr(settings, 'BLOG_INSTAGRAM_ACCOUNT_ID', '')
INSTAGRAM_ACCESS_TOKEN = getattr(settings, 'BLOG_INSTAGRAM_ACCESS_TOKEN', '')
