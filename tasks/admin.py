from django.contrib import admin
from .models import Task, ProgressUpdate, TaskSubmission

admin.site.register(Task)
admin.site.register(ProgressUpdate)
admin.site.register(TaskSubmission)
