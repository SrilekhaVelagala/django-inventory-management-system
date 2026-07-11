"""
models.py
---------
This file defines our DATABASE STRUCTURE using Django's ORM
(Object-Relational Mapper). Instead of writing raw SQL like:

    CREATE TABLE product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(200),
        category VARCHAR(100),
        ...
    );

...we simply write a Python class, and Django automatically
translates it into the correct SQL for whichever database backend
we are using (here, SQLite).

This is the "M" (Model) in Django's MVT (Model-View-Template)
architecture. The Model layer is solely responsible for defining
and interacting with the data.
"""
from django.db import models


class Product(models.Model):
    """
    The Product model represents one row in the "inventory_product"
    database table. Each field below becomes a column in that table.
    """

    # id: Django AUTOMATICALLY creates an "id" AutoField primary key
    # for every model unless you define your own primary key.
    # We do not need to write it explicitly - it is implicit.
    # (id = models.AutoField(primary_key=True) is added by Django behind the scenes)

    # CharField -> stored as VARCHAR(max_length) in SQLite.
    # Used for short text values. max_length is REQUIRED for CharField.
    name = models.CharField(
        max_length=200,
        help_text="Name of the product, e.g. 'Wireless Mouse'"
    )

    category = models.CharField(
        max_length=100,
        help_text="Category of the product, e.g. 'Electronics'"
    )

    # PositiveIntegerField -> stored as INTEGER, but Django's form
    # validation rejects negative numbers. Perfect for stock count,
    # since a product cannot have -5 items in stock.
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="Number of units currently in stock"
    )

    # DecimalField is used (instead of FloatField) for money values
    # because it stores EXACT decimal values with no floating-point
    # rounding errors - very important for prices/currency.
    # max_digits = total digits allowed, decimal_places = digits after the dot.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per unit in INR"
    )

    supplier = models.CharField(
        max_length=200,
        help_text="Name of the supplier/vendor who supplies this product"
    )

    # DateTimeField(auto_now_add=True) automatically stores the
    # current date & time ONLY when the object is first created.
    # It cannot be edited afterwards (Django hides it from forms).
    # Internally Django performs: created_at = datetime.now() at INSERT time.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders query results by newest-first by default, i.e.
        # Django will automatically add "ORDER BY created_at DESC"
        # to SELECT queries unless a different order is requested.
        ordering = ['-created_at']

    def __str__(self):
        """
        __str__ defines what is shown when a Product object is
        printed or displayed as text - for example, in the Django
        admin site's product list, or in a Python shell.
        Without this, Django would show something unhelpful like
        "Product object (1)".
        """
        return self.name
