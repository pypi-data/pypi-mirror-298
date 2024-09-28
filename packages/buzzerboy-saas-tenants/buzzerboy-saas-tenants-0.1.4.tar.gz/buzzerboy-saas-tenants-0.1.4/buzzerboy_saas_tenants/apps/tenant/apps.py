from django.apps import AppConfig


class TenantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buzzerboy_saas_tenants.apps.tenant'
    label = 'buzzerboy_saas_tenants_apps_tenant'
