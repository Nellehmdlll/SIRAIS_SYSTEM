from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User





class CustomUser(AbstractUser):
    COACH = 'coach'
    MENTOR = 'mentor'
    PROJECT_OWNER = 'project_owner'

    USER_TYPES = [
        (COACH, 'Coach'),
        (MENTOR, 'Mentor'),
        (PROJECT_OWNER, 'Porteur de projet'),
    ]


    user_type = models.CharField(max_length=50, choices=USER_TYPES, default=COACH)
       
    # Champs ManyToMany pour les groupes
    groups = models.ManyToManyField(Group, related_name='users_group', blank=True)  # Nom personnalisé pour l'accessor

    # Champs spécifiques aux Coaches
    expertise = models.CharField(max_length=200,blank=False)
    experience = models.IntegerField(default=0)
    photo = models.ImageField(verbose_name='photo de profil', default="img/default_coach.jpg", upload_to='img_coachProfile', blank=True)

    # # Champs spécifiques aux Mentors
    # company = models.CharField(max_length=200, blank=True)
    # mentor_expertise = models.CharField(max_length=200, blank=True)
    # bio = models.TextField(blank=True)
    # mentor_photo = models.ImageField(verbose_name='photo de profil', default="img/default_mentor.jpg", upload_to='img_mentorProfile', blank=True)

    # Champs spécifiques aux Porteurs de projet
    phone_number = models.CharField(max_length=20, blank=True)
    project_owner_photo = models.ImageField(verbose_name='photo de profil', default="img/default_project_owner.jpg", upload_to='img_projectOwnerProfile', blank=True)

    def __str__(self):
        return self.username


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
