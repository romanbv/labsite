from django.shortcuts import render
from .models import Company


# Create your views here.



def company_view(request, company_id):
    company = Company.objects.get(pk=company_id)
    return render(request, 'companies/company.html', {'company':company})


