from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from filebrowser.sites import site

urlpatterns = [
    # Created Apps.
    path('', include('posts.urls')),  # Posts
    path('api/', include('posts_api.urls')),  # Posts API
    path('accounts/', include('accounts.urls')),  # Accounts app.

    # Defaults
    path('admin/', admin.site.urls),  # Admin

    # Third party
    path('tinymce/', include('tinymce.urls')),  # TinyMCE
    path('admin/filebrowser/', site.urls),  # FileBrowser
    path('auth/', include('dj_rest_auth.urls'))  # Dj rest auth
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
