from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):

    return render(request, 'base.html')


class HomeView(TemplateView):
    template_name = "home.html"



