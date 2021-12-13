"""
    Common middlewares
    ==================

    This module exposes common middleware classes.

"""

from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().partition(":")[0]
        if host.startswith('www.'):
            return HttpResponsePermanentRedirect("{request.scheme}://{host[4:]}/" + request.path)
        else:
            return self.get_response(request)
