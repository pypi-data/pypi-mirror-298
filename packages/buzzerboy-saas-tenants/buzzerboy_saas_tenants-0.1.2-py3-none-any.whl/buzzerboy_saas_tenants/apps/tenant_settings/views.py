
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#DJANGO Imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from apps.accounts.models import UserProfile
from apps.tenant.forms import TenantSubscriptionForm
from apps.tenant.models import SubscriptionPlan, Tenant
from apps.tenant_settings.models import BillingDetails, SupportCase
from core.utils import save_audit_log

from .forms import SupportCaseForm, TenantAddressForm, TenantBillingAndPaymentForm, EmailTemplateForm, TenantForm

from core import shortcuts as CORE_SHORTCUTS

from core.middleware import HandleHTTPErrorsMiddleware

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from apps.account_settings.forms import (
    NotificationPreferencesForm,
    NotificationChannelForm,
    NotificationSettingsForm,
    NotificationTypeForm,
    CustomTemplateForm
)
from apps.account_settings.models import (
    NotificationPreferences,
    NotificationChannel,
    NotificationSettings,
    NotificationType
)

middleware = HandleHTTPErrorsMiddleware(get_response=None)

@login_required(login_url="/login/")
def message_templates(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)
        
        if request.method == 'POST':
            form = EmailTemplateForm(request.POST, instance=tenant, user_profile=profile)
            if form.is_valid():
                if form.has_changed():  # Check if any fields have been updated
                    # Get list of changed fields
                    changed_fields = form.changed_data  
                    
                    # Save the updated form
                    form.save()
                    request.session['is_successful'] = True
                    messages.success(request, _("Successfully updated email templates."))

                    save_audit_log(tenant=tenant, activity="Updated message template", module="Message Template", performed_by=profile, details=changed_fields)
                else:
                    messages.info(request, _("No changes detected."))
                
                return redirect(reverse_lazy('message_templates'))
            else:
                messages.error(request, _("Please double-check your inputs. It seems some fields have errors."))
                request.session['is_successful'] = False
                print("Form errors:", form.errors)  # Debug line
        else:
            form = EmailTemplateForm(user_profile=profile, instance=tenant)

        context = {
            'form': form,
            'title': _('Settings'),
            'segment': {'text': _('Message Template'), 'url': 'message_templates'},
        }
        return render(request, 'pages/tenant_settings/message-template.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

@login_required(login_url="/login/")
def subscription_plans(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)
        plans = CORE_SHORTCUTS.GetPlans(SubscriptionPlan)
        if request.method == 'POST':
            form = TenantSubscriptionForm(request.POST, instance=tenant)
            context = {
                'form': form,
                'title': _('Settings'),
                'segment': {'text': _('Subscription Plans'), 'url': 'tenant_subscription_plans'},
                "plans": plans
            }
            if form.is_valid():
                if form.has_changed():  # Check if any fields have been updated
                    # Get list of changed fields
                    changed_fields = form.changed_data

                    # Save the updated form
                    form.save()
                    # Set the session flag to True
                    request.session['is_successful'] = True
                    messages.success(request, _("Successfully changed subscription plan."))

                    save_audit_log(tenant=tenant, activity="Updated subscription plan.", module="Subscription Plans", performed_by=profile, details=changed_fields)
                else:
                    messages.info(request, _("No changes detected."))

                return redirect(reverse_lazy('tenant_subscription_plans'))
            else:
                messages.error(request, _("Please double-check your inputs. It seems some fields have errors."))
                print("Form errors:", form.errors)  # Debug line
                return render(request, 'pages/tenant_settings/subscription-plans.html', context)
        else:
            form = TenantSubscriptionForm(instance=tenant)

        context = {
            'form': form,
            'title': _('Settings'),
            'segment': {'text': _('Subscription Plans'), 'url': 'tenant_subscription_plans'},
            "plans": plans,
            "current_plan": tenant.subscription_plan
        }
        return render(request, 'pages/tenant_settings/subscription-plans.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)


@login_required(login_url="/login/")
def billing_and_payment(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)

        try:
            billing_details = BillingDetails.objects.get(tenant=tenant)
        except ObjectDoesNotExist:
            billing_details = BillingDetails.objects.create(tenant=tenant)

        # Check for the session flag and pass it to the template
        is_successful = request.session.pop('is_successful', False)
        form = TenantBillingAndPaymentForm(request.POST, instance=billing_details)

        if request.method == 'POST':
            context = {
                'form': form,
                'is_successful': is_successful,
                'title': _('Settings'),
                'segment': {'text': _('Billing and Payment'), 'url': 'tenant_billing_and_payment'},
            }
            if form.is_valid():
                if form.has_changed():  # Check if any fields have been updated
                    # Get list of changed fields
                    changed_fields = form.changed_data  
                    
                    # Save the updated form
                    form.save()
                    # Set the session flag to True
                    request.session['is_successful'] = True
                    messages.success(request, _("Successfully updated billing details."))

                    save_audit_log(tenant=tenant, activity="Updated billing details", module="Billing and Payment", performed_by=profile, details=changed_fields)
                else:
                    messages.info(request, _("No changes detected."))

                
                return redirect(reverse_lazy('tenant_billing_and_payment'))
            else:
                messages.error(request, _("Please double-check your inputs. It seems some fields have errors."))
                print("Form errors:", form.errors)  # Debug line
                return render(request, 'pages/tenant_settings/billing-and-payment.html', context)
        else:
            form = TenantBillingAndPaymentForm(instance=billing_details)

        context = {
            'form': form,
            'title': _('Settings'),
                'segment': {'text': _('Billing and Payment'), 'url': 'tenant_billing_and_payment'},
        }
        return render(request, 'pages/tenant_settings/billing-and-payment.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

@login_required(login_url="/login/")
def user_management(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)
        team_mates = tenant.team.all() 

        if request.method == 'POST':
            
            form = EmailTemplateForm(request.POST, instance=tenant, user_profile=profile)
            if form.is_valid():
                form.save()
                request.session['is_successful'] = True
                return redirect(reverse_lazy('tenant_user_management'))
            else:
                request.session['is_successful'] = False
                print("Form errors:", form.errors)  # Debug line
        else:
            form = EmailTemplateForm(user_profile=profile, instance=tenant)

        context = {
            'form': form,
            'title': _('Settings'),
            'segment': {'text': _('User Management'), 'url': 'tenant_user_management'},
            'team_member_list': team_mates 
        }
        return render(request, 'pages/tenant_settings/user-management.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

@login_required(login_url="/login/")
def audit_trail(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)
        audit_logs = tenant.tenant_audit_logs.all().order_by('-timestamp')

        if request.method == 'POST':
            form = EmailTemplateForm(request.POST, instance=tenant, user_profile=profile)
            if form.is_valid():
                form.save()
                request.session['is_successful'] = True
                return redirect(reverse_lazy('tenant_audit_trail'))
            else:
                request.session['is_successful'] = False
                print("Form errors:", form.errors)  # Debug line
        else:
            form = EmailTemplateForm(user_profile=profile, instance=tenant)

        context = {
            'form': form,
            'title': _('Settings'),
            'segment': {'text': _('Audit Trail'), 'url': 'tenant_audit_trail'},
            'audit_logs': audit_logs 
        }
        return render(request, 'pages/tenant_settings/audit-trail.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

@login_required(login_url="/login/")
def notifications(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)

        # Get or create related objects
        preferences, created = NotificationPreferences.objects.get_or_create(user=request.user)
        channels, created = NotificationChannel.objects.get_or_create(user=request.user)
        settings, created = NotificationSettings.objects.get_or_create(user=request.user)
        types, created = NotificationType.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            # Initialize forms with POST data and existing instances
            preferences_form = NotificationPreferencesForm(request.POST, instance=preferences)
            channels_form = NotificationChannelForm(request.POST, instance=channels)
            settings_form = NotificationSettingsForm(request.POST, instance=settings)
            types_form = NotificationTypeForm(request.POST, instance=types)
            
            # For Custom Templates, handle separately if needed
            # For simplicity, we'll assume adding a single template
            custom_template_form = CustomTemplateForm(request.POST)

            if (preferences_form.is_valid() and channels_form.is_valid() and settings_form.is_valid() and types_form.is_valid()):
                if (preferences_form.has_changed() or channels_form.has_changed() or settings_form.has_changed() or types_form.has_changed()):  # Check if any fields have been updated
                    # Get list of changed fields
                    changed_fields = {
                        'preferences': preferences_form.changed_data,
                        'channels': channels_form.changed_data,
                        'settings': settings_form.changed_data,
                        'types': types_form.changed_data
                    }
                    
                    preferences_form.save()
                    channels_form.save()
                    settings_form.save()
                    types_form.save()

                    messages.success(request, 'Your notification settings have been updated.')

                    save_audit_log(tenant=tenant, activity="Modified notification settings", module="Notifications", performed_by=profile, details=changed_fields)
                else:
                    messages.info(request, _("No changes detected."))
                return redirect(reverse_lazy('tenant_notifications'))
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            # Initialize forms with existing instances
            preferences_form = NotificationPreferencesForm(instance=preferences)
            channels_form = NotificationChannelForm(instance=channels)
            settings_form = NotificationSettingsForm(instance=settings)
            types_form = NotificationTypeForm(instance=types)

        context = {
            'title': _('Settings'),
            'segment': {'text': _('Notifications'), 'url': 'tenant_notifications'},
            'preferences_form': preferences_form,
            'channels_form': channels_form,
            'settings_form': settings_form,
            'types_form': types_form
        }
        return render(request, 'pages/tenant_settings/notifications.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

@login_required(login_url="/login/")
def organization_details(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)

        # Check for the session flag and pass it to the template
        is_successful = request.session.pop('is_successful', False)
        form = TenantForm(request.POST, request.FILES, instance=tenant)

        if request.method == 'POST':
            context = {
                'form': form,
                'is_successful': is_successful,
                'title': _('Settings'),
                'segment': {'text': _('Organization Details'), 'url': 'organization_details'},
            }
            if form.is_valid():
                if form.has_changed():  # Check if any fields have been updated
                    # Get list of changed fields
                    changed_fields = form.changed_data  
                    
                    # Save the updated form
                    form.save()
                    # Set the session flag to True
                    request.session['is_successful'] = True
                    messages.success(request, _("Successfully updated organization details."))

                    save_audit_log(tenant=tenant, activity="Updated organization details", module="Organization Details", performed_by=profile, details=changed_fields)
                else:
                    messages.info(request, _("No changes detected."))
                    
                return redirect(reverse_lazy('organization_details'))
            else:
                messages.error(request, _("Please double-check your inputs. It seems some fields have errors."))
                print("Form errors:", form.errors)  # Debug line
                return render(request, 'pages/tenant_settings/organization-details.html', context)
        else:
            form = TenantForm(instance=tenant)

        context = {
            'form': form,
            'title': _('Settings'),
            'segment': {'text': _('Organization Details'), 'url': 'organization_details'},
        }
        return render(request, 'pages/tenant_settings/organization-details.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

@login_required(login_url="/login/")
def address(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)

        # Check for the session flag and pass it to the template
        is_successful = request.session.pop('is_successful', False)
        form = TenantAddressForm(request.POST, instance=tenant)

        if request.method == 'POST':
            context = {
                'form': form,
                'is_successful': is_successful,
                'title': _('Settings'),
                'segment': {'text': _('Address'), 'url': 'tenant_address'},
            }
            if form.is_valid():
                if form.has_changed():  # Check if any fields have been updated
                    # Get list of changed fields
                    changed_fields = form.changed_data  
                    
                    # Save the updated form
                    form.save()
                    # Set the session flag to True
                    request.session['is_successful'] = True
                    messages.success(request, _("Successfully updated tenant address."))

                    save_audit_log(tenant=tenant, activity="Updated tenant address", module="Address", performed_by=profile, details=changed_fields)
                else:
                    messages.info(request, _("No changes detected."))
               
                return redirect(reverse_lazy('tenant_address'))
            else:
                messages.error(request, _("Please double-check your inputs. It seems some fields have errors."))
                print("Form errors:", form.errors)  # Debug line
                return render(request, 'pages/tenant_settings/address.html', context)
        else:
            form = TenantAddressForm(instance=tenant)

        context = {
            'form': form,
            'title': _('Settings'),
            'segment': {'text': _('Address'), 'url': 'tenant_address'},
        }
        return render(request, 'pages/tenant_settings/address.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)

@login_required(login_url="/login/")
def support(request):
    """
    Render the index page for the home view.
    Parameters:
    - request: The HTTP request object.
    Returns:
    - HttpResponse: The rendered HTML template.
    Raises:
    - None.
    """
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile)
        tenant = CORE_SHORTCUTS.GetUserTenant(profile, Tenant)
        support_cases = SupportCase.objects.filter(added_by=profile.user_object)
        
        if request.method == 'POST':
            form = SupportCaseForm(request.POST, user_profile=profile)
            if form.is_valid():
                if form.has_changed():  # Check if any fields have been updated
                    # Get list of changed fields
                    changed_fields = form.changed_data  
                    
                    # Save the updated form
                    form.save()
                    # Set the session flag to True
                    request.session['is_successful'] = True
                    messages.success(request, _("Successfully submitted support case."))

                    save_audit_log(tenant=tenant, activity="Submitted support case.", module="Support Case", performed_by=profile, details=changed_fields)
                else:
                    messages.info(request, _("No changes detected."))
                return redirect(reverse_lazy('tenant_support'))
            else:
                request.session['is_successful'] = False
                print("Form errors:", form.errors)  # Debug line
        else:
            form = SupportCaseForm(user_profile=profile)

        context = {
            'form': form,
            'title': _('Settings'),
            'segment': {'text': _('Support Case'), 'url': 'tenant_support'},
            'support_cases': support_cases
        }
        return render(request, 'pages/tenant_settings/support.html', context)
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)
