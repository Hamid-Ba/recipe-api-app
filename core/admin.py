"""Admin Panel"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdminModel

from core import models

class UserAdmin(BaseAdminModel):
    """User Admin"""
    list_display = ["email","name"]
    ordering = ["id"]

admin.site.register(models.User, UserAdmin)