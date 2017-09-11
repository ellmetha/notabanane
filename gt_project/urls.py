"""
    Base URL configuration the gaelletonic project
    ==============================================

    For more information on this file, see https://docs.djangoproject.com/en/1.10/topics/http/urls/

"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls


js_info_dict = {
    'packages': ('base', ),
}

urlpatterns = [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript_catalog'),

    # Admin
    url(r'^' + settings.ADMIN_URL, admin.site.urls),

    # Apps
    url(r'^' + settings.WAGTAIL_ADMIN_URL, include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    # Add the Debug Toolbar’s URLs to the project’s URLconf
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)), ]

    # In DEBUG mode, serve media files through Django.
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views import static
    urlpatterns += staticfiles_urlpatterns()
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += [
        url(r'^%s/(?P<path>.*)$' % media_url, static.serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]

    # Test 503, 500, 404 and 403 pages
    from django.views.generic import TemplateView
    urlpatterns += [
        url(r'^403/$', TemplateView.as_view(template_name='403.html')),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
        url(r'^503/$', TemplateView.as_view(template_name='503.html')),
    ]
