from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    PasswordChangeForm, 
    UsernameField, 
    PasswordResetForm, 
    SetPasswordForm
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
    """
    Custom login form that extends Django's built-in AuthenticationForm.
    
    Fields:
        - username: A text field for the user's username.
        - password: A password field for the user's password.
    """
    
    username = UsernameField(
        label=_("Username"),
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": _("Username")
        })
    )
    # Username field uses a text input with Bootstrap styling and a placeholder.

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control", 
            "placeholder": _("Password")
        }),
    )
    # Password field uses a password input, which hides the text for security.
    # The "strip" argument is set to False to preserve any whitespace in the password.

class UserPasswordResetForm(PasswordResetForm):
    """
    Custom password reset form that extends Django's built-in PasswordResetForm.
    
    Fields:
        - email: An email field for the user to enter their registered email address.
    """
    
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Email address')
        })
    )
    # Email field uses an email input with Bootstrap styling and a placeholder.
    # This form will send an email with a password reset link to the user.

class UserSetPasswordForm(SetPasswordForm):
    """
    Custom set password form that extends Django's built-in SetPasswordForm.
    
    Fields:
        - new_password1: A password field for the user to enter their new password.
        - new_password2: A password field for the user to confirm their new password.
    """
    
    new_password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Confirm New Password')
        }),
        label=_("New Password")
    )
    new_password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Confirm New Password')
        }),
        label=_("Confirm New Password")
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(_("The two password fields must match."))

        return cleaned_data

class UserPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form that extends Django's built-in PasswordChangeForm.
    
    Fields:
        - old_password: A password field for the user to enter their current password.
        - new_password1: A password field for the user to enter their new password.
        - new_password2: A password field for the user to confirm their new password.
    """
    
    old_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Old Password')
        }),
        label=_('Old Password'),
        required=True
    )
    # Old password field for the user to enter their current password.
    # This is required to verify the user's identity before changing the password.

    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': _('New Password')
        }),
        label=_("New Password"),
        required=True
    )
    # New password field, similar to the set password form, but for users changing their password.

    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Confirm New Password')
        }),
        label=_("Confirm New Password"),
        required=True
    )
    # Confirmation password field to ensure the new password was entered correctly.
