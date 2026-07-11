"""
views.py
--------
This file contains the "V" (View) in Django's MVT architecture.

A VIEW is simply a Python function that:
    1. Receives an HttpRequest object (information about what the
       browser is asking for).
    2. Talks to the Model layer (Product) to fetch/save/update/delete
       data using the Django ORM.
    3. Returns an HttpResponse - usually by rendering an HTML
       template with render(), or by redirecting the browser
       elsewhere with redirect().

We use ONLY Function-Based Views (FBVs) in this project (no
class-based views) because FBVs are simpler to read top-to-bottom
and easier to explain line-by-line in an interview.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product
from .forms import ProductForm


# =====================================================================
# AUTHENTICATION VIEWS
# =====================================================================

def login_view(request):
    """
    Handles user login.

    GET request  -> simply display the empty login form.
    POST request -> the browser submitted the login form, so we
                    validate the username/password against the
                    database and log the user in.

    WHY NOT @login_required HERE?
    This is the login page itself - a NOT-yet-logged-in user must be
    able to reach it, so we deliberately do NOT protect it with
    @login_required (that would create an infinite redirect loop).
    """
    # request.method tells us whether the browser sent a GET request
    # (just opening the page) or a POST request (submitting a form).
    if request.method == 'POST':
        # request.POST is a dictionary-like object containing all
        # form field values submitted by the browser.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate() checks the given username/password against
        # Django's built-in auth_user table. It returns a User object
        # if the credentials are correct, or None if they are wrong.
        # Internally Django performs a SELECT on the auth_user table
        # and verifies the hashed password.
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login() creates a session for this user and stores the
            # session ID in a cookie in the browser. From now on,
            # request.user will return this logged-in user on every
            # subsequent request.
            login(request, user)
            return redirect('dashboard')  # redirect() sends the browser to the dashboard URL
        else:
            # messages.error() stores a one-time "flash message" that
            # we display once on the next page render (see login.html).
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')

    # For a plain GET request, just show the blank login form.
    # render() combines a template file with a context dictionary
    # and returns a proper HttpResponse containing the final HTML.
    return render(request, 'login.html')


def logout_view(request):
    """
    Logs the current user out.

    logout() clears the session data associated with this browser,
    so request.user becomes AnonymousUser again on future requests.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# =====================================================================
# DASHBOARD VIEW
# =====================================================================

@login_required
def dashboard_view(request):
    """
    Displays the main dashboard after login.

    WHY @login_required?
    This decorator wraps the view function and checks, BEFORE the
    view code runs, whether request.user is authenticated. If not,
    it automatically redirects the browser to the URL named in
    LOGIN_URL (settings.py) - i.e. our login page. This saves us
    from manually writing "if not request.user.is_authenticated:
    redirect(...)" in every single protected view.
    """
    # Product.objects.count() executes a SQL "SELECT COUNT(*) FROM
    # inventory_product;" query - it is more efficient than fetching
    # every row and using Python's len(), because the counting
    # happens inside the database itself.
    total_products = Product.objects.count()

    # context is a dictionary of variables we want to make available
    # inside the dashboard.html template, e.g. {{ total_products }}
    context = {
        'total_products': total_products,
    }
    return render(request, 'dashboard.html', context)


# =====================================================================
# PRODUCT CRUD VIEWS  (Create, Read, Update, Delete)
# =====================================================================

@login_required
def product_list_view(request):
    """
    READ operation - displays every product, with an optional search
    by name.
    """
    # request.GET.get('q', '') reads the "q" query parameter from the
    # URL, e.g. /products/?q=mouse -> returns "mouse".
    # The second argument '' is the default value if "q" is missing.
    search_query = request.GET.get('q', '')

    if search_query:
        # Product.objects.filter(name__icontains=search_query) builds
        # a SQL query like:
        #   SELECT * FROM inventory_product
        #   WHERE name LIKE '%search_query%';
        # "icontains" means "case-insensitive contains", so searching
        # "mouse" also matches "Wireless Mouse" and "MOUSE PAD".
        products = Product.objects.filter(name__icontains=search_query)
    else:
        # Product.objects.all() executes:
        #   SELECT * FROM inventory_product ORDER BY created_at DESC;
        # (the ORDER BY comes from Meta.ordering in models.py)
        # This returns ALL rows in the product table as a QuerySet.
        products = Product.objects.all()

    context = {
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'product_list.html', context)


@login_required
def add_product_view(request):
    """
    CREATE operation - adds a brand-new product to the database.
    """
    if request.method == 'POST':
        # We pass request.POST into the ModelForm so it can validate
        # the submitted data against the Product model's field rules.
        form = ProductForm(request.POST)

        # form.is_valid() runs all validation checks (required
        # fields, correct data types, max_length limits, etc.) and
        # returns True only if every field passes.
        if form.is_valid():
            # form.save() takes the cleaned/validated data and
            # performs the actual database INSERT for us:
            #   INSERT INTO inventory_product (name, category, ...)
            #   VALUES (?, ?, ...);
            # It returns the newly created Product object.
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        # GET request -> show a blank form for the user to fill in.
        form = ProductForm()

    context = {
        'form': form,
        'title': 'Add Product',
    }
    return render(request, 'product_form.html', context)


@login_required
def update_product_view(request, pk):
    """
    UPDATE operation - edits an existing product.

    'pk' (primary key) arrives from the URL, e.g. /products/5/edit/
    means pk = 5.

    WHY get_object_or_404() INSTEAD OF Product.objects.get(pk=pk)?
    ------------------------------------------------------------
    Product.objects.get(pk=pk) raises a Product.DoesNotExist
    exception if no row matches, which would crash the app with an
    ugly server error (HTTP 500) if someone visits an invalid URL
    like /products/9999/edit/.
    get_object_or_404() does the exact same ORM lookup internally,
    but automatically catches that exception and returns a clean,
    user-friendly "404 Page Not Found" response instead - much
    safer and more professional.
    """
    # Internally this runs: SELECT * FROM inventory_product WHERE id = pk;
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # instance=product tells the ModelForm "update THIS existing
        # row" instead of creating a new one. Without 'instance',
        # form.save() would create a brand-new Product row.
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            # Because 'instance=product' was supplied, form.save()
            # now performs an UPDATE instead of an INSERT:
            #   UPDATE inventory_product
            #   SET name=?, category=?, quantity=?, price=?, supplier=?
            #   WHERE id = pk;
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        # GET request -> pre-fill the form with the product's
        # current values, so the user can see and edit them.
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'title': 'Update Product',
    }
    return render(request, 'product_form.html', context)


@login_required
def delete_product_view(request, pk):
    """
    DELETE operation - removes a product from the database.

    We show a confirmation page first (GET) instead of deleting
    immediately, so the user does not accidentally delete data by
    clicking a link. The actual deletion only happens on POST,
    after the user confirms.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # product.delete() executes:
        #   DELETE FROM inventory_product WHERE id = pk;
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')

    # GET request -> show the "Are you sure?" confirmation page.
    context = {
        'product': product,
    }
    return render(request, 'product_confirm_delete.html', context)
