from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from .models import Project


@login_required
def create_project(request):

    if request.user.role != 'manager' and not request.user.is_superuser:
        return redirect('login')

    if request.method == 'POST':

        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('project_list')

    else:
        form = ProjectForm()

    return render(
        request,
        'projects/create_project.html',
        {'form': form}
    )


@login_required
def project_list(request):

    if request.user.role == 'tl':
        projects = Project.objects.filter(
            assigned_tl=request.user
        )
    else:
        projects = Project.objects.all()

    return render(
        request,
        'projects/project_list.html',
        {'projects': projects}
    )

@login_required
def manager_report(request):

    if request.user.role != 'manager' and not request.user.is_superuser:
        return redirect('login')

    projects = Project.objects.prefetch_related('task_set').all()

    return render(
        request,
        'projects/report.html',
        {'projects': projects}
    )


@login_required
def update_project_status(request, project_id):

    if request.user.role != 'tl':
        return redirect('login')

    project = get_object_or_404(
        Project,
        id=project_id,
        assigned_tl=request.user
    )

    if request.method == 'POST':
        status = request.POST.get('status')

        valid_statuses = [
            choice[0]
            for choice in Project.STATUS_CHOICES
        ]

        if status in valid_statuses:
            project.status = status
            project.save(update_fields=['status'])

    return redirect('tl_dashboard')
