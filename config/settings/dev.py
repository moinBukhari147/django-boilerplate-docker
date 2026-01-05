import dj_database_url

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.ngrok-free.app",
]

DATABASES = {
    "default": dj_database_url.config(
        default=env("DATABASE_URL", default="sqlite:///./db.sqlite3"),
        conn_max_age=0,  # SQLite doesn't support pooling
    ),
}
