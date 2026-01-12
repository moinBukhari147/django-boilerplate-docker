import dj_database_url

from .base import *

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.ngrok-free.app",
]

DATABASES = {
    "default": dj_database_url.parse(
        env("DATABASE_URL", default="postgres://postgres:postgres@postgres:5432/postgres"),
    ),
}

INSTALLED_APPS += ["silk"]

# Silk middleware must be at the top
MIDDLEWARE = ["silk.middleware.SilkyMiddleware", *MIDDLEWARE]

SILKY_INTERCEPT_PERCENT = 100
SILKY_MAX_REQUEST_BODY_SIZE = -1
SILKY_MAX_RESPONSE_BODY_SIZE = -1
SILKY_IGNORE_PATHS = ["/admin/"]
