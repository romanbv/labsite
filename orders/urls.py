from django.urls import path, include
from .views import *


app_name = 'orders'

urlpatterns = [
    # post views
    path('', orders_view, name='orders'),
    path('<slug:order_num>', order_view, name='order'),
    path('addorder', addorder, name='addorder'),


]