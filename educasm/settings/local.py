from . import db


ALLOWED_HOSTS = [
    '*',
]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = db.SQLITE


CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
    'https://educasm-peru2.web.app',
    'https://sv-rvbfwpnmzd.cloud.elastika.pe',
    'http://sv-rvbfwpnmzd.cloud.elastika.pe'
)
