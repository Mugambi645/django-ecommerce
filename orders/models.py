from decimal import Decimal
from django.conf import settings
from django.db import models

from store.models import Product


class Order(models.Model):
    """
    Model representing a customer's order.

    Attributes:
        user (ForeignKey): The user who placed the order.
        full_name (CharField): Customer's full name.
        address1 (CharField): Primary address line.
        address2 (CharField): Secondary address line.
        city (CharField): City of the customer.
        phone (CharField): Customer's contact number.
        post_code (CharField): Postal code.
        created (DateTimeField): Timestamp when the order was created.
        updated (DateTimeField): Timestamp when the order was last updated.
        total_paid (DecimalField): Total amount paid for the order.
        order_key (CharField): Unique identifier for the order.
        billing_status (BooleanField): Payment status (True if paid).

    Meta:
        ordering (tuple): Orders are sorted by most recent creation date first.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        """
        String representation of the Order showing the creation date.
        """
        return str(self.created)


class OrderItem(models.Model):
    """
    Model representing a single item within an order.

    Attributes:
        order (ForeignKey): Reference to the related Order.
        product (ForeignKey): Reference to the purchased Product.
        price (DecimalField): Price of a single product item.
        quantity (PositiveIntegerField): Quantity of the product ordered.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        String representation of the OrderItem showing its ID.
        """
        return str(self.id)
