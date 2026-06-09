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


class TeamGroup(models.Model):

    name = models.CharField(max_length=150)

    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_groups',
        limit_choices_to={'role': 'manager'}
    )

    team_leaders = models.ManyToManyField(
        User,
        through='TeamGroupLeader',
        related_name='team_groups',
        limit_choices_to={'role': 'tl'}
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamGroupLeader(models.Model):

    group = models.ForeignKey(
        TeamGroup,
        on_delete=models.CASCADE,
        related_name='leader_assignments'
    )

    team_leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_leader_assignments',
        limit_choices_to={'role': 'tl'}
    )

    class Meta:
        unique_together = ('group', 'team_leader')

    def __str__(self):
        return f'{self.group} - {self.team_leader}'


class TeamGroupMember(models.Model):

    group = models.ForeignKey(
        TeamGroup,
        on_delete=models.CASCADE,
        related_name='member_assignments'
    )

    team_leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_group_members',
        limit_choices_to={'role': 'tl'}
    )

    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_member_assignments',
        limit_choices_to={'role': 'member'}
    )

    class Meta:
        unique_together = ('group', 'member')

    def __str__(self):
        return f'{self.member} under {self.team_leader}'
