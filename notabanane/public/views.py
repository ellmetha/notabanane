"""
    Top-level views
    ===============

    This module defines views associated with "top-level" pages.

"""

from django.views.generic import FormView

from .forms import ContactForm


class ContactFormView(FormView):
    """ Allows users to send contact messages to the site owners. """

    form_class = ContactForm
    template_name = 'contact.html'
