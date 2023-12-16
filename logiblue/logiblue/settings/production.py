import os

from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ['poralia.pythonanywhere.com']

CORS_ALLOWED_ORIGINS = [
    'https://poralia.pythonanywhere.com',
    'https://logiblue-fe.vercel.app',
]

STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static')
