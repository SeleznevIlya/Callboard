from django.contrib import admin

from .models import Post, Subscribers, Reply, Category

admin.site.register(Post)
admin.site.register(Subscribers)
admin.site.register(Reply)
admin.site.register(Category)
