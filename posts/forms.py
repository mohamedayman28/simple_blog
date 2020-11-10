# Default
from django.forms import ModelForm
# Created
from posts.models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'overview', 'content', 'categories')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = 'content',
