from decouple import config
from . import db


ALLOWED_HOSTS = [
    'educasm-peru.site',
    'www.educasm-peru.site',
]

CSRF_TRUSTED_ORIGINS = [
    'https://educasm-peru.site',
    'https://www.educasm-peru.site',
]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = db.SQLITE


CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'https://educasm-peru2.web.app',
)
