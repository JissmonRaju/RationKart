from django.apps import AppConfig

class AdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AdminApp'

    # Remove the User model import if not needed here
    # def ready(self):
    #    from django.contrib.auth.models import User