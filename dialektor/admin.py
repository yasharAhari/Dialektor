from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from dialektor.models import Researcher

class ResearcherInline(admin.StackedInline):
    model = Researcher
    can_delete = False
    verbose_name_plural = 'researcher'

class UserAdmin(BaseUserAdmin):
    inlines = (ResearcherInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

