"""
    Common model factories
    ======================

    This module defines model factories that can be used to create model instances when preparing
    test data.

"""

import factory
from django.conf import settings
from faker import Factory


fake = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    """ Factory class for the user model. """

    username = factory.Sequence(lambda n: fake.user_name() + str(n))
    email = factory.Sequence(lambda n: 'test{0}@example.com'.format(n))

    class Meta:
        model = settings.AUTH_USER_MODEL
