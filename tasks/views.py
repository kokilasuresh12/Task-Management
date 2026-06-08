from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, ProgressUpdate
from .forms import TaskForm, ProgressForm


# CREATE TASK (TL)

def update_project_status(project):
    tasks = project.task_set.all()

    if tasks.exists() and not tasks.exclude(status='completed').exists():
        project.status = 'completed'
    elif tasks.exists():
        project.status = 'in_progress'
    else:
        project.status = 'pending'

    project.save(update_fields=['status'])


@login_required
def create_task(request):

    if request.user.role != 'tl':
        return redirect('login')

    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm(user=request.user)

    return render(request, 'tasks/create_task.html', {'form': form})


# TASK LIST

@login_required
def task_list(request):

    if request.user.role == 'tl':
        tasks = Task.objects.filter(
            project__assigned_tl=request.user
        )
    elif request.user.role == 'manager' or request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        return redirect('member_tasks')

    return render(request, 'tasks/task_list.html', {'tasks': tasks})



@login_required
def member_tasks(request):

    if request.user.role != 'member':
        return redirect('login')

    tasks = Task.objects.filter(
        assigned_member=request.user
    )

    return render(
        request,
        'tasks/member_tasks.html',
        {'tasks': tasks}
    )


@login_required
def update_progress(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        assigned_member=request.user
    )

    if request.method == 'POST':

        form = ProgressForm(request.POST)

        if form.is_valid():

            update = form.save(commit=False)

            update.task = task

            update.save()

            task.progress = update.progress

            if update.progress >= 100:
                task.progress = 100
                task.status = 'submitted'

            elif update.progress > 0:
                task.status = 'in_progress'

            task.save()
            update_project_status(task.project)

            return redirect('member_tasks')

    else:

        form = ProgressForm()

    return render(
        request,
        'tasks/update_progress.html',
        {
            'form': form,
            'task': task
        }
    ) 


@login_required
def progress_history(request, task_id):

    if request.user.role == 'member':
        task = get_object_or_404(
            Task,
            id=task_id,
            assigned_member=request.user
        )
    elif request.user.role == 'tl':
        task = get_object_or_404(
            Task,
            id=task_id,
            project__assigned_tl=request.user
        )
    else:
        task = get_object_or_404(
            Task,
            id=task_id
        )

    updates = ProgressUpdate.objects.filter(
        task=task
    ).order_by('-updated_at')

    return render(
        request,
        'tasks/progress_history.html',
        {
            'task': task,
            'updates': updates
        }
    )


@login_required
def approve_task(request, task_id):

    if request.user.role != 'tl':
        return redirect('login')

    task = get_object_or_404(
        Task,
        id=task_id,
        project__assigned_tl=request.user,
        status='submitted'
    )

    if request.method == 'POST':
        task.status = 'completed'
        task.progress = 100
        task.save(update_fields=['status', 'progress'])
        update_project_status(task.project)

    return redirect('task_list')
