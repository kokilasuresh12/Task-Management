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
