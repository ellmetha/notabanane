import os


TEST_ROOT = os.path.abspath(os.path.dirname(__file__))


# PROJECT CONFIGURATION
# ------------------------------------------------------------------------------

from project.settings.base import *  # noqa, isort:skip


# TESTS-SPECIFIC CONFIGURATION
# ------------------------------------------------------------------------------

MEDIA_ROOT = os.path.join(TEST_ROOT, '_testdata/media/')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
TEMPLATES[0]['DIRS'] += [os.path.join(TEST_ROOT, '_testdata/templates/'), ]  # noqa: F405
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
DEFAULT_FROM_EMAIL = 'test@example.com'
PROJECT_CONTACT_EMAIL = 'test@example.com'
WAGTAILSEARCH_BACKENDS['default']['SEARCH_CONFIG'] = 'french'  # noqa: F405
