from django.contrib import admin
from .forms import CustomUserAdminChangeForm, CustomUserAdminCreationForm
from .models import Project , CustomUser,Task,Resource,Comment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
# Les formulaires pour ajouter et modifier des instances d'utilisateur
    form = CustomUserAdminChangeForm
    add_form = CustomUserAdminCreationForm
     

    # Les champs à utiliser pour afficher le modèle User.
    # Celles-ci remplacent les définitions de la baseUserAdmin
    # qui font référence à des champs spécifiques sur auth.User.
    list_display = ['username','staff','email', 'phone', 'address','expertise']
    list_filter = ['admin', 'staff']
    fieldsets = (
    (None, {'fields': ('username', 'password',)}),
    ('Personal info', {'fields': ('email', 'phone', 'address','expertise','biographie')}),
    ('Permissions', {'fields': ('is_active', 'staff', 'admin', 'groups',)}),
    
    )
   
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('username','email','phone','address','expertise')}
    ),
    )
    search_fields = ['username']
    ordering = ['username']
    filter_horizontal = ()



admin.site.register(Project)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task)
admin.site.register(Resource)
admin.site.register(Comment)



