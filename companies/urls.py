from django.urls import path, include
from .views import *


app_name = 'companies'

urlpatterns = [
    # post views
    path('', company_view, name='company'),


]