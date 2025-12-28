import os

ENV = os.getenv("DJANGO_ENV", "dev")

if ENV == "prod":
    from .prod import *
elif ENV == "stage":
    from .stage import *
else:
    from .dev import *
