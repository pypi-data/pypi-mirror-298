
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#DJANGO Imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from apps.accounts.models import UserProfile

from apps.tenant.models import Tenant
from core import shortcuts as CORE_SHORTCUTS


from core.middleware import HandleHTTPErrorsMiddleware

from django.utils.translation import gettext_lazy as _


middleware = HandleHTTPErrorsMiddleware(get_response=None)

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """


    profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
    tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)

    context = {'title': _('Home') ,'segment': {'text': _('Dashboard'), 'url': 'home'}}
    

    html_template = loader.get_template('pages/index.html')
    return HttpResponse(html_template.render(context, request))
