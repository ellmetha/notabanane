"""
    Project GraphQL schema
    ======================

    This module is the main entrypoint for all the GraphQL types and mutations associated with the
    GraphQL schema of the project.

"""

import graphene
from graphene import relay

from main.apps.blog.models import RecipePage

from .types import RecipePageConnection


class Query(graphene.ObjectType):
    """ Main GraphQL query. """

    recipes = relay.ConnectionField(RecipePageConnection)

    def resolve_recipes(self, info, **kwargs):
        """ Returns a queryset of all live recipes. """
        return RecipePage.objects.live().all()


schema = graphene.Schema(query=Query)
