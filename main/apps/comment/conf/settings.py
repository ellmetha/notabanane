"""
    Comment settings
    ================

    This file defines settings that can be overriden in the Django project's settings module.

"""

from django.conf import settings


# The "MAX_LENGTH" setting defines the maximum length allowed for a comment.
MAX_LENGH = getattr(settings, 'COMMENTS_MAX_LENGTH', 1000)
