"""
    Top-level views
    ===============

    This module defines views associated with "top-level" pages.

"""

from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from graphene_django.views import GraphQLView as BaseGraphQLView

from .forms import ContactForm


class ContactFormView(FormView):
    """ Allows users to send contact messages to the site owners. """

    form_class = ContactForm
    template_name = 'contact.html'

    def form_valid(self, form):
        """ Handles a valid form. """
        form.send_contact_email(self.request)
        messages.success(self.request, _('Contact message sent successfully'))
        return super().form_valid(form)

    def get_success_url(self):
        """ Returns the URL to redirect the user to upon valid form processing. """
        return '/'


class GraphQLView(BaseGraphQLView):
    """ Allows to interact with the main GraphQL schema. """

    graphiql = settings.DEBUG
