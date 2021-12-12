"""
    Base Django settings
    ====================

    For more information on this file, see https://docs.djangoproject.com/en/dev/topics/settings/
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/dev/ref/settings/

"""

import os
import pathlib

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


# BASE DIRECTORIES
# ------------------------------------------------------------------------------

# Two base directories are considered for this project:
# The PROJECT_PATH corresponds to the path towards the root of this project (the root of the
# repository).
# The INSTALL_PATH corresponds to the path towards the directory where the project's repository
# is present on the filesystem.
# By default INSTALL_PATH has the same than PROJECT_PATH.

PROJECT_PATH = pathlib.Path(__file__).parents[2]
INSTALL_PATH = pathlib.Path(os.environ.get('DJANGO_INSTALL_PATH')) \
    if 'DJANGO_INSTALL_PATH' in os.environ else PROJECT_PATH


# ENVIRONMENT SETTINGS HANDLING
# ------------------------------------------------------------------------------

load_dotenv()

ENVSETTINGS_NIL = object()


def get_envsetting(setting, default=ENVSETTINGS_NIL):
    """ Get the environment setting variable or return explicit exception. """
    try:
        return os.environ[setting]
    except KeyError:
        if default is not ENVSETTINGS_NIL:
            return default
        raise ImproperlyConfigured(f"Set the {setting} environment variable")


# APP CONFIGURATION
# ------------------------------------------------------------------------------

INSTALLED_APPS = (
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.syndication',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',

    # Wagtail apps
    'wagtail.admin',
    'wagtail.contrib.forms',
    'wagtail.contrib.postgres_search',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.core',
    'wagtail.documents',
    'wagtail.embeds',
    'wagtail.images',
    'wagtail.search',
    'wagtail.sites',
    'wagtail.snippets',
    'wagtail.users',

    # Third-party apps
    'anymail',
    'captcha',
    'graphene_django',
    'js_routes',
    'modelcluster',
    'taggit',
    'widget_tweaks',

    # Django's admin app
    'django.contrib.admin',

    # Local apps
    'main.apps.blog',
    'main.common',
    'main.presentation',
)


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)


# DEBUG CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': get_envsetting('DB_ENGINE'),
        'NAME': get_envsetting('DB_NAME'),
        'USER': get_envsetting('DB_USER'),
        'PASSWORD': get_envsetting('DB_PASSWORD'),
        'HOST': get_envsetting('DB_HOST'),
        'PORT': get_envsetting('DB_PORT', ''),
    },
}


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'EST'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'fr'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = get_envsetting('ALLOWED_HOSTS', '').split(',')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#languages
LANGUAGES = (
    ('fr', 'Français'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = (
    str(PROJECT_PATH / 'project' / 'locale'),
)


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_envsetting('SECRET_KEY')


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(PROJECT_PATH / 'main' / 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'main.common.cache.context_processors.constants',
                'project.context_processors.google_analytics',
                'project.context_processors.pinterest',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ]
        },
    },
]


# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(INSTALL_PATH / 'static')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = get_envsetting('STATIC_URL', '/static/')

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(PROJECT_PATH / 'main' / 'static' / 'build'),
    str(PROJECT_PATH / 'main' / 'static'),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-STATICFILES_STORAGE
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(INSTALL_PATH / 'media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'


# FORMS CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/2.2/ref/settings/#form-renderer
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'


# URL CONFIGURATION
# ------------------------------------------------------------------------------

ROOT_URLCONF = 'project.urls'


# ADMIN CONFIGURATION
# ------------------------------------------------------------------------------

# URL of the admin page
ADMIN_URL = get_envsetting('ADMIN_URL')


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = get_envsetting('EMAIL_BACKEND')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = get_envsetting('DEFAULT_FROM_EMAIL')


# ANYMAIL CONFIGURATION
# ------------------------------------------------------------------------------

ANYMAIL = {
    'SENDGRID_API_KEY': get_envsetting('SENDGRID_API_KEY', 'notset'),
}


# WAGTAIL CONFIGURATION
# ------------------------------------------------------------------------------

WAGTAIL_ADMIN_URL = get_envsetting('WAGTAIL_ADMIN_URL')

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
        'SEARCH_CONFIG': 'nb_french',
    }
}

WAGTAIL_SITE_NAME = 'Nota Banane'


# RECAPTCHA CONFIGURATION
# ------------------------------------------------------------------------------

RECAPTCHA_PUBLIC_KEY = get_envsetting('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_envsetting('RECAPTCHA_PRIVATE_KEY')


# GRAPHENE CONFIGURATIOM
# ------------------------------------------------------------------------------

GRAPHENE = {
    'SCHEMA': 'main.presentation.graphql.schema',
    'RELAY_CONNECTION_MAX_LIMIT': 50,
}


# JS ROUTES CONFIGURATION
# ------------------------------------------------------------------------------

JS_ROUTES_INCLUSION_LIST = [
    'graphql',
]


# GOOGLE ANALYTICS CONFIGURATION
# ------------------------------------------------------------------------------

GA_PROPERTY_ID = get_envsetting('GA_PROPERTY_ID', 'notset')


# PINTEREST CONFIGURATION
# ------------------------------------------------------------------------------

PINTEREST_DOMAIN_VERIFICATION_ID = get_envsetting('PINTEREST_DOMAIN_VERIFICATION_ID', 'notset')


# BLOG CONFIGURATION
# ------------------------------------------------------------------------------

BLOG_INSTAGRAM_ACCOUNT_ID = get_envsetting('BLOG_INSTAGRAM_ACCOUNT_ID', 'notset')
BLOG_INSTAGRAM_ACCESS_TOKEN = get_envsetting('BLOG_INSTAGRAM_ACCESS_TOKEN', 'notset')


# PROJECT CONFIGURATION
# ------------------------------------------------------------------------------

PROJECT_CONTACT_EMAIL = get_envsetting('PROJECT_CONTACT_EMAIL')
