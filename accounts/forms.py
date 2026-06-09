from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import TeamGroup, TeamGroupMember


class LoginForm(forms.Form):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('tl', 'Team Leader'),
        ('member', 'Team Member'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect
    )

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Username'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password'
            }
        )
    )


class WebAdminUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()

        fields = [
            'username',
            'email',
            'role',
            'phone_number',
            'dob',
            'age',
            'salary',
            'address',
        ]

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            raise forms.ValidationError('Email is required.')

        return email

    def clean_password1(self):
        password = self.cleaned_data['password1']
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class TeamGroupForm(forms.ModelForm):

    team_leaders = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.filter(role='tl').order_by('username'),
        widget=forms.SelectMultiple,
        label='Team Leaders'
    )

    class Meta:
        model = TeamGroup

        fields = [
            'name',
            'manager',
            'team_leaders',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        User = get_user_model()

        self.fields['manager'].queryset = User.objects.filter(
            role='manager'
        ).order_by('username')

        self.fields['team_leaders'].queryset = User.objects.filter(
            role='tl'
        ).order_by('username')

        members = User.objects.filter(
            role='member',
            group_member_assignments__isnull=True
        ).order_by('username')

        for team_leader in self.fields['team_leaders'].queryset:
            self.fields[f'members_for_tl_{team_leader.id}'] = (
                forms.ModelMultipleChoiceField(
                    queryset=members,
                    required=False,
                    widget=forms.SelectMultiple,
                    label=f'Members for {team_leader.username}'
                )
            )

    def clean_team_leaders(self):
        team_leaders = self.cleaned_data['team_leaders']

        if not team_leaders:
            raise forms.ValidationError(
                'Select at least one team leader.'
            )

        return team_leaders

    def clean(self):
        cleaned_data = super().clean()
        team_leaders = cleaned_data.get('team_leaders')
        assigned_members = set()

        if not team_leaders:
            return cleaned_data

        for team_leader in team_leaders:
            field_name = f'members_for_tl_{team_leader.id}'

            for member in cleaned_data.get(field_name, []):
                if member.id in assigned_members:
                    self.add_error(
                        field_name,
                        'A team member can be assigned to only one TL in this group.'
                    )
                assigned_members.add(member.id)

        already_allocated = TeamGroupMember.objects.filter(
            member_id__in=assigned_members
        ).select_related('member', 'group')

        if already_allocated.exists():
            allocated_names = ', '.join(
                f'{assignment.member.username} ({assignment.group.name})'
                for assignment in already_allocated
            )
            raise forms.ValidationError(
                f'These team members are already allocated to another group: {allocated_names}.'
            )

        return cleaned_data

    def save(self, commit=True):
        group = super().save(commit=False)

        if commit:
            group.save()
            team_leaders = self.cleaned_data['team_leaders']
            group.team_leaders.set(team_leaders)
            group.member_assignments.all().delete()

            for team_leader in team_leaders:
                field_name = f'members_for_tl_{team_leader.id}'

                for member in self.cleaned_data.get(field_name, []):
                    TeamGroupMember.objects.create(
                        group=group,
                        team_leader=team_leader,
                        member=member
                    )

        return group
