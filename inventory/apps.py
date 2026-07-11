"""
apps.py
-------
Every Django app has a small "AppConfig" class that stores metadata
about the app (its name, default settings, etc). Django uses this
when the app is registered inside INSTALLED_APPS in settings.py.

We rarely need to change this file - it is auto-generated when you
run "python manage.py startapp inventory".
"""
from django.apps import AppConfig


class InventoryConfig(AppConfig):
    # BigAutoField is the modern default primary key type (a 64-bit
    # integer) recommended by Django for new apps.
    default_auto_field = 'django.db.models.BigAutoField'

    # This must exactly match the app's folder name, and the name
    # used in INSTALLED_APPS in settings.py.
    name = 'inventory'
