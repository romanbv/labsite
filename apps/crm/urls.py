from django.urls import path, include
from .views import *


app_name = 'crm'

urlpatterns = [

    path('companies/orders/create/', OrderCreate.as_view(), name='order_create'),
    path('companies/orders/<slug:order_num>', OrderShow.as_view(), name='order'),
    path('companies/orders/update/<int:pk>/', OrderUpdate.as_view(), name='order_update'),
    path('companies/orders/', OrdersListView.as_view(), name='orders'),

    path('companies/create', CompanyCreate.as_view(), name='company_create'),
    path('companies/<int:company_id>', CompanyShow.as_view(), name='company'),
    path('companies/update/<int:pk>', CompanyUpdate.as_view(), name='company_update'),
    path('companies/', CompaniesListView.as_view(), name='companies'),

    path('companies/pricelists/create', PricelistCreate.as_view(), name='pricelist_create'),
    path('companies/pricelists/<int:pricelist_id>', PricelistShow.as_view(), name='pricelist'),
    path('companies/pricelists/update/<int:pk>', PricelistUpdate.as_view(), name='pricelist_update'),
    path('companies/pricelists', PricelistsListView.as_view(), name='pricelists'),

    path('companies/products/create', ProductCreate.as_view(), name='product_create'),
    path('companies/products/<int:product_id>', ProductShow.as_view(), name='product'),
    path('companies/products/update/<int:pk>', ProductUpdate.as_view(), name='product_update'),
    path('companies/products/', ProductsListView.as_view(), name='products'),


    path('delete-file/<int:pk>/', delete_file, name='delete_file'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    #path('orders/create/add_inline_form/<int:forms_count>', add_inline_form, name='add_inline_form'),




]
