# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from apps.tenant.models import Tenant, TenantLanguages, ContractStatus, SubscriptionPlan

admin.site.register(ContractStatus)

class TenantAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Tenant model.
    - list_display: Specifies the fields to display in the admin list view.
    - list_filter: Adds filtering options for the specified fields.
    - search_fields: Allows searching by specified fields.
    """
    list_display = ("company_name", "contract_status", "primary_account_name", "primary_account_email")
    list_filter = ("contract_status",)
    search_fields = ("company_name",)

class TenantLanguageAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the TenantLanguages model.
    - list_display: Specifies the fields to display in the admin list view.
    - list_filter: Adds filtering options for the specified fields.
    """
    list_display = ("tenant", "language",)
    list_filter = ("language", "tenant")

admin.site.register(Tenant, TenantAdmin)
admin.site.register(TenantLanguages, TenantLanguageAdmin)

admin.site.register(SubscriptionPlan)