from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/',
        views.create_project,
        name='create_project'
    ),

    path(
        'list/',
        views.project_list,
        name='project_list'
    ),

    path(
        'report/',
        views.manager_report,
        name='manager_report'
    ),
]
