# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import include, path
from apps.accounts import views as accounts_views
from apps.authentication import views as auth_views

from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

# URL Patterns for the application

urlpatterns =[
    path('accounts/profile/details', accounts_views.profile, name='profile'),
]
