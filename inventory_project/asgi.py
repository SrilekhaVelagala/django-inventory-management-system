"""
asgi.py
-------
ASGI (Asynchronous Server Gateway Interface) is the modern successor
to WSGI, and it supports asynchronous features (e.g. WebSockets,
async views). Our project does not use any async features, but
Django generates this file for every new project by default so that
the project CAN be deployed on an ASGI server if needed in future.

Just like wsgi.py, this exposes an "application" callable that an
ASGI server (e.g. Daphne, Uvicorn) would use.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')

application = get_asgi_application()
