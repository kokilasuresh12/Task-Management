from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .forms import LoginForm, TeamGroupForm, WebAdminUserCreationForm
from .models import TeamGroup


def frontend_redirect():
    return redirect('/')


def user_login(request):

    form = LoginForm()
    error = ""

    if request.method == "POST":

        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            if role == 'admin':
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    return redirect('web_admin_dashboard')

                error = "This user does not have admin access."

            elif user.role != role:
                error = "Selected role does not match user role."

            else:
                login(request, user)
                if user.is_superuser:
                    return redirect('web_admin_dashboard')

                if role == 'manager':
                    return redirect('manager_dashboard')

                elif role == 'tl':
                    return redirect('tl_dashboard')

                elif role == 'member':
                    return redirect('member_dashboard')

        else:
            error = "Invalid username or password."

    return render(
        request,
        'accounts/login.html',
        {
            'form': form,
            'error': error
        }
    )


def send_new_user_credentials(request, user, raw_password):
    debug_info = (
        f"HOST_USER='{settings.EMAIL_HOST_USER}' | "
        f"PWD_LEN={len(settings.EMAIL_HOST_PASSWORD)} | "
        f"HOST={settings.EMAIL_HOST} | "
        f"PORT={settings.EMAIL_PORT} | "
        f"USE_TLS={settings.EMAIL_USE_TLS}"
    )
    
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        messages.error(
            request,
            f'User was created, but email was not sent. Email not configured. DEBUG: {debug_info}'
        )
        return

    try:
        send_mail(
            subject='Your task management account has been created',
            message=(
                f'Hello {user.username},\n\n'
                'An account has been created for you in the task '
                'management system.\n\n'
                f'Username: {user.username}\n'
                f'Password: {raw_password}\n'
                f'Login URL: {request.build_absolute_uri("/")}\n\n'
                'Please log in using these credentials.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        messages.success(
            request,
            f'User created and credentials emailed to {user.email}.'
        )
    except Exception as error:
        messages.error(
            request,
            f'User was created, but email was not sent: {error}. DEBUG: {debug_info}'
        )


@login_required
def web_admin_dashboard(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    return frontend_redirect()


@login_required
def web_admin_add_user(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    if request.method == 'GET':
        return frontend_redirect()

    if request.method == 'POST':
        form = WebAdminUserCreationForm(request.POST)

        if form.is_valid():
            raw_password = form.cleaned_data['password1']
            user = form.save()
            send_new_user_credentials(request, user, raw_password)
            return redirect('web_admin_dashboard')

        messages.error(request, 'User could not be created. Please use the app form.')

    return frontend_redirect()


@login_required
def web_admin_delete_user(request, user_id):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    if request.method != 'POST':
        return redirect('web_admin_dashboard')

    User = get_user_model()
    user_obj = get_object_or_404(User, id=user_id)

    if user_obj == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('web_admin_dashboard')

    username = user_obj.username
    user_obj.delete()
    messages.success(request, f'User {username} deleted successfully.')

    return redirect('web_admin_dashboard')


@login_required
def web_admin_delete_group(request, group_id):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    if request.method != 'POST':
        return redirect('web_admin_dashboard')

    group = get_object_or_404(TeamGroup, id=group_id)
    group_name = group.name
    group.delete()
    messages.success(request, f'Group {group_name} deleted successfully.')

    return redirect('web_admin_dashboard')


@login_required
def web_admin_create_group(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    if request.method != 'POST':
        return frontend_redirect()

    form = TeamGroupForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Group created successfully.')
        return redirect('web_admin_dashboard')

    messages.error(request, 'Group could not be created. Please use the app form.')
    return frontend_redirect()


def user_logout(request):

    logout(request)

    return redirect('login')


@login_required
def manager_dashboard(request):

    if request.user.role != 'manager' and not request.user.is_superuser:
        return redirect('login')

    return frontend_redirect()


@login_required
def tl_dashboard(request):

    if request.user.role != 'tl' and not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    return frontend_redirect()


@login_required
def member_dashboard(request):

    if request.user.role != 'member' and not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    return frontend_redirect()
