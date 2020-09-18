import datetime as dt

import pytest
from django.core.paginator import Page
from django.utils import timezone as tz
from django.utils.translation import activate

from main.apps.blog.models import ArticlePage, RecipePage
from main.apps.blog.test.factories import (
    ArticlePageFactory, BlogPageFactory, RecipeIngredientsSectionFactory,
    RecipeInstructionsSectionFactory, RecipePageFactory, SimplePageFactory
)


@pytest.mark.django_db
class TestBlogPage:
    def test_include_itself_in_generated_context(self, rf):
        blog_page = BlogPageFactory.create()
        context = blog_page.get_context(rf.get('/'))
        assert context['blog_page'] == blog_page

    def test_is_able_to_paginate_attached_entries(self, rf):
        blog_page = BlogPageFactory.create()
        for _ in range(30):
            ArticlePageFactory.create(parent=blog_page)
        setattr(blog_page, 'entries', ArticlePage.objects.all())

        context = blog_page.get_context(rf.get('/', {'page': 2}))

        assert isinstance(context['paginated_entries'], Page)
        assert context['paginated_entries'].number == 2

    def test_return_the_first_page_if_the_page_param_is_not_a_number(self, rf):
        blog_page = BlogPageFactory.create()
        for _ in range(15):
            ArticlePageFactory.create(parent=blog_page)
        setattr(blog_page, 'entries', ArticlePage.objects.all())

        context = blog_page.get_context(rf.get('/', {'page': 'foobar'}))

        assert isinstance(context['paginated_entries'], Page)
        assert context['paginated_entries'].number == 1

    def test_return_the_last_page_if_the_page_param_is_greater_than_the_number_of_pages(self, rf):
        blog_page = BlogPageFactory.create()
        for _ in range(15):
            ArticlePageFactory.create(parent=blog_page)
        setattr(blog_page, 'entries', ArticlePage.objects.all())

        context = blog_page.get_context(rf.get('/', {'page': 42}))

        assert isinstance(context['paginated_entries'], Page)
        assert context['paginated_entries'].number == 2

    def test_include_the_filter_type_and_values_in_the_context_if_they_are_defined(self, rf):
        blog_page = BlogPageFactory.create()
        setattr(blog_page, 'filter_type', 'pagetype')
        setattr(blog_page, 'filter_value', 'article')

        context = blog_page.get_context(rf.get('/', {'page': 42}))

        assert context['filter_type'] == 'pagetype'
        assert context['filter_value'] == 'article'

    def test_include_null_values_for_the_filter_type_and_values_in_the_context_if_they_are_not_defined(self, rf):  # noqa: E501
        blog_page = BlogPageFactory.create()

        context = blog_page.get_context(rf.get('/', {'page': 42}))

        assert context['filter_type'] is None
        assert context['filter_value'] is None

    def test_can_return_its_live_entries(self):
        blog_page = BlogPageFactory.create()

        article_page_1 = ArticlePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=5),
            live=True
        )
        article_page_2 = ArticlePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=4),
            live=True
        )
        article_page_3 = ArticlePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=2),
            live=True
        )
        article_page_4 = ArticlePageFactory.create(parent=blog_page, live=False)  # noqa: F841

        recipe_page_1 = RecipePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=3),
            live=True
        )
        recipe_page_2 = RecipePageFactory.create(parent=blog_page, live=True)
        recipe_page_3 = RecipePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=1),
            live=True
        )
        recipe_page_4 = RecipePageFactory.create(parent=blog_page, live=False)  # noqa: F841

        assert set(blog_page.get_entries()) == {
            recipe_page_1.page_ptr,
            recipe_page_2.page_ptr,
            recipe_page_3.page_ptr,
            article_page_1.page_ptr,
            article_page_2.page_ptr,
            article_page_3.page_ptr,
        }

    def test_can_return_the_live_articles_ordered_by_reversed_publication_dates(self):
        blog_page = BlogPageFactory.create()

        article_page_1 = ArticlePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=2),
            live=True
        )
        article_page_2 = ArticlePageFactory.create(parent=blog_page, live=True)
        article_page_3 = ArticlePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=1),
            live=True
        )
        article_page_4 = ArticlePageFactory.create(parent=blog_page, live=False)  # noqa: F841

        assert list(blog_page.get_articles()) == [article_page_2, article_page_3, article_page_1]

    def test_can_return_the_live_recipes_ordered_by_reversed_publication_dates(self):
        blog_page = BlogPageFactory.create()

        recipe_page_1 = RecipePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=2),
            live=True
        )
        recipe_page_2 = RecipePageFactory.create(parent=blog_page, live=True)
        recipe_page_3 = RecipePageFactory.create(
            parent=blog_page,
            date=tz.now() - dt.timedelta(days=1),
            live=True
        )
        recipe_page_4 = RecipePageFactory.create(parent=blog_page, live=False)  # noqa: F841

        assert list(blog_page.get_recipes()) == [recipe_page_2, recipe_page_3, recipe_page_1]


