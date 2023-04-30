from django.shortcuts import render, redirect
from .forms import *


# Create your views here.



def company_view(request, company_id):
    company = Company.objects.get(pk=company_id)
    UserOrders = Order.objects.filter(user=request.user.id, company = company_id)
    return render(request, 'companies/company.html', {'company':company, 'orders':UserOrders})


def add_company(request):
    if request.method == "POST":
        form = addCompanyForm( request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('userprofiles:profile', user_id=request.user.pk)
            except:
                form.add_error(None,'Ошибка создания компании')
    else:
        form = addCompanyForm()

    return render(request, 'companies/add_company.html', {'form':form, 'title':'Добавление компании'})