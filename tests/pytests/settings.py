import os


TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ['ENVSETTINGS_FILEPATH'] = os.path.join(TEST_ROOT, '.env.json')


# PROJECT CONFIGURATION
# ------------------------------------------------------------------------------

from notabanane_project.settings.base import *  # noqa, isort:skip


# TESTS-SPECIFIC CONFIGURATION
# ------------------------------------------------------------------------------

MEDIA_ROOT = os.path.join(TEST_ROOT, '_testdata/media/')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
