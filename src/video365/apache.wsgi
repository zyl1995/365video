import sys
import os

os.environ["CELERY_LOADER"] = "django"
sys.path.append('/usr/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'video365.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
