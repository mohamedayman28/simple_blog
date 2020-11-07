# Default
from django.forms import ModelForm
# Created
from posts.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'overview', 'content', 'categories')
