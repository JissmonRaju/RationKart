from django.apps import AppConfig


class AdminappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AdminApp'

# RationShop/apps.py (or a new file like create_superuser.py)
import os
from django.contrib.auth.models import User
from django.core.management import call_command

def create_superuser():
    if not User.objects.filter(username=os.getenv('DJANGO_SUPERUSER_USERNAME')).exists():
        call_command(
            'createsuperuser',
            '--noinput',
            '--username', os.getenv('DJANGO_SUPERUSER_USERNAME'),
            '--email', os.getenv('DJANGO_SUPERUSER_EMAIL')
        )
        # Set password (optional)
        user = User.objects.get(username=os.getenv('DJANGO_SUPERUSER_USERNAME'))
        user.set_password(os.getenv('DJANGO_SUPERUSER_PASSWORD'))
        user.save()