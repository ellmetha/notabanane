import datetime as dt
import json

import pytest
from django.urls import reverse
from django.utils import timezone as tz
from graphql_relay import to_global_id
from wagtail.core.models import Site

from main.apps.blog.test.factories import BlogPageFactory, RecipePageFactory


@pytest.mark.django_db
class TestRecipePageType:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blog_page = BlogPageFactory.create()
        self.site = Site.objects.create(
            hostname='localhost',
            site_name='Test site',
            root_page=self.blog_page,
            is_default_site=True
        )

    def test_exposes_only_live_pages_ordered_by_latest_date(self, client):
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

        query = '''
            query {
                recipes(first: 10) {
                    edges {
                        node {
                            id
                            title
                            date
                        }
                    }
                }
            }
        '''

        response = client.post(
            reverse('graphql'),
            json.dumps({'query': query}),
            content_type='application/json'
        )

        content = json.loads(response.content)

        assert [e['node']['id'] for e in content['data']['recipes']['edges']] == [
            to_global_id('RecipePageType', recipe_page_2.id),
            to_global_id('RecipePageType', recipe_page_3.id),
            to_global_id('RecipePageType', recipe_page_1.id),
        ]

    def test_properly_exposes_a_thumbnail_of_the_header_image_of_recipe_pages(self, client):
        recipe_page = RecipePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=3),
            live=True
        )

        query = '''
            query {
                recipes(first: 10) {
                    edges {
                        node {
                            id
                            headerImageThumbnail
                        }
                    }
                }
            }
        '''

        response = client.post(
            reverse('graphql'),
            json.dumps({'query': query}),
            content_type='application/json'
        )

        content = json.loads(response.content)

        assert content['data']['recipes']['edges'][0]['node']['headerImageThumbnail'] == (
            recipe_page.header_image.get_rendition('fill-555x312').url
        )

    def test_properly_exposes_the_url_of_recipe_pages(self, client):
        recipe_page = RecipePageFactory.create(
            parent=self.blog_page,
            date=tz.now() - dt.timedelta(days=3),
            live=True
        )

        query = '''
            query {
                recipes(first: 10) {
                    edges {
                        node {
                            id
                            url
                        }
                    }
                }
            }
        '''

        response = client.post(
            reverse('graphql'),
            json.dumps({'query': query}),
            content_type='application/json',
            site=self.site
        )

        content = json.loads(response.content)

        assert content['data']['recipes']['edges'][0]['node']['url'] == recipe_page.url
