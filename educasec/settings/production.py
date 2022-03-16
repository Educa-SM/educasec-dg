#import dj_database_url
#from decouple import config

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}
#conexion con postgresql
"""DATABASES = {
    'default': dj_database_url.config(
        default = config('DATABASE_URL')
    )
}"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'educasec',
        'USER': 'alonso',
        'PASSWORD': 'alonso',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

#conexion con react
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
   'http://localhost:4200',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'