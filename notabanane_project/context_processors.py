"""
    Project context processors
    ==========================

    This module defines project-level context processors. These context processors should not
    involve too much logic and operations and should only be related to project's configuration.

"""

from django.conf import settings


def google_analytics(request):
    """ Inserts the Google Analytics-relatd setting values into the context. """
    return {'GA_PROPERTY_ID': settings.GA_PROPERTY_ID, }


def pinterest(request):
    """ Inserts the Pinterest-related setting values into the context. """
    return {'PINTEREST_DOMAIN_VERIFICATION_ID': settings.PINTEREST_DOMAIN_VERIFICATION_ID, }


def webpack(request):
    """ Inserts a Webpack dev server URL into the context. """
    return (
        {'WEBPACK_DEV_SERVER_URL': settings.WEBPACK_DEV_SERVER_URL, }
        if settings.WEBPACK_DEV_SERVER_STARTED else {}
    )
