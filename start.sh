#!/usr/bin/env bash
set -e
echo "Creating staticfiles dir..."
mkdir -p staticfiles
echo "Running migrations..."
python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "Starting gunicorn..."
exec gunicorn config.wsgi:application
