# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import include, path
from apps.invites import views as invites_views
from apps.authentication import views as auth_views

from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns


urlpatterns =[
    path('organization/teams/invite-team-member', invites_views.invite_team_member, name='invite_team_member'),
    path('organization/teams/invites', invites_views.team_invites, name='team_invites'),
    path('invite/<uidb64>/<token>/', invites_views.user_invitation, name='user_invitation'),
]