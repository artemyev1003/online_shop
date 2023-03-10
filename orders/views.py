from django.shortcuts import render, redirect, reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item["product"],
                                         price=item["price"],
                                         quantity=item["quantity"])
            cart.clear()
            return redirect(reverse("orders:successful_order", args=[order.id]))
    else:
        form = OrderCreateForm()
        return render(request, "orders/order/create.html",
                      {"cart": cart, "form": form})


def successful_order(request, order_id):
    return render(request, "orders/order/created.html", {"order_id": order_id})
