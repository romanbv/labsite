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
    user = request.user
    if request.method == "POST":
        form = addOrderForm( request.POST)
        file_form = OrderFileModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        if form.is_valid() and file_form.is_valid():
            try:
                order_instance = form.save(commit=False)
                order_instance.user = user
                order_instance.save()
                for f in files:
                    file_instance = OrderFile(file=f, order=order_instance, owner = user)
                    file_instance.save()
                return redirect('account:profile', user_id=request.user.pk)
            except:
                form.add_error(None,'Ошибка создания заказа')
                file_form.add_error(None,'Ошибка загрузки файла')
    else:
        form = addOrderForm()
        file_form = OrderFileModelForm()

    return render(request, 'orders/add_order.html', {'form':form, 'title':'Добавление заказа', 'file_form':file_form})

def add_file(request):
    return render(request, 'account/profile.html')
