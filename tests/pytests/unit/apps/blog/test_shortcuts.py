import unittest.mock

import pytest
from django.core.cache import cache

from main.apps.blog.shortcuts import get_instagram_media_feed


class TestGetInstagramMediaFeed:
    @pytest.mark.fixture(autouse=True)
    def setup(self):
        cache.clear()

    @unittest.mock.patch('facebook.GraphAPI.get_object')
    def test_returns_the_instagram_media_feed(self, mocked_graph_get):
        mocked_graph_get.return_value = {'data': [{'id': 1}, {'id': 2}, {'id': 3}]}
        assert get_instagram_media_feed() == [{'id': 1}, {'id': 2}, {'id': 3}]

    @unittest.mock.patch('facebook.GraphAPI.get_object')
    def test_returns_the_cached_instagram_media_feed_if_applicable(self, mocked_graph_get):
        mocked_graph_get.return_value = {'data': [{'id': 1}, {'id': 2}, {'id': 3}]}
        assert get_instagram_media_feed() == [{'id': 1}, {'id': 2}, {'id': 3}]
        assert get_instagram_media_feed() == [{'id': 1}, {'id': 2}, {'id': 3}]
        assert mocked_graph_get.call_count == 1

    @unittest.mock.patch('facebook.GraphAPI.get_object')
    def test_can_return_the_instagram_media_feed_using_a_specific_limit(self, mocked_graph_get):
        mocked_graph_get.return_value = {'data': [{'id': 1}, {'id': 2}]}
        assert get_instagram_media_feed(limit=2) == [{'id': 1}, {'id': 2}]
        assert mocked_graph_get.call_args[-1]['limit'] == 2
