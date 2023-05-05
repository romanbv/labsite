from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy


from crispy_forms.layout import Submit
from .forms import *

from .utils import *

class ordersView(LoginRequiredMixin, DataMixin, ListView):
    login_url = '/login'
    model = Order
    template_name = 'crm/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Заказы', 'url': reverse_lazy('crm:orders')},

        ]

        return context

class showOrder(LoginRequiredMixin, DataMixin, DetailView):
    login_url = '/login'
    model = Order
    template_name = 'crm/order.html'
    slug_url_kwarg = 'order_num'
    context_object_name = 'order'
    allow_empty = False
    def get_object(self, queryset=None):
        slug = self.kwargs['order_num']
        a_obj = Order.objects.get(number=slug)
        try:
            d_obj = Order.objects.get(number=a_obj)
        except Order.DoesNotExist:
            d_obj = None
        return d_obj
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Заказы', 'url': reverse_lazy('crm:orders')},
            {'title': order.pk, 'url': ""},
        ]
        c_def = self.get_user_context()
        #c_def = self.get_user_context(title=context['title'])
        return dict(list(context.items()) + list(c_def.items()))



class addOrder(LoginRequiredMixin, CreateView):

    form_class = addOrderForm
    template_name = 'crm/order-add.html'
    #success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Заказы', 'url': reverse_lazy('crm:orders')},

        ]

        return context
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class updateOrder(LoginRequiredMixin, UpdateView):
    model = Order
    # fields = "__all__"

    form_class = updateOrderForm
    template_name = 'crm/order-update.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Заказы', 'url': reverse_lazy('crm:orders')},
            {'title': order.pk, 'url': ""},
        ]

        return context
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #
    #     context_data = super(AddOrder, self).get_context_data(**kwargs)
    #
    #     context_data.update({
    #         'file_form': self.file_form_class,
    #     })
    #
    #     return context_data

    # def post(self, request):
    #     super(AddOrder, self).post(request)
    #     post_data = request.POST or None
    #     file_data = request.FILES or None
    #
    #     form = addOrderForm(post_data)
    #     file_form = OrderFileForm(post_data, file_data)
    #     user = request.user
    #     if form.is_valid() and file_form.is_valid():
    #         try:
    #             order_instance = form.save(commit=False)
    #             order_instance.user = user
    #             order_instance.save()
    #             for f in file_data:
    #                 file_instance = OrderFile(file=f, order=order_instance, owner=user)
    #                 file_instance.save()
    #
    #             return redirect('userprofiles:profile', user_id=request.user.pk)
    #         except:
    #
    #             form.add_error(None, 'Ошибка создания заказа')
    #             file_form.add_error(None, 'Ошибка загрузки файла')
    #
    #     context = self.get_context_data(
    #                                     form=form,
    #                                     file_form=file_form
    #                                 )
    #
    #     return self.render_to_response(context)

class showCompany(LoginRequiredMixin, DataMixin, DetailView):
    login_url = '/login'
    model = Company
    template_name = 'crm/company.html'
    #slug_url_kwarg = 'order_num'
    context_object_name = 'company'
    allow_empty = False
    def get_object(self, queryset=None):
        num = self.kwargs['company_id']

        try:
            a_obj = Company.objects.get(pk=num)
        except Company.DoesNotExist:
            a_obj = None
        return a_obj
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        orders = Order.objects.filter(company=company.id)[:5]
        context['orders'] = orders
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компания', 'url': ""},
            {'title': company.pk, 'url': ""},
        ]
        c_def = self.get_user_context()
        #c_def = self.get_user_context(title=context['title'])
        return dict(list(context.items()) + list(c_def.items()))

class addCompany(LoginRequiredMixin, CreateView):
    form_class = addCompanyForm
    template_name = 'crm/company-add.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компания', 'url': ""},

        ]

        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class updateCompany(LoginRequiredMixin, UpdateView):
    model = Company
    # fields = "__all__"

    form_class = updateCompanyForm
    template_name = 'crm/company-update.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        company = self.get_object()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компания', 'url': ""},
            {'title': company.pk, 'url': ""},
        ]

        return context
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



class priceListView(LoginRequiredMixin, DataMixin, DetailView):
    login_url = '/login'
    model = Pricelist
    template_name = 'crm/pricelist.html'
    context_object_name = 'pricelist'

    def get_queryset(self):
        return Pricelist.objects.filter(company = self.request.company, number = self.request.number)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Прайс', 'url': reverse_lazy('crm:pricelist')},

        ]

        return context