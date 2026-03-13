#!/usr/bin/env bash
set -e
mkdir -p staticfiles
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
exec gunicorn config.wsgi:application
