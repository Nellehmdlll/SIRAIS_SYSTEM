from django.contrib import admin
from .forms import CustomUserAdminChangeForm, CustomUserAdminCreationForm, UserAdminChangeForm, UserAdminCreationForm
from .models import Project , CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm

# , Task , Resource , Comment , CoachProjectAssignment, ProjectOwnerProjectAssignment


CustomUser = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
# Les formulaires pour ajouter et modifier des instances d'utilisateur
    form = CustomUserAdminChangeForm
    add_form = CustomUserAdminCreationForm
     

    # Les champs à utiliser pour afficher le modèle User.
    # Celles-ci remplacent les définitions de la baseUserAdmin
    # qui font référence à des champs spécifiques sur auth.User.
    list_display = ['username', 'admin','staff','email', 'phone', 'address',]
    list_filter = ['admin', 'staff']
    fieldsets = (
    (None, {'fields': ('username', 'password',)}),
    ('Personal info', {'fields': ('email', 'phone', 'address','expertise',)}),
    ('Permissions', {'fields': ('is_active', 'staff', 'admin', 'groups', 'permission',)}),
    )
   
    # add_fieldsets n'est pas un attribut ModelAdmin standard. UtilisateurAdmin
    # remplace get_fieldsets pour utiliser cet attribut lors de la création d'un utilisateur.
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('username', 'password')}
    ),
    )
    search_fields = ['username']
    ordering = ['username']
    filter_horizontal = ()



class UserAdmin(BaseUserAdmin):
# Les formulaires pour ajouter et modifier des instances d'utilisateur
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # Les champs à utiliser pour afficher le modèle User.
    # Celles-ci remplacent les définitions de la baseUserAdmin
    # qui font référence à des champs spécifiques sur auth.User.
    list_display = ['username', 'admin','staff']
    list_filter = ['admin', 'staff']
    fieldsets = (
    (None, {'fields': ('username', 'password',)}),
    ('Personal info', {'fields': ('phone',)}),
    ('Permissions', {'fields': ('admin',)}),
    )

    # add_fieldsets n'est pas un attribut ModelAdmin standard. UtilisateurAdmin
    # remplace get_fieldsets pour utiliser cet attribut lors de la création d'un utilisateur.
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('username', 'password')}
    ),
    )
    search_fields = ['username']
    ordering = ['username']
    filter_horizontal = ()









admin.site.register(Project)
#admin.site.register(Project)
#admin.site.register(CustomUser, UserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

""" admin.site.register(Task)
admin.site.register(Resource)
admin.site.register(Comment)
admin.site.register(CoachProjectAssignment)
admin.site.register(ProjectOwnerProjectAssignment)
 """

