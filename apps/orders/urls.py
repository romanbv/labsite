from django.urls import path, include
from .views import *


app_name = 'orders'

urlpatterns = [
    # post views
    path('', ordersView.as_view(), name='orders'),
    path('order_add', addOrder.as_view(), name='order_add'),
    path('order_update/<int:pk>', updateOrder.as_view(), name='order_update'),
    path('<slug:order_num>', showOrder.as_view(), name='order'),




]