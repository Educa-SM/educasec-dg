from . import db


"""ALLOWED_HOSTS = [
    'educasm-peru.site',
    'www.educasm-peru.site',
]"""

ALLOWED_HOSTS = [
    '*',
]


CSRF_TRUSTED_ORIGINS = [
    'https://educasm-peru.site',
    'https://www.educasm-peru.site',
    'https://sv-rvbfwpnmzd.cloud.elastika.pe',
    'http://sv-rvbfwpnmzd.cloud.elastika.pe',
    'http://localhost:4200',
]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#DATABASES = db.POSTGRESQL
DATABASES = db.SQLITE

CORS_ORIGIN_ALLOW_ALL = False
#CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
    'http://127.0.0.1:8000',
    'http://0.0.0.0:*',
    'https://sv-rvbfwpnmzd.cloud.elastika.pe',
    'http://sv-rvbfwpnmzd.cloud.elastika.pe',
    'https://educasm-peru2.web.app',
)
