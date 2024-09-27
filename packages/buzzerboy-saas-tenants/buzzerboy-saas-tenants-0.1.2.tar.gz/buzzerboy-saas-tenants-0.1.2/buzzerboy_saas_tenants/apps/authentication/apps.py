"""
This module contains the configuration for the authentication app.

Attributes:
    default_auto_field (str): The default auto field for the app.
    name (str): The name of the authentication app.
"""

from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'apps_authentication'
    name = 'apps.authentication'
