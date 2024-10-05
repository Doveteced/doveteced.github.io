from django.contrib import admin
from .models import Profile, Topic, Category, Like, Dislike

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'token', 'otp', 'otp_timestamp')
    search_fields = ('user__username', 'user__email')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'featured')
    search_fields = ('name', 'category')
    list_filter = ('category', 'tags')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__username', 'article__title')
    list_filter = ('article', 'created_at')

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__username', 'article__title')
    list_filter = ('article', 'created_at')