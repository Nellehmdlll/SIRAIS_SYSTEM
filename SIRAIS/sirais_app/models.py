from django import apps
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Crée et enregistre un utilisateur avec l'e-mail et le mot de passe donnés.
        """
        if not username:
            raise ValueError('Les utilisateurs doivent avoir un username')

        """ GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        ) """
        #user = GlobalUserModel.normalize_username(username)
        user = self.model(username=username,  **extra_fields)


        user.set_password(password)
        user.save(using=self._db)
        return user




    def create_staffuser(self, username, password):
        """
        Crée et enregistre un utilisateur du staff avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(
        username,
        password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user




    def create_superuser(self, username, password):
        """
        Crée et enregistre un superutilisateur avec l'e-mail et le mot de passe donnés.
        """
        user = self.create_user(
        username,
        password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user






class CustomUser(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()
    username = models.CharField(
    verbose_name='Username',
    max_length=60,
    unique=True,
    )
    phone = models.CharField(max_length=100, default="345656")
    email = models.EmailField(null=True,default=None,blank=True)
    address = models.CharField(max_length=200, blank=True, null=True, default="Votre adresse par défaut")
    expertise = models.CharField(max_length=200,blank=False,default=None, null=True,)
    
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    
    groups = models.ManyToManyField(Group, related_name='users_group', blank=True) 
    permission = models.ManyToManyField(Permission, related_name='users')

    # remarquez l'absence du "champ password", c'est intégré pas besoin de preciser.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] 
    def get_full_name(self):
    # L'utilisateur est identifié par son adresse e-mail
        return self.username
    def get_short_name(self):
    # L'utilisateur est identifié par son adresse e-mail
        return self.username

    def __str__(self):
        return self.username

            
        
    def has_perm(self, perm, obj=None):
        "L'utilisateur a-t-il une autorisation spécifique ?"
    # Réponse la plus simple possible : Oui, toujours
        return True

    def has_module_perms(self, app_label):
        "L'utilisateur dispose-t-il des autorisations nécessaires pour voir l'application ?`app_label`?"
    # Réponse la plus simple possible : Oui, toujours
        return True
        
    @property
    def is_staff(self):
        "L'utilisateur est-il un membre du personnel ?"
        return self.staff
    @property
    def is_admin(self):
        "L'utilisateur est-il un membre administrateur?"
        return self.admin
    
 

# Create your models here.
class Project(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True)
    start_date = models.DateTimeField(default=timezone.now, blank=True)
    end_date = models.DateTimeField(default=timezone.now, blank=True)
    porteur_de_projet = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projets_porteur', limit_choices_to={'groups__name': 'Porteurs de projet'},default='Choisir un porteur de projet')
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


    def __str__(self):
        return f"Resource {self.id} - {self.project.name}"








class CoachProjectAssignment(models.Model):
    # Champ de clé étrangère pour lier le projet à l'utilisateur (coach, mentor, ou porteur de projet)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='coach_assignments', default=1)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    assignment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.coach} assigned to {self.project} on {self.assignment_date}"




class ProjectOwnerProjectAssignment(models.Model):
    project_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='project_owner_assignments')
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    assignment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_owner} assigned to {self.project} on {self.assignment_date}"



# class Comment(models.Model):
#     content = models.TextField()
#     author = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         limit_choices_to=Q(coach__isnull=False) | Q(mentor__isnull=False)
#     )
#     date = models.DateTimeField(auto_now_add=True)
#     project = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
#     task = models.ForeignKey('Task', on_delete=models.CASCADE, blank=True, null=True)

#     def __str__(self):
#         return f"Comment by {self.author} on {self.date}"



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
    deadline = models.DateTimeField(default=None)
    status_choices = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks',default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks_coach', null=True, blank=True)
    
    def __str__(self):
        return self.name
