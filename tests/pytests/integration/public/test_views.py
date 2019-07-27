import unittest.mock

import pytest
from captcha.client import RecaptchaResponse
from django.conf import settings
from django.core import mail
from django.urls import reverse
from wagtail.core.models import Site

from main.apps.blog.test.factories import BlogPageFactory
from main.common.test.factories import UserFactory


@pytest.mark.django_db
class TestContactFormView:
    @pytest.fixture(autouse=True)
    def setup_wagtail_site(self):
        self.owner = UserFactory.create()
        self.blog_page = BlogPageFactory.create(owner=self.owner)
        self.site = Site.objects.create(
            hostname='localhost',
            site_name='Test site',
            root_page=self.blog_page,
            is_default_site=True
        )

    def test_browsing_works(self, client):
        response = client.get(reverse('contact'))
        assert response.status_code == 200

    @unittest.mock.patch('captcha.fields.client.submit')
    def test_triggers_the_sending_of_a_contact_email(self, mocked_submit, client):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)

        post_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'subject': 'Contact',
            'message': 'Hello',
            'g-recaptcha-response': 'PASSED',
        }
        response = client.post(reverse('contact'), post_data, follow=False)
        assert response.status_code == 302
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to[0] == settings.PROJECT_CONTACT_EMAIL
