from django import forms
from django.contrib.auth import get_user_model
from .models import Task, ProgressUpdate


class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and getattr(user, 'role', None) == 'tl':
            self.fields['project'].queryset = self.fields['project'].queryset.filter(
                assigned_tl=user
            )

        self.fields['assigned_member'].queryset = get_user_model().objects.filter(
            role='member'
        )

    class Meta:
        model = Task

        fields = [
            'task_name',
            'description',
            'project',
            'assigned_member',
            'deadline',
        ]


class ProgressForm(forms.ModelForm):

    def clean_progress(self):
        progress = self.cleaned_data['progress']

        if progress < 0 or progress > 100:
            raise forms.ValidationError('Progress must be between 0 and 100.')

        return progress

    class Meta:
        model = ProgressUpdate

        fields = [
            'progress',
            'comment'
        ]

        widgets = {
            'progress': forms.NumberInput(
                attrs={
                    'min': 0,
                    'max': 100,
                }
            )
        }
