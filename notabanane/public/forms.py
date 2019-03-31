"""
    Top-level forms
    ===============

    This module defines forms associated with "top-level" pages.

"""

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    """ Simple form allowing users to send contact messages to the blog authors. """

    first_name = forms.CharField(max_length=30, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=150, required=True, label=_('Last name'))
    email = forms.EmailField(required=True, label=_('E-mail address'))
    subject = forms.CharField(max_length=150, required=True, label=_('Subject'))
    message = forms.CharField(
        required=True,
        max_length=5000,
        label=_('Your message'),
        widget=forms.Textarea
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
