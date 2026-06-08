
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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
