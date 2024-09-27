
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#DJANGO Imports
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template import loader
from django.utils.http import urlsafe_base64_decode

from .models import UserProfile, Tenant

from core import shortcuts as CORE_SHORTCUTS

import html

from core.middleware import HandleHTTPErrorsMiddleware

from django.utils.translation import gettext_lazy as _


middleware = HandleHTTPErrorsMiddleware(get_response=None)

@login_required(login_url="/login/")
def profile(request):
    """
    View function for user profile page.
    Requires the user to be logged in. If the user is not logged in, they will be redirected to the login page.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template for the user profile page.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)

        context = {'title': _('Profile') ,'segment': {'text': _('Profile Details'), 'url': 'profile'}, 'profile': profile}

        html_template = loader.get_template('pages/accounts/index.html')
        return HttpResponse(html_template.render(context, request))
    
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)
