from django.contrib import admin

from posts.models import Post, Category, Author, Comment

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
