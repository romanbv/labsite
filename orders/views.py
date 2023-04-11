from django.shortcuts import render, redirect

from .forms import *
from .models import *


def orders_view(request):
    UserOrders = Order.objects.filter(user = request.user.id)
    return render(request, 'orders/orders.html', {'orders':UserOrders})

def order_view(request, order_num ):
    UserOrder = Order.objects.get(number = order_num)
    return render(request, 'orders/order.html', {'order':UserOrder})

def addorder(request):
    if request.method == "POST":
        form = addOrderForm( request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')
            except:
                form.add_error(None,'Ошибка создания заказа')
    else:
        form = addOrderForm()

    return render(request, 'orders/addorder.html', {'form':form, 'title':'Добавление заказа'})
