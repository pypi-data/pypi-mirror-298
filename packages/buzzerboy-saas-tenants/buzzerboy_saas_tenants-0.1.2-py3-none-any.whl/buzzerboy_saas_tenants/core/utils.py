from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string
from django.conf import settings

from apps.accounts.models import UserProfile
from apps.tenant_settings.models import AuditLog

from django.utils import timezone

def generate_user_token():
    return get_random_string(length=255)  # Adjust length as needed

def create_or_update_user_profile(user):
    profile, created = UserProfile.objects.get_or_create(user_object=user)
    if created or not profile.user_token:
        profile.user_token = generate_user_token()
        profile.save()
    return profile

def generate_invitation_link(user):
    profile = create_or_update_user_profile(user)
    token = profile.user_token
    uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encode user ID
    relative_url = reverse('user_invitation', kwargs={'uidb64': uid, 'token': token})
    full_url = f"{settings.SITE_URL}{relative_url}"  # Prepend domain from settings
    return full_url
    

def save_audit_log(tenant, performed_by, activity, module, details):
    AuditLog.objects.create(tenant=tenant, activity=activity, module=module, details=details, performed_by=performed_by, timestamp=timezone.now())