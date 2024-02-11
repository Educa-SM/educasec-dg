from decouple import config
from . import BASE_DIR



POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': config('PSQL_HOST'),
        'PORT': config('PSQL_PORT'),
        'NAME': config('PSQL_NAME'),
        'USER': config('PSQL_USER'),
        'PASSWORD': config('PSQL_PASSWORD'),
    }
}

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR/'db.sqlite3',
    }
}


MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'educasm',
        'USER': 'root',
        'PASSWORD':'',
    }
}