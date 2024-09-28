from django.apps import AppConfig


class TenantSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buzzerboy_saas_tenants.apps.tenant_settings'
    label = 'buzzerboy_saas_tenants_apps_tenant_settings'
