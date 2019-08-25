import datetime as dt

import pytest
from django.utils import timezone as tz
from wagtail.core.models import Site

from main.apps.blog.test.factories import ArticlePageFactory, BlogPageFactory, RecipePageFactory
from main.common.test.factories import UserFactory
from main.presentation.feeds import LatestEntriesFeed


@pytest.mark.django_db
class TestLatestEntriesFeed:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.owner = UserFactory.create()
        self.blog_page = BlogPageFactory.create(owner=self.owner)
        self.feed = LatestEntriesFeed()
        self.site = Site.objects.create(
            hostname='localhost',
            site_name='Test site',
            root_page=self.blog_page,
            is_default_site=True
        )

    def test_includes_latest_articles_and_recipes(self, rf):
        article_page_1 = ArticlePageFactory.create(
            parent=self.blog_page,
            owner=self.owner,
            date=tz.now() - dt.timedelta(days=5),
            live=True
        )
        article_page_2 = ArticlePageFactory.create(
            parent=self.blog_page,
            owner=self.owner,
            date=tz.now() - dt.timedelta(days=4),
            live=True
        )
        article_page_3 = ArticlePageFactory.create(
            parent=self.blog_page,
            owner=self.owner,
            date=tz.now() - dt.timedelta(days=2),
            live=True
        )
        article_page_4 = ArticlePageFactory.create(  # noqa: F841
            parent=self.blog_page,
            owner=self.owner,
            live=False
        )

        recipe_page_1 = RecipePageFactory.create(
            parent=self.blog_page,
            owner=self.owner,
            date=tz.now() - dt.timedelta(days=3),
            live=True
        )
        recipe_page_2 = RecipePageFactory.create(parent=self.blog_page, owner=self.owner, live=True)
        recipe_page_3 = RecipePageFactory.create(
            parent=self.blog_page,
            owner=self.owner,
            date=tz.now() - dt.timedelta(days=1),
            live=True
        )
        recipe_page_4 = RecipePageFactory.create(  # noqa: F841
            parent=self.blog_page,
            owner=self.owner,
            live=False
        )

        request = rf.get('/')
        request.site = self.site
        self.feed.get_feed(None, request)
        entries = self.feed.items()

        assert entries == [
            recipe_page_2,
            recipe_page_3,
            article_page_3,
            recipe_page_1,
            article_page_2,
            article_page_1,
        ]
