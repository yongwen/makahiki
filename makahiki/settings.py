"""Django settings file containing system-level settings."""

import os
import urlparse
import sys

###############
# PATH settings
###############
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ROOT_URLCONF = 'urls'

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
    ]

# directories which hold static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
    )

# URL that handles the static files such as css, img, and js
STATIC_URL = "/site_media/static/"

# Absolute path to the directory that holds static files.
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')

# prefix for all uploaded media files
MAKAHIKI_MEDIA_PREFIX = "media"

#######################
# Template settings
#######################
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(PROJECT_ROOT, "apps"),
    )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    'django.contrib.messages.context_processors.messages',
    "apps.managers.challenge_mgr.context_processors.competition",
    )

######################
# MIDDLEWARE settings
######################
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    #always start with this for caching

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'apps.lib.django_cas.middleware.CASMiddleware',

    'apps.managers.player_mgr.middleware.LoginMiddleware',
    'apps.managers.log_mgr.middleware.LoggingMiddleware',

    'django.middleware.cache.FetchFromCacheMiddleware',
    #always end with this for caching
    )

######################
# AUTH settings
######################
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.managers.auth_mgr.cas_backend.MakahikiCASBackend',
    #'apps.managers.auth_mgr.ldap_backend.MakahikiLDAPBackend',
    )

AUTH_PROFILE_MODULE = 'player_mgr.Profile'

###################
# Authentication
###################
LOGIN_URL = "/account/cas/login/"
LOGIN_REDIRECT_URLNAME = "home_index"
LOGIN_REDIRECT_URL = "/home"
RESTRICTED_URL = '/restricted/'

#################
# CACHE settings
#################
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 600

#########################
# INSTALLED_APPS settings
#########################
INSTALLED_APPS = (
    # Makahiki pages
    'apps.template_support',
    'apps.pages',

    # Makahiki components
    'apps.managers.auth_mgr',
    'apps.managers.challenge_mgr',
    'apps.managers.team_mgr',
    'apps.managers.resource_mgr',
    'apps.managers.player_mgr',
    'apps.managers.score_mgr',
    'apps.managers.cache_mgr',
    'apps.test_helpers',

    # 3rd party libraries
    'apps.lib.django_cas',
    'apps.lib.brabeion',
    'apps.lib.facebook_api',
    'apps.lib.avatar',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',

    # external
    'django_extensions',
    'gunicorn',
    'storages',
)

################################
# INSTALLED DEFAULT Widgets for all pages
################################
INSTALLED_DEFAULT_WIDGET_APPS = (
    'quests',
    'notifications',
    'ask_admin',
    'home',
    'help',
)
for widget in INSTALLED_DEFAULT_WIDGET_APPS:
    INSTALLED_APPS += ("apps.widgets." + widget, )

################################
# INSTALLED Widgets
################################
INSTALLED_WIDGET_APPS = (
    'ask_admin',
    'badges',
    'canopy_viz',
    'canopy_member',
    'resource_goal',
    'resource_goal.energy',
    'resource_goal.water',
    'energy_power_meter',
    'resource_scoreboard',
    'resource_scoreboard.energy',
    'resource_scoreboard.water',
    'my_achievements',
    'my_commitments',
    'my_info',
    'popular_tasks',
    'prizes',
    'quests',
    'raffle',
    'scoreboard',
    'smartgrid',
    'team_members',
    'upcoming_events',
    'wallpost',
    'help.intro',
    'help.faq',
    'help.rule',
    'status',
    'status.prizes',
    'status.rsvps',
    'status.users',
    'status.actions',
)

for widget in INSTALLED_WIDGET_APPS:
    INSTALLED_APPS += ("apps.widgets." + widget, )

# migration support, need to be the last app.
# nose has to be after south!
INSTALLED_APPS += ('south', 'django_nose',)

################
# INSTALLED Theme
################
INSTALLED_THEMES = (
    'theme-default',
    'theme-wave',
)

################
# TEST settings
################
# South
SOUTH_TESTS_MIGRATE = False

# Use Nose as the test runner.
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

