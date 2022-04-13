#import dj_database_url
#from decouple import config

ALLOWED_HOSTS = [
    '217.21.78.46',
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }
# conexion con postgresql
"""DATABASES = {
    'default': dj_database_url.config(
        default = config('DATABASE_URL')
    )
}"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'educasec',
        'USER': 'postgres',
        'PASSWORD': '123456',
    }
}

# conexion con react
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
