from django.apps import AppConfig

class JobsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'JobsApp'

    def ready(self):
        import JobsApp.signals