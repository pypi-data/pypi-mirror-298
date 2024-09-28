from django.contrib import admin

from buzzerboy_saas_tenants.apps.tenant_settings.models import AuditLog, BillingDetails, SupportCase

# Register your models here.
admin.site.register(BillingDetails)
admin.site.register(AuditLog)
admin.site.register(SupportCase)