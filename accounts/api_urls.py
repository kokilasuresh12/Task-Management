from django.urls import path

from . import api_views


urlpatterns = [
    path('session/', api_views.session_view, name='api_session'),
    path('login/', api_views.login_view, name='api_login'),
    path('logout/', api_views.logout_view, name='api_logout'),
    path('bootstrap/', api_views.bootstrap_view, name='api_bootstrap'),
    path('users/', api_views.users_view, name='api_users'),
    path('users/<int:user_id>/', api_views.user_detail_view, name='api_user_detail'),
    path('groups/', api_views.groups_view, name='api_groups'),
    path('groups/<int:group_id>/', api_views.group_detail_view, name='api_group_detail'),
    path('projects/', api_views.projects_view, name='api_projects'),
    path('projects/<int:project_id>/status/', api_views.project_status_view, name='api_project_status'),
    path('tasks/', api_views.tasks_view, name='api_tasks'),
    path('tasks/<int:task_id>/progress/', api_views.task_progress_view, name='api_task_progress'),
    path('tasks/<int:task_id>/submit/', api_views.task_submit_view, name='api_task_submit'),
    path('tasks/<int:task_id>/approve/', api_views.task_approve_view, name='api_task_approve'),
    path('tasks/<int:task_id>/meet/', api_views.task_meet_view, name='api_task_meet'),
    path('tasks/<int:task_id>/history/', api_views.task_history_view, name='api_task_history'),
]
