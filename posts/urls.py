from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('<category>/', views.home_page, name='category'),
    path('post/<id>/', views.details_post, name='details'),
    path('create-post', views.create_post, name='create'),
]
