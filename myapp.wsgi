import os
import sys
path = '/home/manga/projet-python/gestionServer'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'gestionServer.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()