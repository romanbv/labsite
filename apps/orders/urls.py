from django.urls import path, include
from .views import *


app_name = 'orders'

urlpatterns = [
    # post views
    path('', OrdersView.as_view(), name='orders'),
    path('add_order', add_order, name='add_order'),
    path('<slug:order_num>', ShowOrder.as_view(), name='order'),




]