from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('tl', 'Team Leader'),
        ('member', 'Team Member'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        null=True,
        blank=True
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )

    dob = models.DateField(
        null=True,
        blank=True
    )

    age = models.IntegerField(
        null=True,
        blank=True
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    address = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username