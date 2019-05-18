"""
    Top-level forms
    ===============

    This module defines forms associated with "top-level" pages.

"""

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _

from main.common.email import Email


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

    def send_contact_email(self, request):
        """ Sends the contact e-mail once the form has been processed and validated. """
        email = Email(
            settings.PROJECT_CONTACT_EMAIL,
            html_template='emails/contact.html',
            subject=_('Contact: {}').format(self.cleaned_data['subject']),
            extra_context={
                'request': request,
                'domain': get_current_site(request).domain,
                'protocol': 'https' if request.is_secure() else 'http',
                'contact': self.cleaned_data
            }
        )
        email.send()
