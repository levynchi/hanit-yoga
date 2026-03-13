"""
URL configuration for yoga project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('yoga.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production: serve media from MEDIA_ROOT (e.g. Railway volume)
    media_prefix = settings.MEDIA_URL.strip('/')
    if media_prefix:
        urlpatterns += [
            path(f'{media_prefix}/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
        ]
