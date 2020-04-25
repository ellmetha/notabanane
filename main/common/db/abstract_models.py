"""
    Common abstract models
    ======================

    This module defines common abstract models that can be used with (or combined to) models.

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _


class DatedModel(models.Model):
    """ Represents a model associated with common timestamp columns (created_at / updated_at). """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))

    class Meta:
        abstract = True
