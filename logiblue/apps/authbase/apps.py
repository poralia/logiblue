from django.apps import AppConfig


class AuthBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authbase'
    label = 'authbase'
