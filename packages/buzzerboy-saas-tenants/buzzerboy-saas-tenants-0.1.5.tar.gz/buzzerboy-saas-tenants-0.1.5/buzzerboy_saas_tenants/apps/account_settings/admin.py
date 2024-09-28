from django.contrib import admin

from buzzerboy_saas_tenants.apps.account_settings.models import NotificationPreferences,NotificationChannel, NotificationSettings, NotificationType

# Register your models here.
admin.site.register(NotificationPreferences)
admin.site.register(NotificationChannel)
admin.site.register(NotificationSettings)
admin.site.register(NotificationType)
