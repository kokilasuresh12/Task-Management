from django.db import models
from accounts.models import User
from projects.models import Project


class Task(models.Model):

    TASK_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    task_name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    assigned_member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'member'}
    )

    deadline = models.DateField()

    progress = models.IntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.task_name
    
class ProgressUpdate(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    comment = models.TextField()

    progress_percentage = models.IntegerField()

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.task.task_name    