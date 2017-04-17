from django.conf import settings


def webpack(request):
    """ Inserts a Webpack dev server URL into the context. """
    return {'WEBPACK_DEV_SERVER_URL': settings.WEBPACK_DEV_SERVER_URL, } \
        if settings.WEBPACK_DEV_SERVER_STARTED else {}
