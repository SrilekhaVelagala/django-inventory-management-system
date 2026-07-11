"""
admin.py
--------
Django ships with a built-in, auto-generated admin website at
/admin/. To make our Product model manageable through this admin
site, we must "register" it here.

Once registered, the superuser can log into /admin/ and add/edit/
delete Product rows through a ready-made interface - WITHOUT us
writing any extra code for it.
"""
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    ProductAdmin customises HOW the Product model looks inside the
    Django admin site. This is optional - admin.site.register(Product)
    alone would work - but customising it makes the admin list page
    far more useful.
    """
    # Columns to display in the admin's product list page.
    list_display = ('name', 'category', 'quantity', 'price', 'supplier', 'created_at')

    # Adds a sidebar filter so the admin can quickly filter products
    # by category.
    list_filter = ('category',)

    # Adds a search box at the top of the admin list page that
    # searches these fields (uses SQL LIKE queries internally).
    search_fields = ('name', 'category', 'supplier')

    # Orders the admin list by newest first.
    ordering = ('-created_at',)
