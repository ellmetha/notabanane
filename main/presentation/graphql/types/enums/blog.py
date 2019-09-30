"""
    Blog GraphQL enums
    ==================

    This module defines GraphQL enums associated with models and entities of the blog application.

"""

import graphene

from main.apps.blog.models import RecipePage
from main.common.text import replace


DISH_TYPES_ENUM_MAPPING = {
    replace(t[0], (('-', '_'), ('+', '_'))).upper(): t[0] for t in RecipePage.DISH_TYPE_CHOICES
}

DishType = graphene.Enum('DishType', list(DISH_TYPES_ENUM_MAPPING.items()))
