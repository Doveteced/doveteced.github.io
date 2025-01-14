from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import Article, Profile, Reply, Tag, Comment, User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()

# Unregister the Group model from admin as it's not used
admin.site.unregister(Group)

# Register the custom User model and UserAdmin
admin.site.register(User, UserAdmin)

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
