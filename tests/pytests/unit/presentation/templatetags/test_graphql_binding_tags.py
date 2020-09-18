from main.apps.blog.models import RecipePage
from main.presentation.graphql.types.enums.blog import DishType
from main.presentation.templatetags.graphql_binding_tags import dish_type_enum


def test_dish_type_enum_filter_works_as_expected():
    assert dish_type_enum(RecipePage.DISH_TYPE_MAIN_COURSE) == DishType.MAIN_COURSE.name
