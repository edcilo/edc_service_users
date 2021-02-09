#!/bin/sh

set -e

echo $(date "+%F %T.%3N %Z") "[django] INFO: running start.sh"

env=${APP_ENV:-dev}


echo "update pip and install dependencies"
/usr/local/bin/python -m pip install --upgrade pip
pip install -r requirements.txt

echo "execute migrations"
python manage.py migrate

echo "collect static files"
python manage.py collectstatic  --noinput


if [ $env = "prod" ]
then
    echo $(date "+%F %T.%3N %Z") "[django] INFO: running production environment"
    gunicorn edcilo_com.wsgi:application --bind 0.0.0.0:8000 --config ./gunicorn.config.py
else
    echo $(date "+%F %T.%3N %Z") "[django] INFO: running develop environment"
    python manage.py runserver 0.0.0.0:8000
fi
