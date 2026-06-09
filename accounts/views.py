from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .forms import LoginForm, TeamGroupForm, WebAdminUserCreationForm
from .models import TeamGroup, TeamGroupMember
from projects.models import Project
from tasks.models import Task

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
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        messages.error(
            request,
            'User was created, but email was not sent. '
            'EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are required.'
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
            f'User was created, but email was not sent: {error}'
        )


@login_required
def web_admin_dashboard(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    User = get_user_model()
    users = User.objects.order_by('role', 'username')
    groups = TeamGroup.objects.select_related(
        'manager'
    ).prefetch_related(
        'leader_assignments__team_leader',
        'member_assignments__team_leader',
        'member_assignments__member'
    ).order_by('name')

    context = {
        'total_users': users.count(),
        'managers': users.filter(role='manager').count(),
        'team_leaders': users.filter(role='tl').count(),
        'members': users.filter(role='member').count(),
        'users': users,
        'groups': groups,
    }

    return render(
        request,
        'accounts/web_admin_dashboard.html',
        context
    )


@login_required
def web_admin_add_user(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    if request.method == 'POST':
        form = WebAdminUserCreationForm(request.POST)

        if form.is_valid():
            raw_password = form.cleaned_data['password1']
            user = form.save()
            send_new_user_credentials(request, user, raw_password)
            return redirect('web_admin_dashboard')

    else:
        form = WebAdminUserCreationForm()

    return render(
        request,
        'accounts/web_admin_add_user.html',
        {
            'form': form
        }
    )


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

    if request.method == 'POST':
        form = TeamGroupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Group created successfully.')
            return redirect('web_admin_dashboard')

    else:
        form = TeamGroupForm()

    team_leader_member_fields = []
    allocation_rows = []

    for team_leader in form.fields['team_leaders'].queryset:
        team_leader_member_fields.append(
            {
                'team_leader': team_leader,
                'field': form[f'members_for_tl_{team_leader.id}'],
            }
        )

    if request.method == 'POST':
        for team_leader_id in request.POST.getlist('team_leaders'):
            member_ids = [
                int(member_id)
                for member_id in request.POST.getlist(f'members_for_tl_{team_leader_id}')
                if member_id.isdigit()
            ]

            allocation_rows.append(
                {
                    'team_leader_id': team_leader_id,
                    'member_ids': member_ids,
                }
            )

    if not allocation_rows:
        allocation_rows.append(
            {
                'team_leader_id': '',
                'member_ids': [],
            }
        )

    allocated_members = {
        assignment.member_id: assignment.group.name
        for assignment in TeamGroupMember.objects.select_related('group')
    }
    member_options = []

    for member in get_user_model().objects.filter(
        role='member'
    ).order_by('username'):
        member_options.append(
            {
                'id': member.id,
                'username': member.username,
                'allocated_group': allocated_members.get(member.id),
            }
        )

    return render(
        request,
        'accounts/web_admin_create_group.html',
        {
            'form': form,
            'team_leader_member_fields': team_leader_member_fields,
            'team_leaders': form.fields['team_leaders'].queryset,
            'member_options': member_options,
            'available_members': (
                form.fields[
                    f'members_for_tl_{form.fields["team_leaders"].queryset.first().id}'
                ].queryset
                if form.fields['team_leaders'].queryset.exists()
                else []
            ),
            'allocation_rows': allocation_rows,
        }
    )


def user_logout(request):

    logout(request)

    return redirect('login')


@login_required
def manager_dashboard(request):

    if request.user.role != 'manager' and not request.user.is_superuser:
        return redirect('login')

    total_projects = Project.objects.count()

    completed_projects = Project.objects.filter(
        status='completed'
    ).count()

    pending_projects = Project.objects.filter(
        status='pending'
    ).count()

    total_tasks = Task.objects.count()

    completed_tasks = Task.objects.filter(
        status='completed'
    ).count()

    context = {
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'pending_projects': pending_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    }

    return render(
        request,
        'accounts/manager_dashboard.html',
        context
    )


@login_required
def tl_dashboard(request):

    if request.user.role != 'tl' and not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    if request.user.role == 'tl':
        projects = Project.objects.filter(
            assigned_tl=request.user
        )
        page_subtitle = 'Your assigned projects and review queue'
    else:
        projects = Project.objects.all()
        page_subtitle = 'Admin view of all team leader work'

    tasks = Task.objects.filter(
        project__assigned_tl=request.user
    )

    submitted_tasks = tasks.filter(
        status='submitted'
    )

    return render(
        request,
        'accounts/tl_dashboard.html',
        {
            'projects': projects,
            'total_projects': projects.count(),
            'total_tasks': tasks.count(),
            'submitted_tasks': submitted_tasks.count(),
            'review_tasks': submitted_tasks,
            'project_status_choices': Project.STATUS_CHOICES,
            'page_subtitle': page_subtitle,
        }
    )


@login_required
def member_dashboard(request):

    if request.user.role != 'member' and not request.user.is_staff and not request.user.is_superuser:
        return redirect('login')

    if request.user.role == 'member':
        assigned_tasks = Task.objects.filter(
            assigned_member=request.user
        )
        page_subtitle = 'Your assigned task progress'
    else:
        assigned_tasks = Task.objects.filter(
            assigned_member__role='member'
        )
        page_subtitle = 'Admin view of all team member work'

    total_tasks = assigned_tasks.count()

    completed_tasks = assigned_tasks.filter(
        status='completed'
    ).count()

    pending_tasks = assigned_tasks.exclude(
        status='completed'
    ).count()

    review_tasks = assigned_tasks.filter(
        status='submitted'
    )

    if total_tasks > 0:
        progress_percentage = int(
            (completed_tasks / total_tasks) * 100
        )
    else:
        progress_percentage = 0

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress_percentage': progress_percentage,
        'review_tasks': review_tasks,
        'page_subtitle': page_subtitle,
    }

    return render(
        request,
        'accounts/member_dashboard.html',
        context
    )
