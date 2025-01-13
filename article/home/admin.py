from django.contrib import admin
from .models import Article, Profile, Reply, Tag, Comment

# Register the Article model
admin.site.register(Article)

# Admin configuration for the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

# Admin configuration for the Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tag._meta.fields]

# Admin configuration for the Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]

# Admin configuration for the Reply model
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reply._meta.fields]
