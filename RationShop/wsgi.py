# RationShop/wsgi.py
import os
import logging
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RationShop.settings')
application = get_wsgi_application()

logger = logging.getLogger(__name__)

try:
    User = get_user_model()
    username = os.getenv('DJANGO_SUPERUSER_USERNAME')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        logger.info("Superuser created successfully!")
    else:
        logger.info("Superuser already exists.")
except Exception as e:
    logger.error(f"Error creating superuser: {e}")