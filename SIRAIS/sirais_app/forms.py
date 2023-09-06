from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import *
from django import forms
from .models import Project,Resource,BusinessModelCanvas , Task



class CoachRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'user_type', 'expertise', 'experience', 'photo']
        labels = {
            'expertise': _('Domaine d\'expertise'),
            'experience': _('Expérience (en années)'),
            'photo': _('Photo de profil'),
        }


class ProjectForm(forms.ModelForm):
    is_active = forms.BooleanField(
        required=True, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Is Active' 
    )

    class Meta:
        model = Project
        fields = ['name', 'desc', 'start_date', 'end_date', 'porteur_de_projet', 'coach', 'project_state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'porteur_de_projet': forms.Select(attrs={'class': 'form-control'}),
            'coach': forms.Select(attrs={'class': 'form-control'}),
            'project_state': forms.Select(attrs={'class': 'form-control'}),
        }



# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['name', 'desc' ,'start_date','end_date','state_date','porteur_de_projet','coach','project_state']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'desc': forms.Textarea(attrs={'class': 'form-control'}),
#             'start_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
#             'end_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
#             'porteur_de_projet': forms.Select(attrs={'class': 'form-control'}),
#             'coach': forms.Select(attrs={'class': 'form-control'}),
#             'project_state': forms.Select(attrs={'class': 'form-control'}),
#             'is_active' : forms.BooleanField(attrs={'class' : 'form-control' })
#         }



class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['type', 'file', 'link', 'title' , 'desc', ]
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    
            


            
        



class BusinessModelCanvasForm(forms.ModelForm):
    class Meta:
        model = BusinessModelCanvas
        fields = ['key_segment', 'value_proposition', 'channels','customer_relation', 'key_resource' , 'key_activities','key_partners', 'money_structure']  

 

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline']
