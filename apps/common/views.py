from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from .forms import SignUpForm
from django.http import  HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class HomeView(TemplateView):

    template_name = 'common/home.html'

    def get(self, request, *args, **kwargs):
       if request.user.is_authenticated:
           return redirect('dashboard')
       context = self.get_context_data()
       return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print(self.request.user.id)
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},

        ]
        return context

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'common/register.html'

def pageNotFound(response, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')

