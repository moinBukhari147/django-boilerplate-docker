import dj_database_url

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES["default"] = dj_database_url.config(
    default=os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3"),
    conn_max_age=0,
)
