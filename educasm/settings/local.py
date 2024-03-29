from . import db


ALLOWED_HOSTS = [
    '*',
]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
#DATABASES = db.MYSQL
DATABASES = db.POSTGRESQL
#DATABASES = db.POSTGRESQL


#CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
    'https://educasm-peru2.web.app',
    'https://sv-rvbfwpnmzd.cloud.elastika.pe',
    'http://sv-rvbfwpnmzd.cloud.elastika.pe'
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
