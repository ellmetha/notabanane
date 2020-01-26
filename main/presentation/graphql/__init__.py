"""
    Project GraphQL schema
    ======================

    This module is the main entrypoint for all the GraphQL types and mutations associated with the
    GraphQL schema of the project.

"""

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from main.apps.blog.shortcuts import get_instagram_media_feed

from .converter import *  # noqa: F401
from .filters import RecipePageFilter
from .types import InstagramMediaType, RecipePageType


class Query(graphene.ObjectType):
    """ Main GraphQL query. """

    recipes = DjangoFilterConnectionField(RecipePageType, filterset_class=RecipePageFilter)
    recent_instagram_medias = graphene.List(InstagramMediaType, required=True)

    def resolve_recent_instagram_medias(self, info):
        """ Returns the recent Instagram medias to showcase in the blog pages. """
        return get_instagram_media_feed()


schema = graphene.Schema(query=Query)
