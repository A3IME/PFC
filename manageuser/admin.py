from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from manageuser.models import Directories

class DirectoriesInline(admin.StackedInline):
	model = Directories
	can_delete = False
	verbose_name_plural = 'directory'

class UserAdmin(BaseUserAdmin):
	inlines = (DirectoriesInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
