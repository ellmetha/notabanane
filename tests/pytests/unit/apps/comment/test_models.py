import pytest
from django.utils.text import Truncator

from main.apps.comment.test.factories import CommentFactory
from main.common.test.factories import UserFactory


@pytest.mark.django_db
class TestComment:
    def test_can_return_a_truncated_version_of_the_content(self):
        comment = CommentFactory.create(
            content='t' * 400,
            commented_object=UserFactory.create()
        )
        assert comment.truncated_content == Truncator(comment.content).chars(64)
