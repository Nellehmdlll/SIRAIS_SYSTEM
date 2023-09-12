from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import *
from django import forms
from .models import Project,Resource,BusinessModelCanvas , Task
from django.contrib.auth.forms import ReadOnlyPasswordHashField





class RegisterForm(forms.ModelForm):
    """
    The default

    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirmez le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username']

    

    def clean(self):
        '''
        Vérifiez que les deux mots de passe correspondent.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data




class UserAdminCreationForm(forms.ModelForm):
    """
    Un formulaire pour créer de nouveaux utilisateurs. Comprend tout le nécessaire
    champs, plus un mot de passe répété.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username']

    def clean(self):
        '''
        Vérifiez que les deux mots de passe correspondent.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Enregistrez le mot de passe fourni au format haché
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user




class UserAdminChangeForm(forms.ModelForm):
    """Un formulaire pour mettre à jour les utilisateurs. Inclut tous les champs sur
    l'utilisateur, mais remplace le champ du mot de passe par celui de l'administrateur
    champ d'affichage du hachage du mot de passe.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'is_active']

    def clean_password(self):
    # Indépendamment de ce que l'utilisateur fournit, renvoie la valeur initiale.
    # Cela se fait ici, plutôt que sur le terrain, car le
    # le champ n'a pas accès à la valeur initiale
        return self.initial["password"]




class CustomUserAdminCreationForm(UserCreationForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField()
    phone = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    expertise = forms.CharField(max_length=200)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'phone', 'address', 'expertise')

    def clean(self):
            '''
            Vérifiez que les deux mots de passe correspondent.
            '''
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            password_2 = cleaned_data.get("password_2")
            if password is not None and password != password_2:
                self.add_error("password_2", "Your passwords must match")
            return cleaned_data

    def save(self, commit=True):
            # Enregistrez le mot de passe fourni au format haché
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user

class CustomUserAdminChangeForm(forms.ModelForm):
    # Définissez les champs que vous souhaitez inclure lors de la modification d'un utilisateur existant.
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address', 'expertise', 'is_active', 'groups', 'permission')


    def clean_password(self):
    # Indépendamment de ce que l'utilisateur fournit, renvoie la valeur initiale.
    # Cela se fait ici, plutôt que sur le terrain, car le
    # le champ n'a pas accès à la valeur initiale
        return self.initial["password"]












































































# class CoachRegistrationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password1', 'password2', 'user_type', 'expertise', 'experience', 'photo']
#         labels = {
#             'expertise': _('Domaine d\'expertise'),
#             'experience': _('Expérience (en années)'),
#             'photo': _('Photo de profil'),
#         }


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