from decimal import Decimal
from django.conf import settings
from myshop.shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # If a cart does not exist, save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity: int = 1,
            override_quantity: bool = False):
        """
        Add a product to the cart or update its quantity.
        """

        """
        Convert the product ID into a string because Django 
        uses JSON to serialize session data, and JSON only 
        allows string key names.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            """
            The product's price is converted from decimal 
            into a string in order to serialize it.
            """
            self.cart[product_id] = {"quantity": 0,
                                     "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        """
        By default, Django only saves to the session database when
        the session has been modified – that is if any of its dictionary
        values have been assigned or deleted.
        We tell the session object explicitly that it has been
        modified by setting the modified attribute on the session object.
        """
        self.session.modified = True

    def remove(self, product: Product):
        """
        Removes a product from a cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
