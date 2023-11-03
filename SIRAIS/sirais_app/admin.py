from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'get_groups_display')
    list_filter = ['admin', 'is_staff', 'groups']
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'expertise', 'biographie')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'admin', 'groups',)}),
    )

    def get_groups_display(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])
    
    get_groups_display.short_description = _('Groups')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Resource)
admin.site.register(Comment)
