"""
    Blog GraphQL types
    ==================

    This module defines GraphQL types corresponding to model and entities of the blog application.

"""

import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from main.apps.blog.models import RecipePage


class RecipePageType(DjangoObjectType):
    """ Defines the GraphQL type of recipe pages. """

    header_image_thumbnail = graphene.String()
    url = graphene.String()

    class Meta:
        model = RecipePage
        interfaces = (relay.Node, )
        fields = ('id', 'title', 'date', 'header_image_url', 'url', )

    def resolve_header_image_thumbnail(self, info):
        """ Returns the thumbnail URL of the header image. """
        return self.header_image.get_rendition('fill-555x312').url

    def resolve_url(self, info):
        """ Returns the URL of the recipe page. """
        return self.url


class RecipePageConnection(relay.Connection):
    """ Defines a Relay connection for the RecipePage type. """

    class Meta:
        node = RecipePageType
