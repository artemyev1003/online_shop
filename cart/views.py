from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """
    The view for adding products to the cart or updating quantities
    for existing products. The require_POST decorator is used to allow
    only POST requests. The view receives the product ID as a parameter.
    The Product instance is retrieved with the given ID and validate CartAddProductForm.
    If the form is valid, you either add or update the product in the cart.
    The view redirects to the cart_detail URL.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd["quantity"],
                 override_quantity=cd["override"])
        return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """
    The require_POST decorator is used to allow only POST requests.
    Retrieves the Product instance with the given ID
    and removes the product from the cart.
    Then, redirects the user to the cart_detail URL.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})

