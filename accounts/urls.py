from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'web-admin/',
        views.web_admin_dashboard,
        name='web_admin_dashboard'
    ),

    path(
        'web-admin/add-user/',
        views.web_admin_add_user,
        name='web_admin_add_user'
    ),

    path(
        'web-admin/create-group/',
        views.web_admin_create_group,
        name='web_admin_create_group'
    ),

    path(
        'web-admin/delete-user/<int:user_id>/',
        views.web_admin_delete_user,
        name='web_admin_delete_user'
    ),

    path(
        'web-admin/delete-group/<int:group_id>/',
        views.web_admin_delete_group,
        name='web_admin_delete_group'
    ),

    path(
        'manager/',
        views.manager_dashboard,
        name='manager_dashboard'
    ),

    path(
        'tl/',
        views.tl_dashboard,
        name='tl_dashboard'
    ),

    path(
        'member/',
        views.member_dashboard,
        name='member_dashboard'
    ),
]
