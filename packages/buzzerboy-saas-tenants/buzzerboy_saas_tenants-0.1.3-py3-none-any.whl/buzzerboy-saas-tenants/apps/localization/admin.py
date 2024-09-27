# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from apps.localization.models import Timezone, SupportedLanguage, Country, StateProvince

admin.site.register(Timezone)
admin.site.register(SupportedLanguage)
admin.site.register(Country)

# Detailed and Complex UI Registration
# These models are registered with customized admin interfaces to enhance 
# the user experience by adding search, filters, and custom display fields.

class StateProvinceAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the StateProvince model.
    - list_display: Specifies the fields to display in the admin list view.
    - list_filter: Adds filtering options for the specified fields.
    - search_fields: Allows searching by specified fields.
    """
    list_display = ("location_name", "country")
    list_filter = ("country",)
    search_fields = ("location_name", "country")

# Registering the models with the customized admin interfaces.
admin.site.register(StateProvince, StateProvinceAdmin)
