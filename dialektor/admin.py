from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import CustomUser

from .models import metadata

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'inst_name']

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(metadata)
