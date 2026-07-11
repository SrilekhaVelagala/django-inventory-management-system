"""
urls.py (APP LEVEL)
--------------------
This file maps URL paths to their corresponding view functions for
the "inventory" app. The project-level urls.py includes this file
using include('inventory.urls').

Each path() has three parts:
    1. The URL pattern (the part after the domain name)
    2. The view function to call
    3. A "name" - used elsewhere in the project (templates, views)
       to generate links WITHOUT hard-coding the URL string, e.g.
       {% url 'product_list' %} or redirect('product_list').
       This means if we ever change the URL path itself, we don't
       have to hunt down every hard-coded link in the project.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Root URL ('') -> redirects to login page via the login_view
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard (home page after login)
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Product CRUD URLs
    path('products/', views.product_list_view, name='product_list'),
    path('products/add/', views.add_product_view, name='add_product'),
    path('products/<int:pk>/edit/', views.update_product_view, name='update_product'),
    path('products/<int:pk>/delete/', views.delete_product_view, name='delete_product'),
]
