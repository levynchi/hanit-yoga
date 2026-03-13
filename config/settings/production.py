"""
Django production settings for Railway deployment.
"""
import os
from pathlib import Path

import dj_database_url
from .base import *

# Set DJANGO_DEBUG=1 in Railway Variables to show debug pages (disable after debugging)
DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() in ('1', 'true', 'yes')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('DJANGO_SECRET_KEY must be set in production')

# Allow comma-separated list; default includes Railway public domain
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '.railway.app,localhost')
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(',') if h.strip()]

# PostgreSQL from Railway DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# WhiteNoise for static files (add after SecurityMiddleware)
MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

# Media files on Railway Volume
volume_path = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
if volume_path:
    MEDIA_ROOT = Path(volume_path)
else:
    MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
