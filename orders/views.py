from django.shortcuts import render
from .models import *


def orders_view(request):
    UserOrders = Order.objects.filter(user = request.user.id)
    return render(request, 'orders/orders.html', {'orders':UserOrders})

def order_view(request, order_num ):
    UserOrder = Order.objects.get(number = order_num)
    return render(request, 'orders/order.html', {'order':UserOrder})



