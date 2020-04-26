import pytest
from django.core.exceptions import ValidationError
from django.utils.text import Truncator

from main.apps.comment.test.factories import CommentFactory
from main.common.test.factories import UserFactory


@pytest.mark.django_db
class TestComment:
    def test_cannot_validate_a_comment_without_author(self):
        comment = CommentFactory.build(registered_author=None, unregistered_author_email=None)

        with pytest.raises(ValidationError) as excinfo:
            comment.clean()

        expected_msg = (
            'A comment must be associated with either a registered user or an unregistered user'
        )
        assert expected_msg in str(excinfo.value)

    def test_cannot_validate_a_comment_with_both_a_registered_and_unregistered_author(self):
        comment = CommentFactory.build(
            registered_author=UserFactory.create(),
            unregistered_author_email='test@example.com',
            unregistered_author_name='Foo Bar'
        )

        with pytest.raises(ValidationError) as excinfo:
            comment.clean()

        expected_msg = (
            'A comment cannot be associated with both a registered user and an unregistered user'
        )
        assert expected_msg in str(excinfo.value)

    def test_can_return_a_truncated_version_of_the_content(self):
        comment = CommentFactory.create(
            content='t' * 400,
            commented_object=UserFactory.create()
        )
        assert comment.truncated_content == Truncator(comment.content).chars(64)
