"""
    Comment model factories
    =======================

    This module defines model factories that can be used to create model instances when preparing
    test data.

"""

import factory
import factory.django
from faker import Factory

from ..models import Comment


fake = Factory.create()


class CommentFactory(factory.django.DjangoModelFactory):
    """ Factory class for the ``Comment`` model. """

    unregistered_author_email = factory.LazyFunction(fake.email)
    unregistered_author_name = factory.LazyFunction(fake.first_name)

    content = factory.LazyAttribute(lambda o: fake.sentences(nb=3, ext_word_list=None))

    class Meta:
        model = Comment
