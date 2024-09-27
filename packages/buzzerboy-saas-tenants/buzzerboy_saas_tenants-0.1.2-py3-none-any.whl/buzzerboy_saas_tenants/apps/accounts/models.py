import os
import random
import string
from django.db import models
from apps.localization.models import Country, StateProvince, SupportedLanguage, Timezone
from apps.tenant.models import Tenant
from core.models import AuditableBaseModel
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _  # Make sure to use gettext_lazy for model choices

from django.core import mail
from django.conf import settings

def default_notification_preferences():
    return {
        'email_notifications': True,
        'sms_notifications': True,
        'push_notifications': True
    }
    
def default_privacy_settings():
    return {
        'profile_visibility': 'public',
        'search_engine_indexing': True,
        'data_sharing': True
    }
  
  
class StaticUI:
    
    @staticmethod
    def line_split_notes (str):
        count = 1
        wpl = 40
        str = str.strip()
        words = str.split(" ")
        text = ""
        for w in words:
           count += len(w)
           if count >= wpl:
                text += "<br/>"  
                count = 1   
           text += w + " "
           
        return text
    
    @staticmethod   
    def html_img(alt, str_url):
        s = "<img src='" + alt + "' src='" + str_url + "' />"
        return s

    @staticmethod
    def mask_email(s):
        #finding the location of @
        ln = len(s)
        op = s[0] + "*******" + s[ln-1]
        lo = s.find('@')
        la = s.find ('.', lo)
        if la < 0:
            return op
        if lo > 0:
            k = s[0] + "******" + s[lo-1:lo+2] + "****" + s[la-1:]
            return k
        else:
            return op

    @staticmethod
    def random_string():
        size=10
        chars=string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))


    @staticmethod
    def read_str_to_dict (str):
        lines = str.strip().splitlines()
        dict = {}
        cols = []
        firstrow = []
        i = 0
        j = 0
        for row in lines:
            cols = row.__str__().split(", ")
            for col in cols:
                dict [i] = col
                i+=1
            i=0
        return dict

    @staticmethod
    def your_randint():
        return random.randint(1, 5)

class UserType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    has_full_access = models.BooleanField(default=False)
    has_nonstaff_access = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def has_access_by_url(self, url_key):
        if self.has_full_access:
            return True

        try:
            access = self.accesses.get(request_path=url_key)
            return True
        except UserTypeAccess.DoesNotExist:
            return False

    def has_access(self, a_key):
        if self.has_full_access:
            return True

        try:
            access = self.accesses.get(access_key=a_key)
            return True
        except UserTypeAccess.DoesNotExist:
            return False


    def add_access(self, request_path, access_key):
        access = UserTypeAccess(
            user_type=self,
            request_path=request_path,
            access_key=access_key
        )
        access.save()
        return access

class UserTypeAccess(models.Model):
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True, related_name="accesses")
    request_path = models.CharField(max_length=255)
    access_key = models.CharField(max_length=20)

    class Meta:
        unique_together = ('access_key', 'user_type',)

    def __str__(self):
        return f"{self.access_key} | {self.user_type} ({self.request_path})"

class UserProfile(AuditableBaseModel):
    
    def upload_profile_file_name(instance, filename):
        fname, fextension = os.path.splitext(filename)
        s = "u_" + instance.id.__str__() + fextension
        return os.path.join('uploads', instance.id.__str__(), "user", s)

    
    # Relationships
    tenant = models.ForeignKey(Tenant, on_delete=models.DO_NOTHING, related_name="team", blank=True, null=True)
    user_type = models.ForeignKey(UserType, on_delete=models.DO_NOTHING, blank=True, null=True)
    user_object = models.OneToOneField(User, related_name="profile", on_delete=models.DO_NOTHING, blank=True, null=True)
    
    # Metadata
    profile_picture = models.ImageField(null=True, blank=True, default="", upload_to=upload_profile_file_name)
    
    # Contact Information
    phone_number = models.CharField(max_length=25, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state_province = models.ForeignKey(StateProvince, on_delete=models.SET_NULL, blank=True, null=True)
    postalcode = models.CharField(max_length=7, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Professional Information
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    linkedin_profile = models.CharField(max_length=100, blank=True)
    github_profile = models.CharField(max_length=100, blank=True)
    
    # Preferences and Settings
    language = models.ForeignKey(SupportedLanguage, on_delete=models.SET_NULL, blank=True, null=True)
    timezone = models.ForeignKey(Timezone, on_delete=models.SET_NULL, blank=True, null=True)
    notification_preferences = models.JSONField(default=default_notification_preferences, blank=True)
    privacy_settings = models.JSONField(default=default_privacy_settings, blank=True)

    # Additional Information
    bio = RichTextField(blank=True)
    interests = RichTextField(blank=True)
    skills = RichTextField(blank=True)
    education = RichTextField(blank=True)
    experience = RichTextField(blank=True)

    # New Field
    user_token = models.TextField(blank=True, null=True)

    class UserProfileStatus(models.TextChoices):
        ENABLED = 'ENABLED', _('Enabled')
        DISABLED = 'DISABLED', _('Disabled')
        INVITED = 'INVITED', _('Invited')

    status = models.CharField(max_length=100, choices=UserProfileStatus.choices, default=UserProfileStatus.DISABLED)
    

    def __str__(self):
        return self.user_object.username
        # return self.user_object.username + " @ " + self.tenant.company_name + " (" + self.user_type.description + ")"

    def get_tenant(self):
        return self.tenant

    def suspend_access(self, user):
        self.last_updated_by = user
        self.save()
        self.user_object.is_active = False
        self.user_object.save()

    def reactivate_access(self, user):
        self.last_updated_by = user
        self.save()
        self.user_object.is_active = True
        self.user_object.save()

    def send_invite(self, user):
        l = self.user_object

        connection = mail.get_connection()
        connection.open()
        
        email_body = self.tenant.user_invite_template.__str__()
        ### do any other email body processing
        
        email = mail.EmailMessage(
            self.subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER,],
            [self.user.user_object.email,],
            reply_to=[self.user.tenant.support_email_address,],
            headers={'Message-ID': self.user.tenant.__str__()},
        )
        email.content_subtype = "html" 
        r = email.send()
        connection.close()


    def line_split_notes(self):
        return StaticUI.line_split_notes(self.notes)

    def your_randint(self):
        return random.randint(1, 5)

    def has_role(self):
        return self.user_type

    def has_access(self, access_key):
        return self.user_type.has_access(access_key)

    def has_tenant(self):
        return self.tenant is not None

    def has_access_by_url(self, url_key):
        return self.user_type.has_access_by_url(url_key)

    def preferred_language(self):
        if self.language:
            return self.language

        return SupportedLanguage.objects.first()

    @property
    def email_address_property(self):
        return self.user_object.email_address

    @property
    def profile_picture_url(self):
        myurl = "/static/assets/img/theme/empty-user.png"

        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            myurl = self.profile_picture.url
        return myurl

    @property
    def profile_picture_html(self):
        return StaticUI.html_img(alt=self.user_object.first_name + ' ' + self.user_object.last_name,
                                 str_url=self.profile_picture_url)
