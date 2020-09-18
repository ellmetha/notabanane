from main.apps.blog.models import RecipePage
from main.presentation.graphql.types.enums.blog import Diet, DishType
from main.presentation.templatetags.graphql_binding_tags import diet_enum, dish_type_enum


def test_dish_type_enum_filter_works_as_expected():
    assert dish_type_enum(RecipePage.DISH_TYPE_MAIN_COURSE) == DishType.MAIN_COURSE.name


def test_diet_enum_filter_works_as_expected():
    assert diet_enum(RecipePage.DIET_GLUTEN_FREE) == Diet.GLUTEN_FREE.name
