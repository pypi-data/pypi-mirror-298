# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import include, path
from apps.home import views as home_views
from apps.authentication import views as auth_views

from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

# URL Patterns for the application

urlpatterns =[

    # The home page
    # URL: /
    # View: home_views.index
    # This route directs to the home page of the application.
    path('', home_views.index, name='home'),

    # User Profile page
    # URL: /user/profile
    # View: home_views.profile
    # This route directs to the user's profile page.
    # path('user/profile', home_views.profile, name='profile'),

    # Edit User Profile page
    # URL: /user/edit-profile
    # View: home_views.edit_profile
    # This route allows the user to edit their profile.

    # Change Password page
    # URL: /user/account-settings/change-password
    # View: home_views.UserPasswordChangeView.as_view()
    # This route allows the user to change their account password.
    # path('user/account-settings/change-password', home_views.UserPasswordChangeView.as_view(), name='change_password'),
    # path('user/account-settings/edit-profile', home_views.edit_profile_settings, name='edit_profile_settings'),
    # path('user/account-settings/user-information', home_views.user_information, name='user_information'),

    # path('organization/teams/list', home_views.team_member_list, name='team_member_list'),
    # path('organization/teams/invite-team-member', home_views.invite_team_member, name='invite_team_member'),
    # path('organization/teams/invites', home_views.team_invites, name='team_invites'),
    # path('organization/settings/message-templates', home_views.message_templates, name='message_templates'),
    # path('organization/settings/oganization-details', home_views.organization_details, name='organization_details'),
    # path('invite/<uidb64>/<token>/', home_views.user_invitation, name='user_invitation'),
]

# Serve static files during development
# Static files are served via the `static` function from `django.conf.urls.static`
# with settings defined in `settings.py`.