@pytest.mark.django_db
class TestArticlePage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blog_page = BlogPageFactory.create()

    def test_inserts_its_parent_page_into_the_context(self, rf):
        article_page = ArticlePageFactory.create(parent=self.blog_page)
        context = article_page.get_context(rf.get('/my-article'))
        assert context['blog_page'] == self.blog_page


@pytest.mark.django_db
class TestRecipePage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blog_page = BlogPageFactory.create()

    def test_inserts_its_parent_page_into_the_context(self, rf):
        recipe_page = RecipePageFactory.create(parent=self.blog_page)
        context = recipe_page.get_context(rf.get('/my-recipe'))
        assert context['blog_page'] == self.blog_page

    def test_can_return_a_list_of_diets_tuples(self):
        activate('en')
        recipe_page = RecipePageFactory.create(
            parent=self.blog_page,
            diets=[RecipePage.DIET_GLUTEN_FREE]
        )
        assert recipe_page.diets_tuples == [(RecipePage.DIET_GLUTEN_FREE, 'Gluten free')]

    def test_can_return_a_list_of_dish_types_tuples(self):
        activate('en')
        recipe_page = RecipePageFactory.create(parent=self.blog_page)
        assert recipe_page.dish_types_tuples == [(RecipePage.DISH_TYPE_MAIN_COURSE, 'Main course')]

    def test_can_return_a_list_of_verbose_versions_of_dish_types(self):
        activate('en')
        recipe_page = RecipePageFactory.create(parent=self.blog_page)
        assert recipe_page.verbose_dish_types == ['Main course']


@pytest.mark.django_db
class TestSimplePage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blog_page = BlogPageFactory.create()

    def test_inserts_its_parent_page_into_the_context(self, rf):
        simple_page = SimplePageFactory.create(parent=self.blog_page)
        context = simple_page.get_context(rf.get('/my-page'))
        assert context['blog_page'] == self.blog_page

    def test_does_not_include_an_entry_in_the_sitemaps_if_it_has_the_noindex_flag(self):
        simple_page = SimplePageFactory.create(parent=self.blog_page, noindex=True)
        assert simple_page.get_sitemap_urls() == []


@pytest.mark.django_db
class TestRecipeIngredientsSection:
    @pytest.fixture(autouse=True)
    def setup(self):
        blog_page = BlogPageFactory.create()
        self.recipe_page = RecipePageFactory.create(parent=blog_page)

    def test_can_return_its_list_of_ingredients(self):
        recipe_page_ingredients_section = RecipeIngredientsSectionFactory.create(
            page=self.recipe_page,
            label='Ingredients',
            ingredients='Ingredient 1\nIngredient 2\n\nIngredient 3\nIngredient 4\n\n\n'
        )
        assert recipe_page_ingredients_section.ingredients_list == [
            'Ingredient 1',
            'Ingredient 2',
            'Ingredient 3',
            'Ingredient 4',
        ]


@pytest.mark.django_db
class TestRecipeInstructionsSection:
    @pytest.fixture(autouse=True)
    def setup(self):
        blog_page = BlogPageFactory.create()
        self.recipe_page = RecipePageFactory.create(parent=blog_page)

    def test_can_return_its_list_of_instructions(self):
        recipe_page_instructions_section = RecipeInstructionsSectionFactory.create(
            page=self.recipe_page,
            label='Instructions',
            instructions='Instruction 1\nInstruction 2\n\nInstruction 3\nInstruction 4\n\n\n'
        )
        assert recipe_page_instructions_section.instructions_list == [
            'Instruction 1',
            'Instruction 2',
            'Instruction 3',
            'Instruction 4',
        ]
