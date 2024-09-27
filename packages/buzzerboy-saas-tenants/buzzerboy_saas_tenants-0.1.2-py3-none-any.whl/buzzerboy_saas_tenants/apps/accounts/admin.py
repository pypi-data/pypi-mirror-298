# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from apps.accounts.models import  UserType, UserTypeAccess, UserProfile

admin.site.register(UserType)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the UserProfile model.
    - list_display: Specifies the fields to display in the admin list view.
    - list_filter: Adds filtering options for the specified fields.
    """
    list_display = ("user_object", "tenant", "user_type",)
    list_filter = ("user_type", "tenant")

class UserTypeAccessAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the UserTypeAccess model.
    - list_display: Specifies the fields to display in the admin list view.
    - list_filter: Adds filtering options for the specified fields.
    """
    list_display = ("user_type", "request_path", "access_key")
    list_filter = ("user_type", "request_path", "access_key")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserTypeAccess, UserTypeAccessAdmin)
