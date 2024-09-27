
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#DJANGO Imports
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_str  # Use force_str instead of force_text
from django.utils.http import urlsafe_base64_decode

from apps.accounts.models import UserProfile
from apps.invites.forms import InvitesForm
from apps.tenant.models import Tenant
from core.utils import save_audit_log


from .models import Invites

from core import shortcuts as CORE_SHORTCUTS

import html

from core.middleware import HandleHTTPErrorsMiddleware

from django.utils.translation import gettext_lazy as _


middleware = HandleHTTPErrorsMiddleware(get_response=None)

@login_required(login_url="/login/")
def team_invites(request):
    """
    View function for user profile page.
    Requires the user to be logged in. If the user is not logged in, they will be redirected to the login page.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template for the user profile page.
    """

    my_user_profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
    tenant = CORE_SHORTCUTS.GetUserTenant(my_user_profile, Tenant)

    try:
        team_invite_list = tenant.invites.all()

        if request.method == 'POST':
            if 'delete_template_id' in request.POST:
                pass
            elif 'update_template_id' in request.POST:
                pass
            else:
                form = InvitesForm(request.POST, tenant=my_user_profile.tenant)
                if form.is_valid():
                    try:

                        # Save the form and handle email sending
                        form.save()
                        
                        messages.success(request, _('Invite sent successfully!'))
                        return redirect(reverse_lazy('team_invites'))
                    except forms.ValidationError as e:
                        if hasattr(e, 'message'):
                            print(str(e.message))
                            messages.error(request, f'{str(e.message)}')
                        else:
                            print(str(e))
                            messages.error(request, f'{str(e)}')    
                        return redirect(reverse_lazy('team_invites'))
                    except Exception as e:
                        if hasattr(e, 'message'):
                            print(str(e.message))
                            messages.error(request, f'{str(e.message)}')
                        else:
                            print(str(e))
                            messages.error(request, f'{str(e)}')
                        return redirect(reverse_lazy('team_invites'))
                else:
                    print(form.errors)
                    messages.error(request, _('Error in form submission. Please correct the errors.'))
                    return redirect(reverse_lazy('team_invites'))
        else:
            form = InvitesForm(tenant=my_user_profile.tenant)

        context = {
            'form': form,
            'title': _('Team'),
            'segment': {
                'text': _('Team Invites'), 
                'url': 'team_invites'
            }, 
            'team_invite_list': team_invite_list 
        }

        return render(request, 'pages/teams/invites.html', context)
    
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

@login_required(login_url="/login/")
def invite_team_member(request):
    """
    View function for user profile page.
    Requires the user to be logged in. If the user is not logged in, they will be redirected to the login page.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template for the user profile page.
    """

    my_user_profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
    tenant = CORE_SHORTCUTS.GetUserTenant(my_user_profile, Tenant)

    try:

        if request.method == 'POST':
            if 'delete_template_id' in request.POST:
                pass
            elif 'update_template_id' in request.POST:
                pass
            else:
                form = InvitesForm(request.POST, tenant=my_user_profile.tenant)
                if form.is_valid():
                    try:
                        if form.has_changed():  # Check if any fields have been updated
                            # Get list of changed fields
                            changed_fields = form.changed_data  
                            
                            # Save the form and handle email sending in InvitesForm
                            form.save()
                            messages.success(request, _('Invite sent successfully!'))

                            save_audit_log(tenant=tenant, activity="Invited a team member", module="Invite Team Member", performed_by=my_user_profile, details=changed_fields)
                        else:
                            messages.info(request, _("No changes detected."))

                        if form.cleaned_data['email'] == my_user_profile.user_object.email:
                            messages.error(request, _("You can't invite yourself to the team since you're already part of it."))
                            return redirect(reverse_lazy('invite_team_member'))

                        
                        return redirect(reverse_lazy('team_invites'))
                    except forms.ValidationError as e:
                        if hasattr(e, 'message'):
                            print(str(e.message))
                            messages.error(request, f'{str(e.message)}')
                        else:
                            print(str(e))
                            messages.error(request, f'{str(e)}')    
                        return redirect(reverse_lazy('invite_team_member'))
                    except Exception as e:
                        if hasattr(e, 'message'):
                            print(str(e.message))
                            messages.error(request, f'{str(e.message)}')
                        else:
                            print(str(e))
                            messages.error(request, f'{str(e)}')
                        return redirect(reverse_lazy('invite_team_member'))
                else:
                    messages.error(request, f"{form.errors}")
                    return redirect(reverse_lazy('invite_team_member'))
        else:
            form = InvitesForm(tenant=my_user_profile.tenant)

        context = {
            'form': form,
            'title': _("Team"),
            'segment': {
                'text': _("Invite Team Member"), 
                'url': 'invite_team_member'
            }
        }

        return render(request, 'pages/teams/invite_form.html', context)
    
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

def user_invitation(request, uidb64, token):
    try:
        # Decode user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        
        # Fetch the user object
        user = User.objects.get(pk=uid)

        has_password = True if user.password else False
        
        # Fetch the user profile
        profile = CORE_SHORTCUTS.GetUserProfile(user, UserProfile)

        try:
            invite = Invites.objects.get(email=profile.user_object.email, tenant=profile.tenant, status='pending')
        except:
            invite = None
        
        # Check if the token matches
        if profile.user_token == token:
            # Activate user or perform actions
            user.is_active = True
            user.save()

            if invite:
                invite.status = 'accepted'
                invite.save()
            
            # Clear the token after use
            profile.user_token = None if has_password else token
            profile.status = UserProfile.UserProfileStatus.ENABLED
            profile.save()

            context = {
                'type': 'success',
                'title': _('User successfully activated.'),
                'sub': _('The user has been successfully activated. You can now explore other sections of our site.'),
                'token' : token,
                'has_password': has_password

            }
            return render(request, 'pages/states/team_invite.html', context)
        else:
            context = {
                'type': 'danger',
                'title': _('Invalid user token'),
                'sub': _('The user token provided is invalid. Please double-check the token or request a new one to proceed.'),
                'token' : '',
                'has_password': has_password
            }
            return render(request, 'pages/states/team_invite.html', context)
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)

        return middleware.handle_http_error(request, status_code=500, message=message)
    except UserProfile.DoesNotExist:
        print("User Profile not exist")
        return middleware.handle_http_error(request, status_code=500, message=message)

