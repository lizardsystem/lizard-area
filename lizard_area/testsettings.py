import os

from lizard_ui.settingshelper import setup_logging
from lizard_ui.settingshelper import STATICFILES_FINDERS

DEBUG = True
TEMPLATE_DEBUG = True

# SETTINGS_DIR allows media paths and so to be relative to this settings file
# instead of hardcoded to c:\only\on\my\computer.
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))

# BUILDOUT_DIR is for access to the "surrounding" buildout, for instance for
# BUILDOUT_DIR/var/static files to give django-staticfiles a proper place
# to place all collected static files.
BUILDOUT_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, '..'))
LOGGING = setup_logging(BUILDOUT_DIR)

# Django supports the databases 'postgresql_psycopg2', 'postgresql', 'mysql',
# 'sqlite3' and 'oracle'. If you use a geodatabase, Django supports the
# following ones:
#
#   'django.contrib.gis.db.backends.postgis'
#   'django.contrib.gis.db.backends.mysql'
#   'django.contrib.gis.db.backends.oracle'
#   'django.contrib.gis.db.backends.spatialite'

DATABASES = {
    'default': {
        'NAME': 'area',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'buildout',
        'PASSWORD': 'buildout',
        'HOST': '127.0.0.1',  # empty string for localhost.
        'PORT': '',  # empty string for default.
    }
}

# With regard to the database definitions above, if you want to use a different
# database, consider putting its definition in localsettings.py. Otherwise, if
# you change the definitions above and commit them (to the repository), other
# developers will also have to use them.
#
# One of those other developers is Jenkins, our continuous integration
# solution. Jenkins can only run the tests of the current application when the
# specified database exists. When the tests cannot run, Jenkins sees that as an
# error.

SITE_ID = 1
INSTALLED_APPS = [
    'lizard_security',
    'lizard_fewsnorm',
    'lizard_area',
    'lizard_geo',
    'lizard_ui',
    'lizard_map',
    'lizard_measure',
    'treebeard',
    'djangorestframework',
    'staticfiles',
    'compressor',
    #'south',
    'django_nose',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.gis',
    'django.contrib.sites',
    ]
ROOT_URLCONF = 'lizard_area.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    # Uncomment this one if you use lizard-map.
    # 'lizard_map.context_processors.processor.processor',
    # Default django 1.3 processors.
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages"
    )

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Absolute path to the directory that holds user-uploaded media.
MEDIA_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'media')
# Absolute path to the directory where django-staticfiles'
# "bin/django build_static" places all collected static files from all
# applications' /media directory.
STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
MEDIA_URL = '/media/'
# URL for the per-application /media static files collected by
# django-staticfiles.  Use it in templates like
# "{{ MEDIA_URL }}mypackage/my.css".
STATIC_URL = '/static_media/'
# Used for django-staticfiles
STATIC_URL = '/static_media/'
STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'static')
STATICFILES_FINDERS = STATICFILES_FINDERS


try:
    # Import local settings that aren't stored in svn/git.
    from lizard_area.local_testsettings import *
except ImportError:
    pass
