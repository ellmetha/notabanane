"""
    Project URLs
    ============

    This module is the main entrypoint for all the URLs associated with the views provided by the
    project. It includes URLs associated with specific sections/parts of the considered application.

"""

from django.urls import path

from . import feeds, views


urlpatterns = [
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('graphql/', views.GraphQLView.as_view(), name='graphql'),
    path('feed/', feeds.LatestEntriesFeed(), name='feed'),
    path('bad/', views.BadView.as_view(), name='bad'),
]
