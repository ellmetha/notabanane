"""
    GraphQL binding tags
    ====================

    This module defines templates tags that help converting IDs to GraphQL-specific values such as
    enums.

"""

from django import template

from ..graphql.types.enums.blog import DIETS_ENUM_MAPPING, DISH_TYPES_ENUM_MAPPING


register = template.Library()


@register.filter
def dish_type_enum(dish_type_id):
    """ Returns the dish type enum value corresponding to a specific dish type ID. """
    return {v: k for k, v in DISH_TYPES_ENUM_MAPPING.items()}[dish_type_id]


@register.filter
def diet_enum(diet_id):
    """ Returns the diet enum value corresponding to a specific diet ID. """
    return {v: k for k, v in DIETS_ENUM_MAPPING.items()}[diet_id]
