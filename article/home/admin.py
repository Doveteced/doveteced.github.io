from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
from .models import BlogModel, Profile

admin.site.register(BlogModel)
admin.site.register(Profile)
=======
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
>>>>>>> a8d18b23b80ec99c1d3244ee281b19dc054e7ea5
