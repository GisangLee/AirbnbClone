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

