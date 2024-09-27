from django.apps import AppConfig


class TenantSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tenant_settings'
    label = 'apps_tenant_settings'
