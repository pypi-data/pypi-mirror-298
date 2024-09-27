# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.tenant import views as tenant_views

# URL Patterns for the application

urlpatterns =[
    path('organization/teams/list', tenant_views.team_member_list, name='team_member_list'),
]