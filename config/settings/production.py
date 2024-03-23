from .base import *

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

try:
    from .local import *
except ImportError:
    pass
