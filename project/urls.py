"""
    Project base URL configuration
    ==============================

    For more information on this file, see https://docs.djangoproject.com/en/1.10/topics/http/urls/

"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls


js_info_dict = {
    'packages': ('base', ),
}

urlpatterns = [
    # Admin.
    path(settings.ADMIN_URL, admin.site.urls),

    # Apps.
    path(settings.WAGTAIL_ADMIN_URL, include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    # Sitemaps
    path('sitemap.xml', sitemap, name='sitemap'),

    # Internationalization URLs.
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', cache_page(60 * 15)(JavaScriptCatalog.as_view()), name='javascript_catalog'),

    # Robots URLs.
    path(
        'robots.txt',
        cache_page(60 * 15)(
            TemplateView.as_view(template_name='robots.txt', content_type='text/plain')
        ),
    ),
]

if settings.DEBUG:
    # Add the Debug Toolbar’s URLs to the project’s URLconf.
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]

    # In DEBUG mode, serve media files through Django.
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views import static
    urlpatterns += staticfiles_urlpatterns()
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += [
        re_path(
            r'^%s/(?P<path>.*)$' % media_url,
            static.serve,
            {'document_root': settings.MEDIA_ROOT}
        ),
    ]

    # Test 503, 500, 404 and 403 pages.
    from django.views.generic import TemplateView
    urlpatterns += [
        path('403/', TemplateView.as_view(template_name='403.html')),
        path('404/', TemplateView.as_view(template_name='404.html')),
        path('500/', TemplateView.as_view(template_name='500.html')),
        path('503/', TemplateView.as_view(template_name='503.html')),
    ]

urlpatterns.append(path('', include('main.presentation.urls')))
urlpatterns.append(path('', include(wagtail_urls)))
