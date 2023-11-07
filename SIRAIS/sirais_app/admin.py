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
    
class ProjectAdmin(admin.ModelAdmin):
       list_display = ('name', 'project_state', 'start_date','coach','porteur_de_projet')
       search_fields = ('name',)
       list_filter = ('project_state',)
       ordering = ('-start_date',)

class TaskAdmin(admin.ModelAdmin):
       list_display = ('name', 'deadline', 'status')
       search_fields = ('name',)
       list_filter = ('status',)
       ordering = ('name',)
       
class RessourceAdmin(admin.ModelAdmin):
       list_display = ('title', 'project', 'validated')
       search_fields = ('title',)
       list_filter = ('validated',)
       ordering = ('title',)

class BMCAdmin(admin.ModelAdmin):
       list_display = ('segment_client','proposition_de_valeur','cannaux_de_distribution','relation_client','source_de_revenus','ressources_cles','activites_cles','partenaires_cles','structure_des_couts')
       
class CommentAdmin(admin.ModelAdmin):
       list_display = ('author', 'content', 'date','resource')
       search_fields = ('author',)
       list_filter = ('author',)
       ordering = ('author',)     
         
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Resource,RessourceAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(BusinessModelCanvas,BMCAdmin)
