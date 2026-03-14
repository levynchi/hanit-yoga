#!/usr/bin/env bash
set -e
echo "Creating staticfiles dir..."
mkdir -p staticfiles
echo "Running migrations..."
python manage.py migrate --noinput
# Create superuser if env vars set (e.g. on first deploy). Remove after use.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --noinput 2>/dev/null || true
fi
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "Starting gunicorn..."
exec gunicorn config.wsgi:application
