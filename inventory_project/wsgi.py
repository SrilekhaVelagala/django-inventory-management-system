"""
wsgi.py
-------
WSGI (Web Server Gateway Interface) is the standard Python interface
between web servers and web applications.

This file exposes a module-level variable named ``application``.
Traditional production web servers (like Gunicorn, uWSGI, or Apache
with mod_wsgi) look for this variable to talk to our Django project.

For local development (python manage.py runserver) this file is not
directly used - Django's lightweight dev server handles requests
itself. This file matters mainly for real deployment, but Django
always generates it by convention.
"""

import os

from django.core.wsgi import get_wsgi_application

# Tell Django which settings file this WSGI application should use.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')

# get_wsgi_application() loads the Django app and returns a callable
# that a WSGI server can use to handle requests.
application = get_wsgi_application()
