from django import forms
from apps.accounts.models import UserProfile
from apps.tenant.models import SubscriptionPlan, Tenant
from apps.tenant_settings.models import BillingDetails, SupportCase
from core.email_service import EmailService
from ckeditor.widgets import CKEditorWidget
from django.apps import apps

from django.contrib.auth.models import User

from django.utils import timezone


from django.utils.translation import gettext_lazy as _


class TenantSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['subscription_plan']  # Change to a list

    subscription_plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.all(),
        required=False,  # Change to True if you want to make it required
        label="",  # Empty label will hide the label
        help_text=None,  # Set help_text to None to hide it
        widget=forms.Select(attrs={'class': 'd-none'})  # Add your CSS class here
    )
