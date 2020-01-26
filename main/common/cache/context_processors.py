"""
    Common cache-related context processors
    =======================================

    This module provides common context processors related to cache usage.

"""

from . import constants as c


def constants(request):
    """ Returns common cache expiry values.

    This context processor returns some cache expiry values that can be used to perform fragment
    caching in templates. These timeouts can be used to do russian doll caching in templates by
    nesting cache calls with different expirations.

    """

    return {
        'TINY_TTL': c.TINY_TTL,
        'SHORT_TTL': c.SHORT_TTL,
        'MIDDLE_TTL': c.MIDDLE_TTL,
        'LONG_TTL': c.MIDDLE_TTL,
        'FOREVER_TTL': c.FOREVER_TTL,
    }
