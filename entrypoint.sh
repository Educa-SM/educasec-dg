#!/bin/sh

echo 'Running collecstatic...'
python manage.py collectstatic 

echo 'Making migrations...'
#python manage.py makemigrations 

echo 'Applying migrations...'
python manage.py migrate 

echo 'Running server...'
python manage.py runserver 0.0.0.0:${PORT} 