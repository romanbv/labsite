from django.urls import path, include
from .views import *


app_name = 'companies'

urlpatterns = [
    # post views
    path('<int:company_id>', company_view, name='company'),
    path('add_company', add_company, name='add_company'),



]