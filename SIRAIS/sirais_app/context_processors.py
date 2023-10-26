
from sirais_app.models import Project

def disponibleProject (request):
    dispo_projets = Project.objects.all()
    return {'dispo_projets': dispo_projets}


def active_project(request):
    active_project = None
    project_id = request.session.get('active_project_id')
    if request.user.is_authenticated:
        project_id = request.session.get('active_project_id')
        if project_id:
            try:
                active_project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                pass
    return {'active_project': active_project}

""" def active_project(request):
    active_project = None
    project_id = request.session.get('active_project_id') #utiliser un request.user
    if request.user.is_authenticated:
        project_id = request.session.get('active_project_id')
        if project_id:
            try:
                active_project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                pass
    return active_project """

