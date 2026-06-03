from django.db import models
from accounts.models import User


class Project(models.Model):

    PROJECT_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    project_name = models.CharField(max_length=100)

    description = models.TextField()

    assigned_tl = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'tl'}
    )

    deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=PROJECT_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.project_name
