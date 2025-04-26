from decimal import Decimal
from store.models import Product

class Basket:
    """Handles session-based shopping cart functionality."""

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if not basket:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        """Add or update product quantity in the basket."""
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
        """Iterate over basket items and attach product details."""
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
        """Total number of items (sum of quantities)."""
        return sum(item['qty'] for item in self.basket.values())

    def update(self, product_id, qty):
        """Update quantity of a product in the basket."""
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
            self.save()

    def delete(self, product_id):
        """Remove a product from the basket."""
        product_id = str(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def get_total_price(self):
        """Calculate total basket price."""
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def save(self):
        """Mark the session as modified to save changes."""
        self.session.modified = True
