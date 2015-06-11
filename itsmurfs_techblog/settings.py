# Django settings for itsmurfs_techblog project.
from __future__ import absolute_import
import os

###################################################################
#
#                       FLAGS AND VARIABLES
#
###################################################################
DEBUG = True
TEMPLATE_DEBUG = DEBUG
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



###################################################################
#
#                           DATABASES
#
###################################################################

MONGO_DATABASE_NAME = 'techblog_db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog',
        'USER': 'blog',
        'PASSWORD': 'blog',
        'HOST': 'localhost',
        'PORT': ''
    },
    MONGO_DATABASE_NAME: {
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'techblog_db',
    }
}

DATABASE_ROUTERS = ['techblog.routers.TechblogRouter']

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}

###################################################################
#
#                           TESTS
#
###################################################################

TEST_RUNNER = 'techblog.tests.TechblogRunner'

SOUTH_TESTS_MIGRATE = False # To disable migrations and use syncdb instead
SKIP_SOUTH_TESTS = True # To disable South's own unit tests

###################################################################
#
#                       ADMINISTRATION
#
###################################################################

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pox8+s8(=ra8%1qtb0qy67h@!d=dj@*4seo#5-z+0-!-%e9s2o'


###################################################################
#
#                           SITES
#
###################################################################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

SITE_ID = '1'

SITE_DOMAIN = "http://127.0.0.1:8000/"

###################################################################
#
#                 CULTURE AND INTERNATIONALIZATION
#
###################################################################

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


###################################################################
#
#                    MEDIA AND STATIC FILES
#
###################################################################

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'


FILE_UPLOAD_TEMP_DIRECTORY = "upload_temp"
FILE_UPLOAD_DIRECTORY = "uploads"


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

###################################################################
#
#                       TEMPLATES
#
###################################################################

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\', '/'),)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "itsmurfs_techblog.context_processors.facebook_context_processor"

 )

###################################################################
#
#                       MIDDLEWARE
#
###################################################################

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

###################################################################
#
#                       APPLICATIONS
#
###################################################################

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'djcelery',
    'south',
    'taggit',
    'techblog',
    'itsmurfs_techblog',
    'mongoadminforms',
    'crossdb_utils'
)

###################################################################
#
#                           TECHBLOG
#
###################################################################
FRONT_IMAGE_SIZES = (
    ('facebook',(1200,630)),
)


###################################################################
#
#                           CELERY
#
###################################################################
from celery.schedules import timedelta, crontab

CELERYBEAT_SCHEDULE = {

    'entry_OneToOne_entryTagsCrossDb_check': {
        'task': 'techblog.tasks.entry_OneToOne_entryTagsCrossDb_check',
        'schedule': crontab(minute=0, hour=0)
    },
    'author_OneToMany_entry_check': {
        'task': 'techblog.tasks.author_ManyToMany_entry_check',
        'schedule': crontab(minute=0, hour=0)
    }

}

BROKER_URL = 'amqp://guest@localhost//'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

###################################################################
#
#                       LOGGING
#
###################################################################

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

###################################################################
#
#                 OTHERS (waiting for a place :D )
#
###################################################################

ROOT_URLCONF = 'itsmurfs_techblog.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'itsmurfs_techblog.wsgi.application'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

FACEBOOK_APP_ID = '846313175403086'