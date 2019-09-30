"""
    Project GraphQL schema
    ======================

    This module is the main entrypoint for all the GraphQL types and mutations associated with the
    GraphQL schema of the project.

"""

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .converter import *  # noqa: F401
from .filters import RecipePageFilter
from .types import RecipePageType


class Query(graphene.ObjectType):
    """ Main GraphQL query. """

    recipes = DjangoFilterConnectionField(RecipePageType, filterset_class=RecipePageFilter)


schema = graphene.Schema(query=Query)
