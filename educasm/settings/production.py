from . import db

ALLOWED_HOSTS = [
    '*',
]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#DATABASES = db.POSTGRESQL
DATABASES = db.SQLITE

CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
    'http://127.0.0.1:8000',
    'http://0.0.0.0:*',
    'https://sv-rvbfwpnmzd.cloud.elastika.pe',
    'https://sv-rvbfwpnmzd.cloud.elastika.pe:*',
    'http://sv-rvbfwpnmzd.cloud.elastika.pe',
    'https://educasm-peru2.web.app',
)


CSRF_TRUSTED_ORIGINS = [
    'https://educasm-peru.site',
    'https://www.educasm-peru.site',
    'https://sv-rvbfwpnmzd.cloud.elastika.pe',
    'http://sv-rvbfwpnmzd.cloud.elastika.pe',
    'http://localhost:4200',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True
