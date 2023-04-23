import os
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
import yadisk
#API
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from apps.companies.models import Company
from apps.orders.models import Order

#from django.contrib.auth.models import User

from .forms import *


class HomeView(TemplateView):
    template_name = "home.html"

def pageNotFound(response, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')



    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

    # def get_success_url(self):
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('account:login')

def check_token(request):

    try:
        y = yadisk.YaDisk('4bf5384cd0904299a07adcb616cc0e08', 'cc9a5b4b894e40649b8e2bd8be5aad5f',
                          'y0_AgAAAAALE7y3AAm3GAAAAADhGLoR90SrSie4Q7Sh8hEJ6f29c5MBG9E')
        if not y.exists('/test_dir'):
            y.mkdir('/test_dir')
        file_ = open(os.path.join(settings.MEDIA_ROOT, '/uploads/test_file.txt'))
        y.upload(file_, '/test_dir/testfile.txt')
        check_result = 'Загружен файл'
    except:
        check_result = 'Ошибка загрузки'




    return render(request, 'account/profile.html', {'check_result':check_result})

@login_required
def profile_view(request, user_id):
    UserCompanies   = Company.objects.filter(owner=user_id)
    UserOrders      = Order.objects.filter(user=user_id)
    user_profile    = User.objects.get(pk= user_id)
    return render(request, 'account/profile.html', {'companies':UserCompanies, 'orders':UserOrders, 'user':user_profile})

def password_change_view(request):
    return render(request, 'account/profile.html')


class GetUserInfoView(APIView):
    def get(self, request):
        # Извлекаем набор всех записей из таблицы Capital
        queryset = User.objects.all()
        # Создаём сериалайзер для извлечённого наборa записей
        serializer_for_queryset = UserSerializer(
            instance=queryset,  # Передаём набор записей
            many=True  # На вход подается именно набор, а не одна запись
        )
        return Response(serializer_for_queryset.data)