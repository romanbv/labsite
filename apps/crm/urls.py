from django.urls import path, include
from .views import *


app_name = 'crm'

urlpatterns = [
    # post views
    path('orders/', ordersView.as_view(), name='orders'),

    path('order_add', addOrder.as_view(), name='order_add'),
    path('order_update/<int:pk>', updateOrder.as_view(), name='order_update'),
    path('<slug:order_num>', showOrder.as_view(), name='order'),
    path('<int:company_id>', company_view, name='company'),
    path('add_company', add_company, name='add_company'),



]