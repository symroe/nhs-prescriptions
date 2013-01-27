# Django settings for nhs project.
import os
import ffs

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT = ffs.Path(__file__).parent


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

import dj_database_url

DATABASES = {'default': dj_database_url.config(default='postgis://localhost/scrip')}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = str(ROOT/'static')

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@$))#obur9s0^_*8gfqj%kris-$zj$usz04lq+s&k(mwjb3xt!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'nhs.urls'

TEMPLATE_DIRS = (
    ROOT/'templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'django_extensions',
    'mapit',
    'test_utils',
    'prescriptions',
    'practices',
    'patents',
    'api',
    'ccgs',
)

GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH','/app/.geodjango/geos/lib/libgeos_c.so')
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH','/app/.geodjango/gdal/lib/libgdal.so')

MAPIT_AREA_SRID = 4326
MAPIT_COUNTRY = 'GB'


try:
    from local_settings import *
except:
    pass
