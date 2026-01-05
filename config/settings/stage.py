# config/settings/stage.py
import dj_database_url

from .base import *

DEBUG = False

DATABASES["default"] = dj_database_url.config(
    conn_max_age=300,
    ssl_require=True,
)

# -------------------------------------------------------------------
# Cors
# -------------------------------------------------------------------
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])


# -------------------------------------------------------------------
# Security
# -------------------------------------------------------------------
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
