from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
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
                    return redirect('/admin/')

                error = "This user does not have admin access."

            elif user.role != role:
                error = "Selected role does not match user role."

            else:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin/')

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

    if request.user.role != 'tl':
        return redirect('login')

    projects = Project.objects.filter(
        assigned_tl=request.user
    )

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
        }
    )


@login_required
def member_dashboard(request):

    if request.user.role != 'member':
        return redirect('login')

    user = request.user

    assigned_tasks = Task.objects.filter(
        assigned_member=user
    )

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
    }

    return render(
        request,
        'accounts/member_dashboard.html',
        context
    )
