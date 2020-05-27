from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields":
                    (
                        "avatar",
                        "language",
                        "bio",
                        "birthdate",
                        "currency",
                        "superhost",
                    )
            },
        ),
    )

    list_filter = (
            UserAdmin.list_filter + (
        "superhost",
    )
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verify",
    )
