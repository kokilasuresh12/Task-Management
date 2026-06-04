from django.contrib import admin
from .models import Task, ProgressUpdate

admin.site.register(Task)
admin.site.register(ProgressUpdate)