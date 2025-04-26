from decimal import Decimal
from store.models import Product


class Basket:
    """
    A base Basket class that handles session-based shopping cart functionality.
    Supports adding, updating, deleting, and iterating over basket items.
    """

    def __init__(self, request):
        """
        Initialize the basket with the current session data.
        If no basket exists in the session, create an empty one.
        """
        self.session = request.session
        basket = self.session.get('skey')
        if not basket:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Add a product to the basket or update its quantity if it already exists.

        Args:
            product (Product): The product instance to add.
            qty (int): The quantity of the product.
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {
                'price': str(product.price),
                'qty': qty,
            }
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the basket, fetching products from the database,
        and yielding each item with its full product details, price, and total price.
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Return the total number of items in the basket (sum of quantities).
        """
        return sum(item['qty'] for item in self.basket.values())

    def update(self, product, qty):
        """
        Update the quantity of a specific product in the basket.

        Args:
            product (Product): The product instance whose quantity should be updated.
            qty (int): The new quantity.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
            self.save()

    def get_total_price(self):
        """
        Calculate and return the total price of all items in the basket.

        Returns:
            Decimal: The total price.
        """
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        """
        Remove a product from the basket.

        Args:
            product (Product): The product instance to remove.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def save(self):
        """
        Mark the session as modified to ensure it is saved.
        """
        self.session.modified = True


