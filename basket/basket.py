from decimal import Decimal

from django.conf import settings
from store.models import Product


class Basket:
    """
    A base Basket class, providing default behaviors for managing
    a shopping basket using Django sessions.
    """

    def __init__(self, request):
        """
        Initialize the basket.
        If no basket is in the session, create an empty one.
        
        :param request: Django HttpRequest object
        """
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Add a product to the basket or update its quantity.

        :param product: Product instance to add
        :param qty: Quantity of the product
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        else:
            self.basket[product_id] = {"price": str(product.regular_price), "qty": qty}

        self.save()

    def __iter__(self):
        """
        Iterate over the basket items and attach the product instances.
        Also calculate the total price per item.
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Count all items in the basket.

        :return: Total quantity of all basket items
        """
        return sum(item["qty"] for item in self.basket.values())

    def update(self, product, qty):
        """
        Update the quantity of a product in the basket.

        :param product: Product instance to update
        :param qty: New quantity
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        self.save()

    def get_subtotal_price(self):
        """
        Calculate the subtotal of all items in the basket.

        :return: Subtotal as Decimal
        """
        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

    def get_total_price(self):
        """
        Calculate the total price including a fixed shipping cost.

        :return: Total price as Decimal
        """
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + shipping
        return total

    def delete(self, product):
        """
        Remove a product from the basket.

        :param product: Product instance to remove
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        """
        Remove the entire basket from the session.
        """
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        """
        Mark the session as modified to make sure it's saved.
        """
        self.session.modified = True
