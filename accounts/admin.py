
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.core.mail import send_mail
from .models import User

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
