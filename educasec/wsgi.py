
import os

from django.core.wsgi import get_wsgi_application

"""
from decouple import config as config_decouple

if config_decouple('PRODUCTION', default=False):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kevincar.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kevincar.settings.local')

"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educasec.settings.local')

application = get_wsgi_application()
