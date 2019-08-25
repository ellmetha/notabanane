import pytest
from django.conf import settings
from django.core import mail

from main.presentation.forms import ContactForm


@pytest.mark.django_db
class TestContactForm:
    def test_can_trigger_the_sending_of_the_contact_email(self, rf):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'subject': 'Contact',
            'message': 'Hello',
            'g-recaptcha-response': 'PASSED',
        }
        form = ContactForm(form_data)
        form.is_valid()
        form.send_contact_email(rf.get('/'))
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to[0] == settings.PROJECT_CONTACT_EMAIL
