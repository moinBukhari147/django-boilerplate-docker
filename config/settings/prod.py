# config/settings/prod.py
import dj_database_url

from .base import *

DATABASES = {
    "default": dj_database_url.parse(env("DATABASE_URL"), conn_max_age=600, ssl_require=True),
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
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# -------------------------------------------------------------------
# Logging (minimal, production-safe)
# -------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
