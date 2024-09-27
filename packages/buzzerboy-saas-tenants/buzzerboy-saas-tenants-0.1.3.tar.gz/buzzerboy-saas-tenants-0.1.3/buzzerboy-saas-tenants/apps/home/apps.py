from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class HomeConfig(AppConfig):
    """
    AppConfig for the 'home' app.
    Attributes:
        default_auto_field (str): The default auto field to use for models.
        label (str): The label for the app.
        name (str): The name of the app.
    Methods:
        ready(): A method called when the app is ready.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'apps_home'
    name = 'apps.home'
    
        