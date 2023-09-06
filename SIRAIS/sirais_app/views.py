from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import ProjectForm , ResourceForm ,BusinessModelCanvasForm,TaskForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from google_auth_oauthlib.flow import InstalledAppFlow
from django.http import HttpResponse, HttpResponseRedirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import datetime
from googleapiclient.discovery import build
from datetime import datetime, timedelta



class ProjectOwnerLoginView(View):
    login_page = 'projectOwner_login_view.html'
    is_staff=True

    def get(self, request):
        return render(request, self.login_page)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('project_liste') 
        else:
            return render(request, self.login_page, {'error_message': 'Identifiant ou mot de passe incorrect.'})

class ProjectOwnerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  



class DashboardView(View):

    def get(self, request):
        num_coaches = CustomUser.objects.filter(user_type='coach').count()

        num_mentors = CustomUser.objects.filter(user_type='mentor').count()
        liste_mentors = CustomUser.objects.filter(user_type='mentor').all()

        num_project_owners = CustomUser.objects.filter(user_type='project_owner').count()
        liste_project_owners = CustomUser.objects.filter(user_type='project_owner').all()

        nombre_projets = Project.objects.count()

    
        context = {
            'num_coaches': num_coaches,

            'num_mentors': num_mentors,
            'liste_mentors':liste_mentors,

            'num_project_owners': num_project_owners,
            'liste_project_owners':liste_project_owners,

            'num_project': nombre_projets,
        }

        return render(request, 'dashboard.html', context)




class ListView(View):
    def get(self, request, liste_type):
        if liste_type == 'mentors':
            liste = CustomUser.objects.filter(groups__name='Mentor').all()
            titre = 'Mentors'
        elif liste_type == 'coachs':
            liste = CustomUser.objects.filter(groups__name='Coachs').all()
            titre = 'Coaches'
        elif liste_type == 'project_owners':
            liste = CustomUser.objects.filter(groups__name='Porteurs de projet').all()
            titre = 'Porteurs de projet'
        else:
            liste = []
            titre = 'Liste inconnue'

        context = {
            'liste': liste,
            'titre': titre,
        }

        return render(request, 'liste.html', context)

class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.all()
        context = {
            'projects': projects,
        }
        return render(request, 'project_list.html', context)

class ResourceListView(View):
    def get(self, request, project_id):
        resources = Resource.objects.filter(project_id=project_id)

        context = {
            'resources': resources,
        }
        return render(request, 'resources_list.html', context)



class CreateProjectView(View):
    template_name = 'create_project.html'

    def get(self, request):
        form = ProjectForm()
        return render(request, 'create_project.html', {'form': form})

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', project_id=project.id)
        return render(request, 'create_project.html', {'form': form})


class EditProjectView(View):
    template_name = 'edit_project.html'

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = ProjectForm(instance=project)
        return render(request, 'edit_project.html', {'form': form, 'project':project})

    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_liste')
        return render(request, 'project_list.html', {'form': form, 'project':project})
    
class DeleteProjectView(View):
    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        project.delete()
        return redirect('project_liste')
    


def add_resource(request, project_id, phase ):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.project_id = project_id
            resource.validation_phase = Project.objects.get(id=project_id).current_phase
            resource.author = request.user
            resource.validation_phase = phase  

            resource.save()
            return redirect('validate_resources', project_id=project_id,phase=phase)
    else:
        form = ResourceForm()
    return render(request, 'add_resource.html', {'form': form})


def BusinessModelView(request):
    return render(request, 'business_model.html')

class BusinessModelView(View):
    template_name = 'business_model.html'

    def get(self, request):
        form = BusinessModelCanvasForm()
        return render(request, 'business_model.html', {'form': form})

    def post(self, request):
        form = BusinessModelCanvasForm(request.POST)
        if form.is_valid():
            project = Project.id
            canvas_data = form.save(commit=False)
            canvas_data.project = project
            canvas_data.save()
            return redirect('dashboard')  # Redirigez vers la page appropriée après l'enregistrement
        return render(request, 'business_model.html', {'form': form})


def select_active_project(request, project_id):
    try:
        active_project = Project.objects.get(id=project_id)
        request.session['active_project_id'] = active_project.id
        request.user.active_project = active_project  # Mettre à jour l'attribut
        request.user.save()
    except Project.DoesNotExist:
        pass



