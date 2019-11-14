import datetime as dt
import json

import pytest
from django.urls import reverse
from django.utils import timezone as tz
from graphql_relay import to_global_id

from main.apps.blog.test.factories import BlogPageFactory, RecipePageFactory


@pytest.mark.django_db
class TestRecipePageType:
    def test_exposes_only_live_pages_ordered_by_latest_date(self, client):
        blog_page = BlogPageFactory.create()

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
