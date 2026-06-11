from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/',
        views.create_task,
        name='create_task'
    ),

    path(
        'list/',
        views.task_list,
        name='task_list'
    ),

    path(
        'member/',
        views.member_tasks,
        name='member_tasks'
    ),

    path(
        'update/<int:task_id>/',
        views.update_progress,
        name='update_progress'
    ),

    path(
        'submit-work/<int:task_id>/',
        views.submit_work,
        name='submit_work'
    ),

    path(
        'history/<int:task_id>/',
        views.progress_history,
        name='progress_history'
    ),

    path(
        'approve/<int:task_id>/',
        views.approve_task,
        name='approve_task'
    ),

    path(
        'share-meet/<int:task_id>/',
        views.share_meet_link,
        name='share_meet_link'
    ),
]
