import sys
import os

sys.path.append('/usr/django')
os.environ["CELERY_LOADER"] = "django"
os.environ['DJANGO_SETTINGS_MODULE'] = 'video365.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
