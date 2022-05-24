from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, Post, Rating


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile.html'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PostInline(admin.StackedInline):
    model = Post
    can_delete = True
    verbose_name_plural = 'post'


# Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (PostInline,)

admin.site.register(Post)


admin.site.register(Rating)