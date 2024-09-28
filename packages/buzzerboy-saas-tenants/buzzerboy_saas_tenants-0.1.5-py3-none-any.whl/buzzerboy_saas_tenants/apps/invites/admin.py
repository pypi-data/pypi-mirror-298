# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from buzzerboy_saas_tenants.apps.invites.models import Invites

admin.site.register(Invites)
