from django.contrib import admin
from .models import Topic, Post, Comment, Reply, Like, Dislike

admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)
admin.site.register(Dislike)
