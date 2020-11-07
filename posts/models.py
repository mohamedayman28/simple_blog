from django.conf import settings
from django.shortcuts import reverse
from django.db import models

from filebrowser.fields import FileBrowseField
from tinymce import HTMLField


user = settings.AUTH_USER_MODEL


class Author(models.Model):
    name = models.OneToOneField(user, on_delete=models.CASCADE)
    profile_pic = FileBrowseField(max_length=200)

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
    # blank and null for test purposes
    thumbnail = FileBrowseField(max_length=200, null=True, blank=True)
    overview = models.CharField(max_length=300)
    # blank and null for test purposes
    content = HTMLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:details', kwargs={'id': self.id})
