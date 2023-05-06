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
    path('company/company_add', addCompany.as_view(), name='company_add'),
    path('company/company_update/<int:pk>', updateCompany.as_view(), name='company_update'),
    path('company/pricelist/<int:pricelist_id>', priceListView.as_view(), name='pricelist'),
    path('company/pricelist_add', addPricelist.as_view(), name='pricelist_add'),
    path('company/pricelist_update/<int:pk>', updatePricelist.as_view(), name='pricelist_update'),
    path('company/product/<int:product_id>', showProduct.as_view(), name='product'),
    path('company/product_add', addProduct.as_view(), name='product_add'),
    path('company/product_update/<int:pk>', updateProduct.as_view(), name='product_update'),



]