import pytest

from main.apps.blog.models import RecipePage
from main.apps.blog.test.factories import BlogPageFactory, RecipePageFactory
from main.presentation.graphql.filters import RecipePageFilter


@pytest.mark.django_db
class TestRecipePageFilter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blog_page = BlogPageFactory.create()

    def test_can_filter_by_dish_types(self):
        recipe_page_1 = RecipePageFactory.create(
            parent=self.blog_page,
            dish_types=[RecipePage.DISH_TYPE_APPETIZERS, RecipePage.DISH_TYPE_MAIN_COURSE],
            live=True
        )
        recipe_page_2 = RecipePageFactory.create(  # noqa: F841
            parent=self.blog_page,
            dish_types=[RecipePage.DISH_TYPE_MAIN_COURSE],
            live=True
        )
        recipe_page_3 = RecipePageFactory.create(
            parent=self.blog_page,
            dish_types=[RecipePage.DISH_TYPE_DESSERTS],
            live=True
        )

        qs = RecipePageFilter({'dish_types': ['DESSERTS', 'APPETIZERS']}).qs
        assert set(qs) == {recipe_page_1, recipe_page_3}

    def test_can_filter_by_seasons(self):
        recipe_page_1 = RecipePageFactory.create(
            parent=self.blog_page,
            seasons=[RecipePage.SEASON_AUTUMN, RecipePage.SEASON_WINTER],
            live=True
        )
        recipe_page_2 = RecipePageFactory.create(  # noqa: F841
            parent=self.blog_page,
            seasons=[RecipePage.SEASON_SUMMER],
            live=True
        )
        recipe_page_3 = RecipePageFactory.create(
            parent=self.blog_page,
            seasons=[RecipePage.SEASON_AUTUMN],
            live=True
        )

        qs = RecipePageFilter({'seasons': ['AUTUMN', 'WINTER']}).qs
        assert set(qs) == {recipe_page_1, recipe_page_3}

    def test_can_filter_by_diets(self):
        recipe_page_1 = RecipePageFactory.create(
            parent=self.blog_page,
            diets=[RecipePage.DIET_VEGAN, RecipePage.DIET_VEGETARIAN],
            live=True
        )
        recipe_page_2 = RecipePageFactory.create(  # noqa: F841
            parent=self.blog_page,
            diets=[RecipePage.DIET_VEGETARIAN],
            live=True
        )
        recipe_page_3 = RecipePageFactory.create(
            parent=self.blog_page,
            diets=[RecipePage.DIET_GLUTEN_FREE],
            live=True
        )

        qs = RecipePageFilter({'diets': ['VEGAN', 'GLUTEN_FREE']}).qs
        assert set(qs) == {recipe_page_1, recipe_page_3}
