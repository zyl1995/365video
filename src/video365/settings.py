# -*- coding: utf-8 -*-
'''
Copyright Cobalys.com (c) 2011

This file is part of 365Video.

    365Video is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    365Video is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with 365Video.  If not, see <http://www.gnu.org/licenses/>.
'''
'''
Load Celery
''' 
import djcelery
djcelery.setup_loader()


'''
Production Settings
'''
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SITE_ID = 1
ROOT_URLCONF = 'video365.urls'
SECRET_KEY = '2^4=@x=c-cp&j95&%zk8@bf_(*!!aw$^l85dp0=&w-krc2#)t)'


'''
Administrators and Error Notification
'''
ADMINS = (
          #('Your name here', 'youmail@example.com'),
)
MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX = '[DJANGO-365VIDEO]'
SEND_BROKEN_LINKS_EMAIL = False

'''
Mail
'''
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.example.com'
#EMAIL_HOST_USER = 'notification@example.com'
#EMAIL_HOST_PASSWORD = 'password'
#EMAIL_PORT = 587


'''
Database
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                           # Or path to database file if using sqlite3.
        'USER': '',                           # Not used with sqlite3.
        'PASSWORD': '',                       # Not used with sqlite3.
        'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    }
}


'''
Internationalization
'''
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
DEFAULT_CHARSET = 'utf-8'
FORMAT_MODULE_PATH = 'video365.formats'

'''
Directories
'''
APPLICATION_DIR = '/usr/django/video365/'
MEDIA_ROOT = '/var/www/media/'
GENERATOR_DIR =  '%s/templates/layout/generated/' % APPLICATION_DIR
TEMPLATE_DIRS = (
                 '%stemplates' % APPLICATION_DIR
                )

PATH_VIDEOS = '%suploads/videos/' % MEDIA_ROOT
PATH_TEMP = '%suploads/temp/' % MEDIA_ROOT
PATH_SPLASH = '%suploads/splash/' % MEDIA_ROOT

APP_DOMAIN = "127.0.0.1"
APP_PATH = "/"

MEDIA_URL = '/media%s' % APP_PATH
LOGIN_REDIRECT_URL = '%sadmin/' % APP_PATH
LOGIN_URL = '%sadmin/login/' % APP_PATH


'''
Loaders
'''
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.media",
    "django.core.context_processors.auth",
    "django.core.context_processors.request",
    'video365.helpers.processors.path_context_processor',
)
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',
    'video365.apps.tag',
    'video365.apps.videopost',
    'djcelery',
    'djkombu',
)
