from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
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

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.prefetch_related('ordered_product__order')

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


#START ORDER#

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'crm/order-add.html'
    success_url = reverse_lazy('crm:orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_formset'] = OrderedProductFormSet()
        if self.request.POST:
            context['product_formset'] = OrderedProductFormSet(self.request.POST)
        else:
            context['product_formset'] = OrderedProductFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        product_formset = context['product_formset']
        if product_formset.is_valid():
            self.object = form.save()
            product_formset.instance = self.object
            product_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)



class updateOrder(LoginRequiredMixin, UpdateView):
    model = Order
    # fields = "__all__"

    form_class = OrderForm
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

        if self.request.POST:
            context['ordered_products'] = OrderedProductFormSet(self.request.POST, instance=self.object)
        else:
            context['ordered_products'] = OrderedProductFormSet(instance=self.object)
        return context

        return context
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        ordered_products = context['ordered_products']
        with transaction.atomic():
            form.instance.updated_by = self.request.user
            self.object = form.save()
            if ordered_products.is_valid():
                ordered_products.instance = self.object
                ordered_products.save()
        return redirect('crm:orders')

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if 'delete_ordered_product' in request.POST:
            ordered_product_id = request.POST['delete_ordered_product']
            ordered_product = OrderedProduct.objects.get(id=ordered_product_id)
            ordered_product.delete()
            return redirect('crm:order_update', pk=order.pk)
        return super().post(request, *args, **kwargs)

#END ORDER#


#START COMPANY#
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
        pricelists = Pricelist.objects.filter(company=company.id)
        context['orders'] = orders
        context['pricelists'] = pricelists
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компания', 'url': ""},
            {'title': company.pk, 'url': ""},
        ]
        c_def = self.get_user_context()
        #c_def = self.get_user_context(title=context['title'])
        return dict(list(context.items()) + list(c_def.items()))

class addCompany(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
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

    form_class = CompanyForm
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

#END COMPANY VIEWS#


#START PRODUCT VIEW#
class showProduct(LoginRequiredMixin, DataMixin, DetailView):
    login_url = '/login'
    model = Company
    template_name = 'crm/product.html'
    #slug_url_kwarg = 'order_num'
    context_object_name = 'product'
    allow_empty = False
    def get_object(self, queryset=None):
        num = self.kwargs['product_id']

        try:
            a_obj = Product.objects.get(pk=num)
        except Company.DoesNotExist:
            a_obj = None
        return a_obj
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()


        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Изделие', 'url': ""},
            {'title': product.pk, 'url': ""},
        ]
        c_def = self.get_user_context()
        #c_def = self.get_user_context(title=context['title'])
        return dict(list(context.items()) + list(c_def.items()))

class addProduct(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'crm/product-change.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Изделие', 'url': ""},

        ]

        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class updateProduct(LoginRequiredMixin, UpdateView):
    model = Product
    # fields = "__all__"

    form_class = ProductForm
    template_name = 'crm/product-change.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Изделие', 'url': ""},
            {'title': product.pk, 'url': ""},
        ]

        return context
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

#END PRODUCT VIEW#




#START PRICELIST VIEW#
class priceListView(LoginRequiredMixin, DataMixin, DetailView):
    login_url = '/login'
    model = Pricelist
    template_name = 'crm/pricelist.html'
    context_object_name = 'pricelist'

    def get_object(self, queryset=None):
        num = self.kwargs['pricelist_id']

        try:
            a_obj = Pricelist.objects.get(pk=num)
        except Company.DoesNotExist:
            a_obj = None
        return a_obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pricelist = self.get_object()
        products = Product.objects.filter(pricelist=pricelist.id)
        context['products'] = products
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Прайс', 'url': ""},
            {'title':   pricelist.pk, 'url':""},

        ]

        return context

class addPricelist(LoginRequiredMixin, CreateView):
    form_class = PricelistForm
    template_name = 'crm/pricelist-change.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Прайс', 'url': ""},

        ]

        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class updatePricelist(LoginRequiredMixin, UpdateView):
    model = Pricelist
    # fields = "__all__"

    form_class = PricelistForm
    template_name = 'crm/pricelist-change.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        price = self.get_object()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Прайс', 'url': ""},
            {'title': price.pk, 'url': ""},
        ]

        return context
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

#END PRICELIST VIEW#