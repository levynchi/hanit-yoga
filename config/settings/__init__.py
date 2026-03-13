"""
Load local or production settings based on DJANGO_ENV.
"""
import os

if os.environ.get('DJANGO_ENV') == 'production':
    from .production import *  # noqa: F401, F403
else:
    from .local import *  # noqa: F401, F403
