"""
    Comment models
    ==============

    This module defines the models allowing manipulate and store comments data.

"""

from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .conf import settings as comments_settings


class Comment(models.Model):
    """ The comment model. """

    # A comment can be submitted by an authenticated user. If so the information displayed regarding
    # the author of the comment should come from the User object.
    registered_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('Poster'),
    )

    # A comment can also be submitted by an anonymous user who doesn't have a registered account.
    # In that case basic poster information (email, name, website URL) is persisted along with the
    # comment.
    unregistered_author_email = models.EmailField(verbose_name=_('Email address'))
    unregistered_author_name = models.CharField(max_length=30, verbose_name=_('Name'))
    unregistered_author_website_url = models.URLField(verbose_name=_('Website'))

    # The author of a comment can choose whether they want to be notified when responses to their
    # comment are submitted.
    notify_author = models.BooleanField(
        default=False,
        verbose_name=_('Notify author'),
        help_text=_('Define whether the author is notified when responses to the comment are made')
    )

    # The content of the comment is stored in a dedicated text column.
    content = models.TextField(
        validators=[MaxLengthValidator(comments_settings.MAX_LENGH)],
        blank=False,
        verbose_name=_('Content')
    )

    # Some metadata (eg. IP address) can be stored along with the comment.
    ip_address = models.GenericIPAddressField(
        unpack_ipv4=True,
        blank=True,
        null=True,
        verbose_name=_('IP address')
    )

    # Creation dates and modification dates are stored for every comment.
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
