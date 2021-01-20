from django.conf import settings
from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User

from filebrowser.fields import FileBrowseField
from tinymce import HTMLField


user = settings.AUTH_USER_MODEL


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = FileBrowseField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name.username


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Category"

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    thumbnail = FileBrowseField(max_length=200, null=True)
    content = HTMLField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:details', kwargs={'id': self.id})

    def get_create_url(self):
        return reverse('posts:create', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('posts:update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('posts:delete', kwargs={'id': self.id})


class UserInteraction(models.Model):
    """Mutual fields within Comment and Replay models"""
    commenter = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.commenter.username

    class Meta:
        abstract = True


class Comment(UserInteraction):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
