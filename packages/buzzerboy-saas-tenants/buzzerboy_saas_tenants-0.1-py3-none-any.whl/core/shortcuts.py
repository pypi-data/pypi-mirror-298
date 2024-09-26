import os
from django.core.exceptions import ObjectDoesNotExist
from apps.accounts.models import UserType
from django.core.management import call_command

def GetUserProfile(user, UserProfile, token=None, **kwargs):
    """
    Get or create the user profile for the given user and update it with any provided kwargs.
    
    Parameters:
    - user: The user object for which to retrieve or create the profile.
    - UserProfile: The UserProfile model class.
    - kwargs: Additional fields to update in the UserProfile.
    
    Returns:
    - profile: The user profile object.
    
    Comments:
    - This function checks if the given user has a profile attribute. If not, it creates a new profile using the UserProfile model class.
    - Any additional keyword arguments passed to the function are used to update the profile fields.
    - Finally, it returns the user profile object.
    """
    if token:
        profile, created = UserProfile.objects.get_or_create(user_token=token)
    else:
        profile, created = UserProfile.objects.get_or_create(user_object=user)
    
    # Update profile fields based on kwargs
    for key, value in kwargs.items():
        if hasattr(profile, key):
            setattr(profile, key, value)

    if not profile.has_role() and profile.user_object.is_superuser:
        try:
            user_type = UserType.objects.get(name="Administrator")
        except ObjectDoesNotExist:
            user_type = UserType.objects.create(
                name="Administrator", 
                description="Responsible for system management and configuration with full access",
                has_full_access=True,
                has_nonstaff_access=True
            )

        setattr(profile, 'user_type', user_type)
    
    profile.save()
    
    return profile

def GetUserTenant(userProfile, Tenant):
    """
    Get the tenant object for the given user.
    
    Parameters:
    - user: The user object for which to retrieve the tenant.
    
    Returns:
    - tenant: The tenant object.
    
    Comments:
    - This function retrieves the tenant object associated with the given user.
    - If the user does not have a tenant, it creates one.
    - Otherwise, it returns the tenant object associated with the user.
    """
    # Update profile fields based on kwargs

    if not userProfile.has_tenant():

        # Check if default tenant is exists
        # Explanation: Since the company name is unique, it might cause constraint errors if not checked.
        try:
            tenant = Tenant.objects.get(company_name="*** TENANT NOT SETUP ***")
        except ObjectDoesNotExist:
            tenant = Tenant.objects.create()

        
        userProfile.tenant = tenant
        userProfile.save()    

    return userProfile.tenant


def GetPlans(SubscriptionPlan):
    plans = SubscriptionPlan.objects.all()
    if not plans.exists():
        # Load data from fixtures if no plans are found
        fixture_path = os.path.join('fixtures', 'plans.json')
        call_command('loaddata', fixture_path)

    # Fetch the updated list of subscription plans
    plans = SubscriptionPlan.objects.all()

    return plans