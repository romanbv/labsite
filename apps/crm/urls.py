from django.urls import path, include
from .views import *


app_name = 'crm'

urlpatterns = [
    # post views
    path('orders/', ordersView.as_view(), name='orders'),

    path('orders/order_add', addOrder.as_view(), name='order_add'),
    path('orders/order_update/<int:pk>', updateOrder.as_view(), name='order_update'),
    path('orders/<slug:order_num>', showOrder.as_view(), name='order'),
    path('company/<int:company_id>', showCompany.as_view(), name='company'),
    path('company/company_add', addCompany.as_view(), name='add_company'),
    path('company/company_update/<int:pk>', updateCompany.as_view(), name='update_company'),
    path('company/pricelist', priceListView.as_view(), name='pricelist'),



]