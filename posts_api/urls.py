from django.urls import path

from . import views


urlpatterns = [
    # Posts
    path('', views.AllPosts.as_view()),  # Get all posts.
    path('create/', views.PostCreate.as_view()),  # Create new post.
    path('<post_pk>/', views.PostDetails.as_view()),  # View post.
    path('<post_pk>/update/', views.PostUpdate.as_view()),  # Upddate post.
    path('<post_pk>/delete/', views.PostDelete.as_view()),  # Delete post.

    # Handle comments.
    path('<post_pk>/add-comment/', views.PostAddComment.as_view()),  # Add new comment.
    path('<post_pk>/show-related-comments/', views.PostShowRelatedComments.as_view()),  # Show comments related to one post
    path('<post_pk>/<comment_pk>/update/', views.PostUpdateComment.as_view()),  # Update comment.
    path('<post_pk>/<comment_pk>/delete/', views.PostDeleteComment.as_view()),  # Delete comment.

    # Search posts
    path('search/', views.SearchPosts.as_view()),
    # Filter posts by category
    path('filter/<category>/', views.FilterByCategory.as_view()),
]
