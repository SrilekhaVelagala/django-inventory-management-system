"""
settings.py
-----------
This file contains ALL the configuration for our Django project:
database settings, installed apps, middleware, templates, static
files, etc. Django reads this file automatically when the server
starts (because manage.py sets DJANGO_SETTINGS_MODULE to point here).

For this academic project we deliberately keep the settings SIMPLE:
- SQLite database (no external database server needed)
- No REST framework, no Celery, no Redis
- Only what is required to run a basic CRUD + login app
"""

from pathlib import Path

# BASE_DIR points to the root folder of the project (the folder that
# contains manage.py). We build every other path relative to this,
# so the project works on any computer/operating system.
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
# Django uses this key internally for cryptographic signing
# (e.g. session cookies, CSRF tokens). In a real company project
# this would be loaded from an environment variable, but for a
# college/academic demo project a hard-coded key is fine.
# -----------------------------------------------------------------
SECRET_KEY = 'django-insecure-academic-project-secret-key-change-me'

# DEBUG = True shows detailed error pages while developing.
# Must be set to False in a real production deployment.
DEBUG = True

# ALLOWED_HOSTS lists the domain names/IPs allowed to serve this
# Django project. Empty list + DEBUG=True works fine for localhost.
ALLOWED_HOSTS = []


# -----------------------------------------------------------------
# INSTALLED_APPS: every Django "app" (feature module) that is part
# of this project must be registered here. Django uses this list to
# know which models, templates, and admin configurations to load.
# -----------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',        # built-in admin site
    'django.contrib.auth',         # built-in authentication system (login/logout/users)
    'django.contrib.contenttypes', # framework used internally by auth/admin
    'django.contrib.sessions',     # stores login session data (who is logged in)
    'django.contrib.messages',     # one-time flash messages (e.g. "Product added!")
    'django.contrib.staticfiles',  # manages CSS/JS/image files

    'inventory',                   # OUR own app that contains the Product model, views, etc.
]

# -----------------------------------------------------------------
# MIDDLEWARE: a chain of "hooks" that process every request/response.
# Order matters. Each class in this list does one small job -
# for example, SessionMiddleware attaches session data to every
# request, AuthenticationMiddleware attaches the logged-in user.
# -----------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',        # protects forms against CSRF attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # attaches request.user
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF tells Django which file contains the master URL list.
# Django looks here first for every incoming request URL.
ROOT_URLCONF = 'inventory_project.urls'

# -----------------------------------------------------------------
# TEMPLATES: tells Django's template engine where to look for HTML
# files. We use a single project-level "templates" folder (instead
# of an app-level templates folder) to keep things simple and easy
# to explain.
# -----------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # our custom templates folder
        'APP_DIRS': True,  # also look inside each app's own /templates folder
        'OPTIONS': {
            'context_processors': [
                # context processors inject extra variables into every
                # template automatically, e.g. {{ user }} and {{ messages }}
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION points to the WSGI entry point used when
# deploying with a traditional web server (e.g. Gunicorn + Nginx).
WSGI_APPLICATION = 'inventory_project.wsgi.application'


# -----------------------------------------------------------------
# DATABASE CONFIGURATION
# We use SQLite because it requires ZERO setup - it is just a single
# file (db.sqlite3) stored inside the project folder. This is ideal
# for an academic project and for interviews, since there is no
# separate database server to install or configure.
# -----------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -----------------------------------------------------------------
# PASSWORD VALIDATION
# Django ships with built-in validators that reject weak passwords
# (too short, too common, all numeric, similar to username, etc.)
# -----------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization settings (language + timezone)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # set to Indian Standard Time for this project
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------
# STATIC FILES (CSS, JavaScript, images)
# STATIC_URL is the prefix used in templates: {% static 'css/style.css' %}
# STATICFILES_DIRS tells Django where our custom static folder lives
# during development.
# -----------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type for models that don't specify one.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------------------------------------------
# LOGIN/LOGOUT REDIRECT SETTINGS
# These tell Django's auth system where to send the user after they
# log in or log out, and where to redirect if @login_required blocks
# access to a page.
# -----------------------------------------------------------------
LOGIN_URL = 'login'                 # name of the URL pattern for our login page
LOGIN_REDIRECT_URL = 'dashboard'    # where to go after a successful login
LOGOUT_REDIRECT_URL = 'login'       # where to go after logging out
