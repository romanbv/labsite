from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from orders.models import *


# Create your views here.



def company_view(request, company_id):
    company = Company.objects.get(pk=company_id)
    UserOrders = Order.objects.filter(user=request.user.id, company = company_id)
    return render(request, 'companies/company.html', {'company':company, 'orders':UserOrders})


