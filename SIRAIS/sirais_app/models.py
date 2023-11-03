from django import apps
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.utils.translation import gettext_lazy as _
#from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=30,default='Nom')
    last_name = models.CharField(max_length=30,default='Prénom')
    email = models.EmailField(unique=True,default='votremail@gmail.com')
    phone = models.CharField(max_length=100, default="002266345656")
    address = models.CharField(max_length=200, blank=True, null=True, default="Votre adresse par défaut")
    expertise = models.CharField(max_length=200,blank=False,default=None, null=True,)
    biographie = models.TextField(blank=True,null=True)

    project = models.OneToOneField('Project', related_name='member', null=True, blank=True, on_delete=models.SET_NULL)
    
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
     

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Project(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True)
    start_date = models.DateTimeField(default=timezone.now, blank=True)
    end_date = models.DateTimeField(default=timezone.now, blank=True)
    porteur_de_projet = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projets_porteur', limit_choices_to={'groups__name': 'Porteur de projet'},default='Choisir un porteur de projet')
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projets_coach', limit_choices_to={'groups__name': 'Coachs'},default='Choisir un coach')
    is_active = models.BooleanField(default=True)

    PROJECT_STATES = (
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('on_hold', 'En attente'),
        # Ajoutez d'autres états si nécessaire
    )

    project_state = models.CharField(max_length=20, choices=PROJECT_STATES, blank=True)
    
    VALIDATION_PHASES = (
        ('ideation', 'Idéation'),
        ('prototypage', 'Prototypage'),
        ('modele_economique', 'Modèle économique'),
        ('entree_marche', 'Entrée sur le marché'),
    )
    current_phase = models.CharField(max_length=20, choices=VALIDATION_PHASES, default='ideation')


    
    def __str__(self):
        return self.name


class Resource(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200, default= None )
    desc = models.TextField(blank=True)
    RESOURCE_TYPES = (
        ('document', 'Document'),
        ('image', 'Image'),
        ('lien', 'Lien'),
    )
    type = models.CharField(max_length=100, choices=RESOURCE_TYPES, default='document')

    file = models.FileField(upload_to='resources/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    VALIDATION_PHASES = (
        ('ideation', 'Idéation'),
        ('prototypage', 'Prototypage'),
        ('modele_economique', 'Modèle économique'),
        ('entree_marche', 'Entrée sur le marché'),
    )
    validation_phase = models.CharField(max_length=20, choices=VALIDATION_PHASES, default='ideation')
    
    def is_coach(self):
        return self.user.groups.filter(name='Coachs').exists()

    def is_mentor(self):
        return self.author.groups.filter(name='Mentors').exists()
    
    def is_porteur(self):
        return self.author.groups.filter(name='Porteur de projet').exists()

    def __str__(self):
        return f"Resource {self.id} - {self.project.name}"

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,)
    date = models.DateTimeField(auto_now_add=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.author} - {self.date}"


class BusinessModelCanvas(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    key_segment = models.TextField()
    value_proposition = models.TextField()
    channels = models.TextField()
    customer_relation = models.TextField()
    money_source = models.TextField()
    key_resource =models.TextField()
    key_activities = models.TextField()
    key_partners=models.TextField()
    money_structure =models.TextField()

    def __str__(self):
        return f"Business Model Canvas for {self.project.name}"

  
class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now, blank=True)
    deadline = models.DateTimeField(default=timezone.now, blank=True)
    status_choices = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    #assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks',default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks',null=True,)
    #coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks_coach', null=True, blank=True)
    
    def __str__(self):
        return self.name
