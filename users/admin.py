from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdminConfig(UserAdmin):
    """User config for Admin Dashboard."""

    ordering = ["id"]
    list_filter = ["id"]
    list_display = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("email",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        None,
        {"classes": ("wide",), "fields": ("email", "password1", "password2")},
    )
