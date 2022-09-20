from django.contrib import admin
from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    filter_horizontal = ("following",)   #nice representation for M-M relationships in admin interface

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    filter_horizontal = ("likes",)

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)

#admin, admin@example.com, 12345