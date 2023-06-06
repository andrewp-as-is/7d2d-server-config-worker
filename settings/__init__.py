from configurations import Configuration, values
from .utils import get_installed_apps

class Base(Configuration):
    DATABASES = values.DatabaseURLValue(environ_name='DJANGO_DATABASE_URL')
    INSTALLED_APPS = get_installed_apps()
    TIME_ZONE = 'UTC'

class Dev(Base):
    DEBUG = True


class Prod(Base):
    DEBUG = False

try:
    import psycopg2
except ImportError:
    # Fall back to psycopg2cffi
    from psycopg2cffi import compat
    compat.register()
