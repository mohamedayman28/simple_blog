from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from filebrowser.sites import site

urlpatterns = [
    path('admin/', admin.site.urls),
    # Posts app
    path('', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
    # TinyMce
    path('tinymce/', include('tinymce.urls')),
    # Filebrowser
    path('admin/filebrowser/', site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
