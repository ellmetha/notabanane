"""
    Comment models
    ==============

    This module defines the models allowing manipulate and store comments data.

"""

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from main.common.db.abstract_models import DatedModel

from .conf import settings as comments_settings


class Comment(DatedModel):
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
    unregistered_author_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_('Email address')
    )
    unregistered_author_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_('Name'))
    unregistered_author_website_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Website')
    )

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

    # The commented object is a generic foreign key, thus allowing any model to have associated
    # comments.
    commented_object_content_type = models.ForeignKey(
        ContentType,
        db_index=True,
        related_name='+',
        on_delete=models.CASCADE,
    )
    commented_object_id = models.CharField(max_length=255, db_index=True)
    commented_object = GenericForeignKey('commented_object_content_type', 'commented_object_id')

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return self.truncated_content

    @property
    def truncated_content(self):
        """ Returns a truncated version of the comment. """
        return Truncator(self.content).chars(64)

    def clean(self):
        """ Validates the comment. """
        super().clean()

        unregistered_author_set = (
            self.unregistered_author_email is not None and
            self.unregistered_author_name is not None
        )

        if self.registered_author_id is None and not unregistered_author_set:
            raise ValidationError(
                _(
                    'A comment must be associated with either a registered user or an unregistered '
                    'user'
                )
            )
        elif self.registered_author_id is not None and unregistered_author_set:
            raise ValidationError(
                _(
                    'A comment cannot be associated with both a registered user and an '
                    'unregistered user'
                )
            )
