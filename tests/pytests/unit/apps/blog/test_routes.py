import datetime as dt

import pytest
from django.utils import timezone as tz

from main.apps.blog.test.factories import ArticlePageFactory, BlogPageFactory, RecipePageFactory


@pytest.mark.django_db
class TestBlogRoutes:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blog_page = BlogPageFactory.create()

    def test_entries_list_include_the_latest_articles_and_recipes(self, rf):
        article_page_1 = ArticlePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=5),
            live=True
        )
        article_page_2 = ArticlePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=4),
            live=True
        )
        article_page_3 = ArticlePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=2),
            live=True
        )
        article_page_4 = ArticlePageFactory.create(parent=self.blog_page, live=False)  # noqa: F841

        recipe_page_1 = RecipePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=3),
            live=True
        )
        recipe_page_2 = RecipePageFactory.create(parent=self.blog_page, live=True)
        recipe_page_3 = RecipePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=1),
            live=True
        )
        recipe_page_4 = RecipePageFactory.create(parent=self.blog_page, live=False)  # noqa: F841

        response = self.blog_page.entries_list(rf.get('/'))

        assert list(response.context_data['self'].latest_recipes) == [
            recipe_page_2,
            recipe_page_3,
            recipe_page_1,
        ]
        assert list(response.context_data['self'].latest_articles) == [
            article_page_3,
            article_page_2,
            article_page_1,
        ]

    def test_entries_search_can_search_for_blog_entries(self, rf):
        article_page_1 = ArticlePageFactory.create(
            parent=self.blog_page,
            live=True,
            title='My super article'
        )
        ArticlePageFactory.create(
            parent=self.blog_page,
            live=True,
            title='My dummy article'
        )
        recipe_page_1 = RecipePageFactory.create(
            parent=self.blog_page,
            live=True,
            title='My super recipe'
        )
        RecipePageFactory.create(
            parent=self.blog_page,
            live=True,
            title='My dummy recipe'
        )

        response = self.blog_page.entries_search(rf.get('/search', {'q': 'super'}))

        assert set(response.context_data['self'].entries) == {
            article_page_1.page_ptr,
            recipe_page_1.page_ptr,
        }

    def test_articles_list_include_live_articles(self, rf):
        article_page_1 = ArticlePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=5),
            live=True
        )
        article_page_2 = ArticlePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=4),
            live=True
        )
        article_page_3 = ArticlePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=2),
            live=True
        )
        article_page_4 = ArticlePageFactory.create(parent=self.blog_page, live=False)  # noqa: F841

        response = self.blog_page.articles_list(rf.get('/articles'))

        assert list(response.context_data['self'].entries) == [
            article_page_3,
            article_page_2,
            article_page_1,
        ]

    def test_recipes_list_include_live_recipes(self, rf):
        recipe_page_1 = RecipePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=3),
            live=True
        )
        recipe_page_2 = RecipePageFactory.create(parent=self.blog_page, live=True)
        recipe_page_3 = RecipePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=1),
            live=True
        )
        recipe_page_4 = RecipePageFactory.create(parent=self.blog_page, live=False)  # noqa: F841

        response = self.blog_page.recipes_list(rf.get('/recipes'))

        assert list(response.context_data['self'].entries) == [
            recipe_page_2,
            recipe_page_3,
            recipe_page_1,
        ]
