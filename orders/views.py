from django.shortcuts import render, redirect, get_object_or_404


from .forms import *
from .models import *


def orders_view(request):
    UserOrders = Order.objects.filter(user = request.user.id)
    return render(request, 'orders/orders.html', {'orders':UserOrders})

def order_view(request, order_num ):
    UserOrder = get_object_or_404(Order, number = order_num)
    return render(request, 'orders/order.html', {'order':UserOrder})

def add_order(request):
    if request.method == "POST":
        form = addOrderForm( request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('account:profile', user_id=request.user.pk)
            except:
                form.add_error(None,'Ошибка создания заказа')
    else:
        form = addOrderForm()

    return render(request, 'orders/add_order.html', {'form':form, 'title':'Добавление заказа'})
