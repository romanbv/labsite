import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
#API
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer


# Яндекс Диск
import yadisk

#Другие приложения
from apps.common.forms import UserForm, ProfileForm
from apps.orders.models import Order
from apps.companies.models import Company


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'userprofiles/profile.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        UserCompanies = Company.objects.filter(owner=self.request.user.id)
        UserOrders = Order.objects.filter(user=self.request.user.id)[:5]


        context = super().get_context_data(**kwargs)
        context['companies'] = UserCompanies
        context['orders'] = UserOrders
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Профиль', 'url': reverse_lazy('profile')},
        ]


        return context

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'userprofiles/profile-update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Профиль', 'url': reverse_lazy('profile')},
        ]

        return context
    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Ваш профиль успешно обновлен!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

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
        check_result = 'Ошибка загрузки файла на Яндекс Диск'


    return render(request, 'userprofiles/profile.html', {'message':check_result})


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