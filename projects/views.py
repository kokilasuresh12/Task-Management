from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project


def create_project(request):

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


def project_list(request):

    projects = Project.objects.all()

    return render(
        request,
        'projects/project_list.html',
        {'projects': projects}
    )

def manager_report(request):

    projects = Project.objects.all()

    return render(
        request,
        'projects/report.html',
        {'projects': projects}
    )