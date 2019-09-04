"""
    Common duration template tags
    =============================

    This module defines common template tags allowing to perform operations related to durations.

"""

import isodate
from django import template
from django.utils.translation import ngettext
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.filter
def duration(timedelta):
    """ Formats a time delta to a human-friendly output. """
    total_seconds = int(timedelta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    if hours and not minutes:
        return ngettext('{} hour', '{} hours', hours).format(hours)
    elif minutes and not hours:
        return ngettext('{} minute', '{} minutes', minutes).format(minutes)

    return _('{hours} {minutes}').format(
        hours=ngettext('{} hour', '{} hours', hours).format(hours),
        minutes=ngettext('{} minute', '{} minutes', minutes).format(minutes)
    )


@register.filter
def iso8601(timedelta):
    """ Formats a time delta to a the ISO 8601 format. """
    return isodate.duration_isoformat(timedelta)
