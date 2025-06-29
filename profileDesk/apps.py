from django.apps import AppConfig

class ProfileDeskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profileDesk'

    def ready(self):
        import profileDesk.signals