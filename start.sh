#!/usr/bin/env bash
set -e
echo "Creating staticfiles dir..."
mkdir -p staticfiles
echo "Running migrations..."
for attempt in {1..10}; do
  if python manage.py migrate --noinput; then
    break
  fi

  if [ "$attempt" -eq 10 ]; then
    echo "Migrations failed after $attempt attempts."
    exit 1
  fi

  echo "Database unavailable, retrying migrations in 5 seconds... ($attempt/10)"
  sleep 5
done
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "Starting gunicorn..."
exec gunicorn config.wsgi:application
