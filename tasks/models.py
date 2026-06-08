from django.db import models
from django.conf import settings
from projects.models import Project


class Task(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted for Review'),
        ('completed', 'Completed'),
    )

    task_name = models.CharField(max_length=100)

    description = models.TextField()

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    assigned_member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'member'}
    )

    deadline = models.DateField()

    progress = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


class ProgressUpdate(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    progress = models.IntegerField()

    comment = models.TextField()

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.task.task_name
