"""
    E-mail common helpers
    =====================

    This file defines an ``Email`` class that wraps the regular 'email' function provided by Django
    in order to smoothly handle text/html e-mail sending.

"""

import logging

import html2text
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.encoding import force_text

from .context_managers import switch_language


logger = logging.getLogger(__file__)


class Email:
    """ A simple wrapper around the regular Django email sending implementation.

    It allows to manipulate an e-mail sending as an object and it also generates a text version of
    an e-mail if only the HTML version is provided.

    """

    def __init__(
        self,
        recipient,
        html_template,
        text_template=None,
        subject='',
        from_email=None,
        subject_template=None,
        extra_context=None,
        language=None
    ):
        self.recipient = recipient
        self.recipient = [self.recipient, ] if isinstance(self.recipient, str) else self.recipient
        self.language = language if language else translation.get_language()
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        with switch_language(self.language):
            self.context = {}
            self.context.update(extra_context or {})
            self.subject = (
                self._render_template(subject_template).strip() if subject_template else
                force_text(subject)
            )
            self.html_message = self._render_template(html_template)
            self.text_message = (
                self._render_template(text_template) if text_template else
                html2text.html2text(self.html_message)
            )

    def send(self):
        msg = EmailMultiAlternatives(
            self.subject,
            self.text_message,
            self.from_email,
            self.recipient
        )
        msg.attach_alternative(self.html_message, 'text/html')
        try:
            msg.send()
        except Exception:
            # NOTE: the exception here depends on the considered email backend.
            logger.error(f'Failed to send email message to {self.recipient}', exc_info=True)

    def _render_template(self, template_name):
        return render_to_string(template_name, self.context)
