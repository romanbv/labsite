from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout



def index(request):
    return render(request, 'profile.html')


class HomeView(TemplateView):
    template_name = "home.html"


def pageNotFound(response, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')
