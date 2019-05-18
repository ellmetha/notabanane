"""
    Common duration template tags
    =============================

    This module defines common template tags allowing to perform operations related to durations.

"""

from babel.dates import format_timedelta
from django import template
from django.utils.translation import get_language


register = template.Library()


@register.filter
def duration(timedelta):
    """ Formats a time delta to a human-friendly output. """
    return format_timedelta(timedelta, locale=get_language())
