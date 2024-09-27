from django.contrib import admin

from apps.tenant_settings.models import AuditLog, BillingDetails, SupportCase

# Register your models here.
admin.site.register(BillingDetails)
admin.site.register(AuditLog)
admin.site.register(SupportCase)