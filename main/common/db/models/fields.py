"""
    Common model fields
    ===================

    This module defines common model fields.

"""

from django import forms
from django.contrib.postgres.fields import ArrayField


class ChoiceArrayField(ArrayField):
    """ Allows to store an array of char fields associated with choices. """

    def formfield(self, **kwargs):
        """ Returns the form field associated with the field. """
        defaults = {'form_class': forms.MultipleChoiceField, 'choices': self.base_field.choices}
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)
