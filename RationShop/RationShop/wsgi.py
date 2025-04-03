# RationShop/wsgi.py
import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RationShop.settings')
application = get_wsgi_application()

# Auto-create superuser
User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists() and all([username, email, password]):
    User.objects.create_superuser(username, email, password)