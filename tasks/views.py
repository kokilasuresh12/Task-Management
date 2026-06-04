from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, ProgressUpdate
from .forms import TaskForm, ProgressForm


# CREATE TASK (TL)

def create_task(request):

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})


# TASK LIST

def task_list(request):

    tasks = Task.objects.all()

    return render(request, 'tasks/task_list.html', {'tasks': tasks})




def member_tasks(request):

    tasks = Task.objects.filter(
        assigned_member=request.user
    )

    return render(
        request,
        'tasks/member_tasks.html',
        {'tasks': tasks}
    )


def update_progress(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method == 'POST':

        form = ProgressForm(request.POST)

        if form.is_valid():

            update = form.save(commit=False)

            update.task = task

            update.save()

            task.progress = update.progress

            if update.progress == 100:
                task.status = 'completed'

            elif update.progress > 0:
                task.status = 'in_progress'

            task.save()

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


def progress_history(request, task_id):

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