class ProjectDetailView(View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        resources = Resource.objects.filter(project_id=project_id)
        total_resources = resources.count()
        validated_resources = resources.filter(validated=True).count()
        progress = (validated_resources / total_resources) * 100 if total_resources > 0 else 0

        # Appel de la vue select_active_project pour définir le projet actif
        select_active_project(request, project_id)

        context = {
            'project': project,
            'resources': resources,
            'progress': progress,       
            'project_id': project_id,  
            'phase': project.current_phase,
            
        }

        return render(request, 'project_detail.html', context)

def phaseView(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    resources = Resource.objects.filter(project_id=project_id)
    # Je fais ca pour calculer la progression en fonction des ressources validées
    total_resources = resources.count()
    validated_resources = resources.filter(validated=True).count()
    progress = (validated_resources / total_resources) * 100 if total_resources > 0 else 0

    context = {
        'project': project,
        'resources': resources,
        'project_id': project_id, 
        'progress' : progress, 
        'phase': project.current_phase,  


    }

    return render(request, 'phases.html', context)

def validate_resources(request, phase, project_id):
    pending_resources = Resource.objects.filter(validated=False, validation_phase=phase, project_id=project_id)
    
    
    context = {
        'pending_resources': pending_resources,
        # 'project': project,
        'phase': phase, 
        'project_id':project_id,
        
    }
    return render(request, 'validate_resource.html', context)





def validate_resource(request, resource_id):
    resource = Resource.objects.get(id=resource_id)

    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'validate':
            resource.validated = True
            resource.save()
        elif action == 'reject':
            resource.validated = False
            resource.save()

        return redirect('validate_resources', phase=resource.validation_phase, project_id=resource.project_id)

    context = {
        'resource': resource,
    }
    return render(request, 'validate_resource.html', context)

# def create_task(request, project_id):
#     project = Project.objects.get(id=project_id)
#     coaches = CustomUser.objects.filter(groups__name='coach')  
    
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.project = project
#             task.coach = request.user if request.user.groups.filter(name='coach').exists() else None
#             task.save()
#             return redirect('task_list', project_id=project.id)
#     else:
#         form = TaskForm()
#         print(form.errors)
#     return render(request, 'create_task.html', {'form': form, 'project': project, 'coaches': coaches})



class CreateTaskView(View):
    template_name = 'create_task.html'

    def get(self, request):
        form = TaskForm()
        return render(request, 'create_task.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('project_detail', task_id=task.id)
        return render(request, 'task_list.html', {'form': form})
    
def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'task_list.html', {'project': project, 'tasks': tasks})

def task_detail(request, project_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})





 
t = 0

def agenda(request):
    if t == 1:
        credentials_info = request.session.get('credentials')
        calendar_id = None
        if credentials_info:
            credentials = Credentials.from_authorized_user_info(credentials_info, scopes=['https://www.googleapis.com/auth/calendar'])
            service = build('calendar', 'v3', credentials=credentials)

            events = service.events().list(calendarId='primary').execute()
            calendar_id = events[0]['organizer']['email']
        return render(request,'agenda.html',{id: calendar_id})
    return redirect('oauth2callback')




def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        'sirais_app/config/client_secrets.json',  # Téléchargé depuis la console de développement Google
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://localhost:8000/oauth2callback/'
    )
    
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Enregistrez les informations d'authentification dans la session ou la base de données
    request.session['credentials'] = credentials.to_authorized_user_info()
    global t
    t=1
    return redirect('agenda')  # Redirigez vers la page principale de votre application


def create_calendar_event(request):
    credentials_info = request.session.get('credentials')
    if credentials_info:
        credentials = Credentials.from_authorized_user_info(credentials_info, scopes=['https://www.googleapis.com/auth/calendar'])
        service = build('calendar', 'v3', credentials=credentials)

        event = {
            'summary': 'Nom de l\'événement',
            'start': {
                'dateTime': (datetime.now() + timedelta(days=1)).isoformat(),
                'timeZone': 'Europe/Paris',
            },
            'end': {
                'dateTime': (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
                'timeZone': 'Europe/Paris',
            },
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {created_event['htmlLink']}")

    # Redirection ou autre traitement
    return redirect('agenda')