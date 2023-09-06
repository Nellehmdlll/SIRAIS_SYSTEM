from django.urls import path
from .views import ProjectOwnerLoginView, ProjectListView ,DashboardView ,ResourceListView, BusinessModelView, CreateProjectView ,EditProjectView, DeleteProjectView ,ListView ,CreateTaskView
from .views import add_resource , ProjectDetailView ,validate_resources , agenda ,phaseView,validate_resource
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', ProjectOwnerLoginView.as_view(), name='porteur_de_projet_login'),
    #path('dashboard/',dashboard, name='dashboard'),  
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
    path('detail/<int:project_id>/', ProjectDetailView.as_view(), name='project_detail'),
    path('liste/<str:liste_type>/', ListView.as_view(), name='liste'),
    path('project_liste/', ProjectListView.as_view(), name='project_liste'),
    path('edit/<int:id>/', EditProjectView.as_view(), name='edit_project'),
    path('delete/<int:id>/', DeleteProjectView.as_view(), name='delete_project'),
    path('resource/<int:project_id>/', ResourceListView.as_view(), name='project_resource'),
    #path('phases/<int:project_id>/', phaseView, name='phases'),
    
    path('creer/', CreateTaskView.as_view(), name='create_task'),

    #path('project/<int:project_id>/create_task/', views.create_task, name='create_task'),
    path('project/<int:project_id>/tasks/', views.task_list, name='task_list'),
    path('project/<int:project_id>/task/<int:task_id>/', views.task_detail, name='task_detail'),
 



    path('validate/add/<int:resource_id>/', validate_resource, name='validate_resource'),

    path('validate/<int:project_id>/<str:phase>/', validate_resources, name='validate_resources'),
    path('add_resource/<int:project_id>/<str:phase>/', add_resource, name='add_resource'),
    path('business_model/', BusinessModelView.as_view(), name='business_model'),

    # path('authorize_google/', authorize_google, name='authorize_google'),
    # path('google_callback/', google_callback, name='google_callback'),
    
    path('agenda/',agenda,name='agenda'),
    # path('google-auth/', views.google_auth, name='google_auth'),
    # path('google-auth-return/', views.google_auth_return, name='google_auth_return'),
    # path('create-event/', views.create_event, name='create_event'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('calendar/create_events/', views.create_calendar_event, name='create_events'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    


]
