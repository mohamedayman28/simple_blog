from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    # All posts.
    path('', views.home_page, name='home_page'),
    # Filter posts by category.
    path('category/<category>/', views.home_page, name='category'),
    # Create new post.
    path('create-post/', views.post_form, name='create'),
    # Get post details.
    path('post/<id>/', views.post_details, name='details'),
    # Update post.
    path('update-post/<id>/', views.post_form, name='update'),
    # Delete post
    path('delete-post/<id>/', views.post_form, name='delete'),
]
