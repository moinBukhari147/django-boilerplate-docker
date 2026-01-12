# config/settings/stage.py
import dj_database_url

from .base import *

DATABASES = {
    "default": dj_database_url.parse(env("DATABASE_URL"), conn_max_age=600),
}

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
