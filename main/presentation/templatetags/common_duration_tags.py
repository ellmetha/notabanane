"""
    Common duration template tags
    =============================

    This module defines common template tags allowing to perform operations related to durations.

"""

import isodate
from babel.dates import format_timedelta
from django import template
from django.utils.translation import get_language


register = template.Library()


@register.filter
def duration(timedelta):
    """ Formats a time delta to a human-friendly output. """
    return format_timedelta(timedelta, locale=get_language())


@register.filter
def iso8601(timedelta):
    """ Formats a time delta to a the ISO 8601 format. """
    return isodate.duration_isoformat(timedelta)
