"""
    Blog GraphQL types
    ==================

    This module defines GraphQL types corresponding to model and entities of the blog application.

"""

import graphene
from django.template.defaultfilters import date
from graphene import relay
from graphene_django.types import DjangoObjectType

from main.apps.blog.models import RecipePage

from .connections import ExtendedConnection
from .enums import DishType


class RecipePageType(DjangoObjectType):
    """ Defines the GraphQL type of recipe pages. """

    dish_types = graphene.List(DishType, required=True)
    header_image_thumbnail = graphene.String(required=True)
    url = graphene.String(required=True)
    formatted_date = graphene.String(required=True)

    class Meta:
        model = RecipePage
        connection_class = ExtendedConnection
        interfaces = (relay.Node, )
        fields = (
            'id',
            'title',
            'date',
            'header_image_url',
            'url',
            'dish_types',
            'formatted_date',
        )
        filter_fields = ('dish_types', )

    @classmethod
    def get_queryset(cls, queryset, info):
        """ Returns the default queryset to use for the RecipePage type. """
        return queryset.select_related('header_image').live().order_by('-date')

    def resolve_formatted_date(self, info):
        """ Returns the formatted date. """
        return date(self.date, 'SHORT_DATE_FORMAT')

    def resolve_header_image_thumbnail(self, info):
        """ Returns the thumbnail URL of the header image. """
        return self.header_image.get_rendition('fill-555x312').url

    def resolve_url(self, info):
        """ Returns the URL of the recipe page. """
        return self.url
