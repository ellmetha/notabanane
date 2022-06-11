"""
    Blog app config
    ===============

    This module contains the application configuration class - available in the Django app registry.
    For more information on this file, see https://docs.djangoproject.com/en/dev/ref/applications/

"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogAppConfig(AppConfig):
    label = 'blog'
    name = 'main.apps.blog'
    verbose_name = _('Blog')
    default_auto_field = 'django.db.models.AutoField'
