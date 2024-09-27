# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.account_settings import views as account_settings_views

urlpatterns =[
    path('user/account-settings/change-password', account_settings_views.UserPasswordChangeView.as_view(), name='change_password'),
    path('user/account-settings/edit-profile', account_settings_views.edit_profile_settings, name='edit_profile_settings'),
    path('user/account-settings/user-information', account_settings_views.user_information, name='user_information')
]
