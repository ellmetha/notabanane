"""
    Blog GraphQL types
    ==================

    This module defines GraphQL types corresponding to model and entities of the blog application.

"""

import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from main.apps.blog.models import RecipePage
from main.common.text import replace


DishType = graphene.Enum(
    'DishType',
    [(replace(t[0], (('-', '_'), ('+', '_'))).upper(), t[0]) for t in RecipePage.DISH_TYPE_CHOICES]
)


class RecipePageType(DjangoObjectType):
    """ Defines the GraphQL type of recipe pages. """

    dish_types = graphene.List(DishType, required=True)
    header_image_thumbnail = graphene.String(required=True)
    url = graphene.String(required=True)

    class Meta:
        model = RecipePage
        interfaces = (relay.Node, )
        fields = ('title', 'date', 'header_image_url', 'url', 'dish_types', )
        filter_fields = ()

    def resolve_header_image_thumbnail(self, info):
        """ Returns the thumbnail URL of the header image. """
        return self.header_image.get_rendition('fill-555x312').url

    def resolve_url(self, info):
        """ Returns the URL of the recipe page. """
        return self.url
