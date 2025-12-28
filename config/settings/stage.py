# config/settings/stage.py
import dj_database_url

from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

DATABASES["default"] = dj_database_url.config(
    conn_max_age=300,
    ssl_require=True,
)

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
