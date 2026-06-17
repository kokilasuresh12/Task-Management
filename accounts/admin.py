
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.core.mail import send_mail
import logging

from .models import TeamGroup, TeamGroupLeader, TeamGroupMember, User

logger = logging.getLogger(__name__)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Additional information',
            {
                'fields': (
                    'role',
                    'phone_number',
                    'dob',
                    'age',
                    'salary',
                    'address',
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Additional information',
            {
                'fields': (
                    'email',
                    'role',
                    'phone_number',
                    'dob',
                    'age',
                    'salary',
                    'address',
                )
            },
        ),
    )

    list_display = (
        'username',
        'role',
        'email',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj is None and 'email' in form.base_fields:
            form.base_fields['email'].required = True

        return form

    def save_model(self, request, obj, form, change):
        raw_password = None

        if not change:
            raw_password = form.cleaned_data.get('password1')

        super().save_model(request, obj, form, change)

        if not change and obj.email and raw_password:
            login_url = request.build_absolute_uri('/')
            
            # Debug: Log the actual values
            logger.info(f"DEBUG - EMAIL_HOST_USER: '{settings.EMAIL_HOST_USER}'")
            logger.info(f"DEBUG - EMAIL_HOST_PASSWORD length: {len(settings.EMAIL_HOST_PASSWORD)}")
            logger.info(f"DEBUG - EMAIL_HOST: '{settings.EMAIL_HOST}'")
            logger.info(f"DEBUG - EMAIL_PORT: {settings.EMAIL_PORT}")
            logger.info(f"DEBUG - EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")

            if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                self.message_user(
                    request,
                    'User was created, but email was not sent. '
                    'EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are required.',
                    level=messages.ERROR,
                )
                logger.error("DEBUG - Email check failed: HOST_USER or PASSWORD is empty")
                return

            try:
                send_mail(
                    subject='Your task management account has been created',
                    message=(
                        f'Hello {obj.username},\n\n'
                        'An account has been created for you in the task '
                        'management system.\n\n'
                        f'Username: {obj.username}\n'
                        f'Password: {raw_password}\n'
                        f'Login URL: {login_url}\n\n'
                        'Please log in using these credentials.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )
                self.message_user(
                    request,
                    f'Login credentials were emailed to {obj.email}.',
                    level=messages.SUCCESS,
                )
                logger.info(f"DEBUG - Email sent successfully to {obj.email}")
            except Exception as error:
                self.message_user(
                    request,
                    f'User was created, but email was not sent: {error}',
                    level=messages.ERROR,
                )
                logger.error(f"DEBUG - Email sending failed: {error}")
                    level=messages.ERROR,
                )


class TeamGroupLeaderInline(admin.TabularInline):
    model = TeamGroupLeader
    extra = 1


class TeamGroupMemberInline(admin.TabularInline):
    model = TeamGroupMember
    extra = 1


@admin.register(TeamGroup)
class TeamGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'created_at')
    list_filter = ('manager',)
    search_fields = ('name', 'manager__username')
    inlines = (TeamGroupLeaderInline, TeamGroupMemberInline)
