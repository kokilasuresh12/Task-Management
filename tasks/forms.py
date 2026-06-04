from django import forms
from .models import Task, ProgressUpdate


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            'task_name',
            'project',
            'assigned_member',
            'deadline',
            'status'
        ]


class ProgressForm(forms.ModelForm):

    class Meta:
        model = ProgressUpdate

        fields = [
            'progress',
            'comment'
        ]