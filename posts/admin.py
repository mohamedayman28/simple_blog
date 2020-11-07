from django.contrib import admin

from posts.models import Post, Category, Author

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
