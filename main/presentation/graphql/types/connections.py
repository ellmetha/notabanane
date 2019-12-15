"""
    Connection GraphQL types
    ========================

    This module defines common GraphQL types corresponding to connections.

"""

import graphene


class ExtendedConnection(graphene.Connection, abstract=True):
    """ Defines an extended connection type that exposes the total count of results. """

    total_count = graphene.Int()

    def resolve_total_count(self, info, **kwargs):
        """ Returns the total count for the considered set. """
        return self.length
