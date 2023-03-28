from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def company_view(request):
    return render(request, 'companies\company.html')


