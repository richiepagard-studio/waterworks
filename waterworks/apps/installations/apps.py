from django.apps import AppConfig


class InstallationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.installations'

    def ready(self):
        import apps.installations.signals
