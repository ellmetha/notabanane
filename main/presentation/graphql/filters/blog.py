"""
    Blog GraphQL filters
    ====================

    This module defines GraphQL filters corresponding to model and entities of the blog application.

"""

import django_filters

from main.apps.blog.models import RecipePage

from ..types.enums import DIETS_ENUM_MAPPING, DISH_TYPES_ENUM_MAPPING, SEASONS_ENUM_MAPPING


class RecipePageFilter(django_filters.FilterSet):
    """ Defines filter for recipe pages. """

    dish_types = django_filters.MultipleChoiceFilter(
        choices=list(DISH_TYPES_ENUM_MAPPING.items()),
        method='filter_dish_types',
    )

    seasons = django_filters.MultipleChoiceFilter(
        choices=list(SEASONS_ENUM_MAPPING.items()),
        method='filter_seasons',
    )

    diets = django_filters.MultipleChoiceFilter(
        choices=list(DIETS_ENUM_MAPPING.items()),
        method='filter_diets',
    )

    class Meta:
        model = RecipePage
        fields = ('dish_types', 'seasons', 'diets')

    def filter_dish_types(self, qs, field_name, values):
        """ Filters the queryset from a list of possible dish types. """
        mapped_values = [DISH_TYPES_ENUM_MAPPING[v] for v in values]
        return qs.filter(dish_types__overlap=mapped_values) if mapped_values else qs

    def filter_seasons(self, qs, field_name, values):
        """ Filters the queryset from a list of possible seasons. """
        mapped_values = [SEASONS_ENUM_MAPPING[v] for v in values]
        return qs.filter(seasons__overlap=mapped_values) if mapped_values else qs

    def filter_diets(self, qs, field_name, values):
        """ Filters the queryset from a list of possible diets. """
        mapped_values = [DIETS_ENUM_MAPPING[v] for v in values]
        return qs.filter(diets__overlap=mapped_values) if mapped_values else qs
