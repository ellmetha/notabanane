import unittest.mock

from django.conf import settings
from django.core import mail

from notabanane.common.email import Email


class TestEmail:
    def test_can_send_an_email(self):
        email = Email(
            'test@example.com',
            'emails/hello_world.html',
        )
        email.send()

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to[0] == 'test@example.com'
        assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
        assert mail.outbox[0].subject == ''
        assert 'Hello World!' in mail.outbox[0].body

    def test_can_send_an_email_with_a_specific_text_template(self):
        email = Email(
            'test@example.com',
            'emails/hello_world.html',
            text_template='emails/hello_world.txt',
        )
        email.send()

        assert mail.outbox[0].body == 'Hello World from text!\n'

    def test_can_send_an_email_with_a_specific_subject(self):
        email = Email(
            'test@example.com',
            'emails/hello_world.html',
            subject='Hello World!',
        )
        email.send()

        assert mail.outbox[0].subject == 'Hello World!'

    def test_can_send_an_email_with_a_specific_from_email(self):
        email = Email(
            'test@example.com',
            'emails/hello_world.html',
            from_email='from@example.com',
        )
        email.send()

        assert mail.outbox[0].from_email == 'from@example.com'

    def test_can_send_an_email_with_a_specific_subject_template(self):
        email = Email(
            'test@example.com',
            'emails/hello_world.html',
            subject_template='emails/hello_world.txt',
        )
        email.send()

        assert mail.outbox[0].subject == 'Hello World from text!'

    def test_can_send_an_email_with_an_extra_context(self):
        email = Email(
            'test@example.com',
            'emails/hello_world.html',
            extra_context={'var': 'My variable'},
        )
        email.send()

        assert 'My variable' in mail.outbox[0].body

    def test_can_send_an_email_in_a_specific_language(self):
        email_1 = Email('test@example.com', 'emails/hello_world.html', language='en')
        email_1.send()
        assert 'Current language: en' in mail.outbox[0].body

        email_2 = Email('test@example.com', 'emails/hello_world.html', language='fr')
        email_2.send()
        assert 'Current language: fr' in mail.outbox[1].body

    @unittest.mock.patch('django.core.mail.EmailMultiAlternatives.send')
    @unittest.mock.patch('notabanane.common.email.logger')
    def test_logs_an_error_in_case_of_a_failure(self, mocked_logging, mocked_send):
        mocked_send.side_effect = Exception('Boom!')

        email = Email('test@example.com', 'emails/hello_world.html')
        email.send()

        assert mocked_logging.error.called
