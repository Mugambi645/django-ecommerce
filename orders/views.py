from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from django.shortcuts import render

from basket.basket import Basket

from .models import Order, OrderItem


def add(request):
    """
    Create a new order and associated order items based on the current user's basket.

    If an order with the same order key already exists, no new order is created.
    Responds with a JSON success message after processing the order.
    """
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name='name',
                address1='add1',
                address2='add2',
                total_paid=baskettotal,
                order_key=order_key
            )
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty']
                )

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    """
    Update the billing status of an order to True after payment confirmation.

    Args:
        data (str): The order key of the order to be updated.
    """
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    """
    Retrieve all completed (paid) orders for the current logged-in user.

    Returns:
        QuerySet: A queryset of orders where billing_status is True.
    """
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