##############################
# LOGGING settings
##############################
# Default log file location.
LOG_FILE = 'makahiki.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %'
                      '(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
            },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'simple',
            }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
            },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            },
        'makahiki_logger': {
            'handlers': ['file'],
            'level': 'INFO',
            }
    }
}

#########################
# MISC
#########################

# Permissions for large uploaded files.
FILE_UPLOAD_PERMISSIONS = 0644

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Locale Info
TIME_ZONE = 'Pacific/Honolulu'
LOCALE_SETTING = 'en'
LANGUAGE_CODE = 'en_US.UTF-8'

# Markdown info
MARKDOWN_LINK = "http://daringfireball.net/projects/markdown/syntax"
MARKDOWN_TEXT = "Uses <a href=\"" + MARKDOWN_LINK + "\" target=\"_blank\">Markdown</a> formatting."

SERIALIZATION_MODULES = {
    'csv': 'snippetscream.csv_serializer',
    }


##############################
# Dummy setting for CHALLENGE
##############################
# set the dummpy challenge object to by pass reference check.
# It should be overridden from the DB ChallengeSettings object.
class Challenge():
    """Defines the dummy global settings for the challenge. """
    competition_name = None

CHALLENGE = Challenge()
COMPETITION_ROUNDS = None

#############################################
# Load sensitive settings from OS environment
#############################################
# DB settings
if 'DATABASE_URL' in os.environ:
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    if url.scheme == 'postgres':
        DATABASES = {}
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
            }
else:
    if 'READTHEDOCS' not in os.environ:
        print "Environment variable DATABASE_URL not defined. Exiting."
        sys.exit(1)

# Admin info Settings
if 'MAKAHIKI_ADMIN_INFO' in os.environ:
    admin_info = os.environ['MAKAHIKI_ADMIN_INFO'].split(":")
    ADMIN_USER = admin_info[0]
    ADMIN_PASSWORD = admin_info[1]
else:
    if 'READTHEDOCS' not in os.environ:
        print "Environment variable MAKAHIKI_ADMIN_INFO not defined. Exiting."
        sys.exit(1)

# email Settings
if 'MAKAHIKI_EMAIL_INFO' in os.environ:
    email_info = os.environ['MAKAHIKI_EMAIL_INFO'].split(":")
    EMAIL_HOST_USER = email_info[0]
    EMAIL_HOST_PASSWORD = email_info[1]

# Helper lambda for retrieving environment variables:
env = lambda e, d: os.environ[e] if e in os.environ else d

# DEBUG settings
MAKAHIKI_DEBUG = env('MAKAHIKI_DEBUG', '').lower() == "true"
DEBUG = MAKAHIKI_DEBUG
TEMPLATE_DEBUG = MAKAHIKI_DEBUG

# CACHE settings
if env('MAKAHIKI_MEMCACHED_ENABLED', '').lower() == "true":
    CACHES = {'default':
                {'BACKEND': 'django_pylibmc.memcached.PyLibMCCache'}}
else:
    CACHES = {'default':
                {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

# static media settings
MAKAHIKI_USE_S3 = env('MAKAHIKI_USE_S3', '').lower() == "true"
if MAKAHIKI_USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    #STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', '')

    MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    SERVE_MEDIA = False
else:
    # URL that handles the media files such as uploads.
    MEDIA_URL = "/site_media/"
    # Absolute path to the directory that holds media.
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')
    # serve media through django.views.static.serve.
    SERVE_MEDIA = True

# settings to use less files
MAKAHIKI_USE_LESS = env('MAKAHIKI_USE_LESS', '').lower() == "true"

# LDAP settings
AUTH_LDAP_BIND_DN = env('MAKAHIKI_LDAP_BIND_DN', '')
AUTH_LDAP_BIND_PASSWORD = env('MAKAHIKI_LDAP_BIND_PWD', '')

# django secret key
SECRET_KEY = env('MAKAHIKI_SECRET_KEY', '')

# facebook key
FACEBOOK_APP_ID = env('MAKAHIKI_FACEBOOK_APP_ID', '')
FACEBOOK_SECRET_KEY = env('MAKAHIKI_FACEBOOK_SECRET_KEY', '')
