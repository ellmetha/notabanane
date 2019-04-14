"""
    Production Django settings
    ==========================

    This file imports the ``base`` settings and can add or modify previously defined settings to
    alter the configuration of the application for production environments.

    For more information on this file, see https://docs.djangoproject.com/en/dev/topics/settings/
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/dev/ref/settings/

"""

from .base import *  # noqa: F403


# APP CONFIGURATION
# ------------------------------------------------------------------------------

INSTALLED_APPS += (  # noqa: F405
    'raven.contrib.django.raven_compat',
)


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------

MIDDLEWARE += ('django.middleware.security.SecurityMiddleware', )  # noqa: F405


# CSRF CONFIGURATION
# ------------------------------------------------------------------------------

# We want to ensure that CSRF cookies are only ever sent over HTTPS (this should already be the case
# because we are systematically redirecting HTTP to HTTPS using a specific Nginx directive or a
# Cloudflare page rule).
# See: https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-CSRF_COOKIE_SECURE
CSRF_COOKIE_SECURE = True


# SESSION CONFIGURATION
# ------------------------------------------------------------------------------

# We want to ensure that session cookies are only ever sent over HTTPS (this should already be the
# case because we are systematically redirecting HTTP to HTTPS using a specific Nginx directive or a
# Cloudflare page rule).
# See: https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-SESSION_COOKIE_SECURE
SESSION_COOKIE_SECURE = True


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECURE_HSTS_SECONDS
SECURE_HSTS_SECONDS = 31536000

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECURE_HSTS_INCLUDE_SUBDOMAINS  # noqa
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


# RAVEN CONFIGURATION
# ------------------------------------------------------------------------------

RAVEN_CONFIG = {
    'dsn': get_envsetting('SENTRY_DSN'),  # noqa: F405
}
