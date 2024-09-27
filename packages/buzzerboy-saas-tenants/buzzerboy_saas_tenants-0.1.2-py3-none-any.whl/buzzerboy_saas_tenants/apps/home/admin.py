# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from apps.tenant.models import (
    Tenant, SupportedLanguage, Country, StateProvince, TenantLanguages, ContractStatus
)

from apps.invites.models import (
    Invites
)

from apps.accounts.models import (
    UserType, UserTypeAccess, UserProfile
)

from apps.localization.models import (
    Timezone, Country, StateProvince, SupportedLanguage
)

# Simple Registration
# The following models are registered with the default admin interface, 
# which provides basic LCRUD operations without any customization.
#admin.site.register(Invites)

#admin.site.register(Timezone) --> already declared in localization

#admin.site.register(ContractStatus)


#admin.site.register(SupportedLanguage) --> already declared in localization

#admin.site.register(CustomTranslation) #### --- cant find where this is @AliBacelonia

#admin.site.register(UserType)

# admin.site.register(Country)

# Detailed and Complex UI Registration
# These models are registered with customized admin interfaces to enhance 
# the user experience by adding search, filters, and custom display fields.

#class StateProvinceAdmin(admin.ModelAdmin):
#    """
#    Custom admin interface for the StateProvince model.
#    - list_display: Specifies the fields to display in the admin list view.
#    - list_filter: Adds filtering options for the specified fields.
#    - search_fields: Allows searching by specified fields.
#    """
#    list_display = ("location_name", "country")
#    list_filter = ("country",)
#    search_fields = ("location_name", "country")

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

class UserProfileAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the UserProfile model.
    - list_display: Specifies the fields to display in the admin list view.
    - list_filter: Adds filtering options for the specified fields.
    """
    list_display = ("user_object", "tenant", "user_type",)
    list_filter = ("user_type", "tenant")

class TenantLanguageAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the TenantLanguages model.
    - list_display: Specifies the fields to display in the admin list view.
    - list_filter: Adds filtering options for the specified fields.
    """
    list_display = ("tenant", "language",)
    list_filter = ("language", "tenant")

class UserTypeAccessAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the UserTypeAccess model.
    - list_display: Specifies the fields to display in the admin list view.
    - list_filter: Adds filtering options for the specified fields.
    """
    list_display = ("user_type", "request_path", "access_key")
    list_filter = ("user_type", "request_path", "access_key")

# Registering the models with the customized admin interfaces.
#admin.site.register(StateProvince, StateProvinceAdmin)
#admin.site.register(Tenant, TenantAdmin)
#admin.site.register(UserProfile, UserProfileAdmin)
#admin.site.register(TenantLanguages, TenantLanguageAdmin)
#admin.site.register(UserTypeAccess, UserTypeAccessAdmin)
