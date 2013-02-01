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

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = True
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

STATIC_ROOT = ''
# STATIC_ROOT = str(ROOT/'static')

STATICFILES_DIRS = (
    str(ROOT / 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = '@$))#obur9s0^_*8gfqj%kris-$zj$usz04lq+s&k(mwjb3xt!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
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
    # 3rd Party
    'south',
    'django_extensions',
    'mapit',
    'tastypie_swagger',
    # Us
    'prescriptions',
    'practices',
    'patents',
    'nice',
    'api',
    'ccgs',
)

# 27700
MAPIT_AREA_SRID = 27700
MAPIT_COUNTRY = 'GB'

TASTYPIE_SWAGGER_API_MODULE = 'nhs.api.urls.v1_api';

try:
    from local_settings import *
except:
    pass



# TEST_RUNNER = 'django.contrib.gis.tests.GeoDjangoTestSuiteRunner'
