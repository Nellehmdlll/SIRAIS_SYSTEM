from django.contrib import admin
from sirais_app.models import CustomUser
from .models import Project 
# , Task , Resource , Comment , CoachProjectAssignment, ProjectOwnerProjectAssignment

admin.site.register(Project)
#admin.site.register(Project)
admin.site.register(CustomUser)
""" admin.site.register(Task)
admin.site.register(Resource)
admin.site.register(Comment)
admin.site.register(CoachProjectAssignment)
admin.site.register(ProjectOwnerProjectAssignment)
 """

