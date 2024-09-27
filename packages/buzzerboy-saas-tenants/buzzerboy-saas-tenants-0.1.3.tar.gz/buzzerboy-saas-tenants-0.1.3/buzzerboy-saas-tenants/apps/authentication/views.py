from apps.accounts.models import UserProfile
from . import forms
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

from core import shortcuts as CORE_SHORTCUTS

from core.middleware import HandleHTTPErrorsMiddleware

from django.utils.translation import gettext_lazy as _

middleware = HandleHTTPErrorsMiddleware(get_response=None)

# Authentication
class UserLoginView(LoginView):
    """
    Custom login page for users.

    This class handles user login by displaying a login form and processing the user's credentials.
    It extends Django's built-in LoginView, which provides much of the functionality automatically.

    Attributes:
        template_name (str): The path to the HTML template that should be used to display the login form.
        form_class (forms.LoginForm): The form that will be used to collect the user's login details.
    """
    template_name = 'pages/authentication/auth-login-minimal.html'  # Specify the template to use for the login page.
    form_class = forms.LoginForm  # Use the custom LoginForm defined in forms.py.

def logout_view(request):
    """
    Log out the current user.

    This function logs out the user and redirects them to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the login page.
    """
    logout(request)  # Log out the user.
    return redirect('login')  # Redirect to the login page.

class UserPasswordResetView(PasswordResetView):
    """
    Password reset view for users who forgot their password.

    This view displays a form where users can request a password reset email. It extends Django's
    built-in PasswordResetView, which handles the process of sending the reset email.

    Attributes:
        template_name (str): The path to the HTML template that should be used for the password reset form.
        form_class (forms.UserPasswordResetForm): The form class that collects the user's email address.
    """
    template_name = 'accounts/password_reset.html'  # Specify the template to use for the password reset page.
    form_class = forms.UserPasswordResetForm  # Use the custom UserPasswordResetForm.

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    View for setting a new password after receiving a reset link.

    This view is used when the user clicks the link in their password reset email.
    It allows the user to enter a new password.

    Attributes:
        template_name (str): The path to the HTML template for the password reset confirmation page.
        form_class (forms.UserSetPasswordForm): The form used for setting the new password.
    """
    template_name = 'accounts/password_reset_confirm.html'  # Specify the template to use for password reset confirmation.
    form_class = forms.UserSetPasswordForm  # Use the custom UserSetPasswordForm.

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    View for changing the user's password.

    This class allows users to change their passwords securely. It ensures that only authenticated users can access this view,
    and handles the entire process of password change, from displaying the form to processing it.

    Attributes:
        template_name (str): The path to the HTML template that will be used to render the password change page.
        form_class (Form): The form class that will handle the user's input for changing the password.
        success_url (str): The URL to redirect the user to after a successful password change. In this case, it redirects back to the same page.
    """

    template_name = 'pages/home/account_settings/change-password.html'  # Specify the template to use for the password change page.
    form_class = forms.UserPasswordChangeForm  # Use a custom form class for changing the password.
    success_url = reverse_lazy('change_password')  # After a successful password change, redirect back to the same page.

    def get_context_data(self, **kwargs):
        """
        Provides additional context data for rendering the view.

        This method adds extra information to the template's context, such as the page title and whether
        the password was successfully changed, to customize the user experience.

        Args:
            **kwargs: Additional keyword arguments that might be passed to the view.

        Returns:
            dict: A dictionary containing context data for rendering the template.
        """

        context = super().get_context_data(**kwargs)  # Get the default context data from the parent class.
        context['title'] = _('Account Settings')  # Set the title of the page.
        context['segment'] = {'text': _('Change Password'), 'url': 'change_password'}  # Define the current segment of the site.
        context['password_changed'] = 'password_changed' in self.request.GET  # Check if the password was successfully changed.
        return context  # Return the updated context to be used in the template.

    def form_valid(self, form):
        """
        Handles the form submission and processes the password change.

        This method is called when the user submits the password change form. If the form is valid, the password is changed,
        and the user is redirected to the same page with a confirmation message.

        Args:
            form (Form): The form instance that contains the user's input.

        Returns:
            HttpResponse: A response object that redirects the user after a successful password change.
        """
        
        response = super().form_valid(form)  # Call the parent class's form_valid method to handle the password change.
        self.success_url += '?password_changed=True'  # Append a flag to the URL to indicate the password was changed.
        return response  # Return the response to complete the process.

def create_password_invite(request, token):
    try:
        profile = CORE_SHORTCUTS.GetUserProfile(request.user, UserProfile, token)

        form = forms.UserSetPasswordForm(profile.user_object)

        if request.method == 'POST':
            form = forms.UserSetPasswordForm(profile.user_object, request.POST)
            try:
                if form.is_valid():
                    form.save()

                    profile.user_token = None
                    profile.save()
                    
                    print('Your password has been set successfully.')
                    return redirect('password_create_complete')  # Redirect to the login page or another page of your choice
                else:
                    print('There was an error setting your password. Please try again.')
            except ValidationError as e:
                print(f'Error: {", ".join(e.messages)}')
            
        context = {
            'form': form,
            'token': token
        }
        
        return render(request, 'pages/authentication/password-create.html', context)
    
    except Exception as e:
        if hasattr(e, 'message'):
            message = str(e.message)
            print(message)
        else:
            message = str(e)
            print(message)
        return middleware.handle_http_error(request, status_code=500, message=message)