from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from crispy_forms.layout import Submit
from .forms import *

from .utils import *

#BEGIN ORDER#


class OrderInline():
    form_class = OrderForm
    model = Order
    template_name = "crm/order_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('crm:orders')

    def formset_ordered_products_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        products = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in products:
            variant.order = self.object
            variant.save()

    def formset_files_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        files = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for file in files:
            file.order = self.object
            file.owner = self.object.user
            file.save()

class OrderCreate(OrderInline, CreateView):

    def get_initial(self):
        initial = super().get_initial()
        company = Company.objects.get(id=1)  # Получение значения из модели
        initial['company'] = company
        return initial

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': 'Заказы', 'url': reverse_lazy('crm:orders')},

        ]
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'ordered_products': OrdersProductsFormSet(prefix='ordered_products'),
                'files': OrdersFilesFormSet(prefix='files'),
            }
        else:
            return {
                'ordered_products': OrdersProductsFormSet(self.request.POST or None, self.request.FILES or None, prefix='ordered_products'),
                'files': OrdersFilesFormSet(self.request.POST or None, self.request.FILES or None, prefix='files'),
            }

class OrderShow(LoginRequiredMixin, DataMixin, DetailView):
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

class OrderUpdate(OrderInline, UpdateView):

    def get_context_data(self, **kwargs):
        order = self.get_object()
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': "crm:companies"},
            {'title': 'Заказы', 'url': "crm:orders"},
            {'title': order.pk, 'url': ""},
        ]

        return context

    def get_named_formsets(self):
        return {
            'ordered_products': OrdersProductsFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                       prefix='ordered_products'),
            'files': OrdersFilesFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                   prefix='files'),
        }

class OrdersListView(LoginRequiredMixin, DataMixin, ListView):
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
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': 'Заказы', 'url': reverse_lazy('crm:orders')},

        ]

        return context

def add_inline_form(request, forms_count):
        context = {}
        formset = OrdersFilesFormSet(prefix='files')
        context["formset"] = formset
        context["forms_count"] =  forms_count
        return render(request, "crm/add-inline-form.html", context)

def delete_file(request, pk):

    try:
        file = OrderFile.objects.get(id=pk)
        order = file.order
    except OrderFile.DoesNotExist:
        messages.success(
            request, 'Файл не найден'
        )
        return redirect('crm:order_update', pk=order.id )

    file.delete()
    messages.success(
        request, 'Файл заказа успешно удален'
    )
    return redirect('crm:order_update', pk=order.id)

def delete_product(request, pk):
    try:
        product = OrderedProduct.objects.get(id=pk)
    except OrderedProduct.DoesNotExist:
        messages.success(
            request, 'Изделие в заказе не найдено'
        )
        return redirect('crm:order_update', pk=product.order.id)

    product.delete()
    messages.success(
        request, 'Изделие заказа успешно удалено'
    )
    return redirect('crm:order_update', pk=product.order.id)


#END ORDER#


#START COMPANY#
class CompanyCreate(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
    template_name = 'crm/company_create_or_update.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},

        ]

        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CompanyShow(LoginRequiredMixin, DataMixin, DetailView):
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
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': company.pk, 'url': ""},
        ]
        c_def = self.get_user_context()
        #c_def = self.get_user_context(title=context['title'])
        return dict(list(context.items()) + list(c_def.items()))

class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    # fields = "__all__"

    form_class = CompanyForm
    template_name = 'crm/company_create_or_update.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        company = self.get_object()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': company.pk, 'url': ""},
        ]

        return context
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CompaniesListView(LoginRequiredMixin, DataMixin, ListView):
    login_url = '/login'
    model = Pricelist
    template_name = 'crm/companies.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user.id)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.prefetch_related('ordered_product__order')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},

        ]

        return context


#END COMPANY VIEWS#


#START PRODUCT VIEW#
class ProductCreate(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'crm/product-create-or-update.html'
    # success_url = reverse_lazy('orders:order')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': 'Изделия', 'url': reverse_lazy('crm:products')},

        ]

        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ProductShow(LoginRequiredMixin, DataMixin, DetailView):
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
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': 'Изделия', 'url': reverse_lazy('crm:products')},
            {'title': product.pk, 'url': ""},
        ]
        c_def = self.get_user_context()
        #c_def = self.get_user_context(title=context['title'])
        return dict(list(context.items()) + list(c_def.items()))

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    # fields = "__all__"

    form_class = ProductForm
    template_name = 'crm/product-create-or-update.html'
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

class ProductsListView(LoginRequiredMixin, DataMixin, ListView):
    login_url = '/login'
    model = Product
    template_name = 'crm/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.prefetch_related('ordered_product__order')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': 'Изделия', 'url': reverse_lazy('crm:products')},
        ]

        return context

#END PRODUCT VIEW#




#START PRICELIST VIEW#

class PricelistInline():
    form_class = PricelistForm
    model = Pricelist
    template_name = "crm/pricelist_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('crm:pricelist', pricelist_id=self.object.pk )

    def formset_pricelists_products_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        products = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in products:
            variant.pricelist = self.object
            variant.save()

class PricelistCreate(PricelistInline, CreateView):

    def get_initial(self):
        initial = super().get_initial()
        company = Company.objects.get(id=1)  # Получение значения из модели
        initial['company'] = company
        return initial

    def get_context_data(self, **kwargs):
        context = super(PricelistCreate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': 'Прайслисты', 'url': reverse_lazy('crm:pricelists')},

        ]

        return context


    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'pricelists_products': PricelistsProductsFormSet(prefix='pricelists_products'),

            }
        else:
            return {
                'pricelists_products': PricelistsProductsFormSet(self.request.POST or None, self.request.FILES or None, prefix='pricelists_products'),

            }

class PricelistShow(LoginRequiredMixin, DataMixin, DetailView):
    login_url = '/login'
    model = Pricelist
    template_name = 'crm/pricelist.html'
    context_object_name = 'pricelist'

    def get_object(self, queryset=None):
        num = self.kwargs['pricelist_id']

        try:
            a_obj = Pricelist.objects.get(pk=num)
        except Pricelist.DoesNotExist:
            a_obj = None
        return a_obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pricelist = self.get_object()
        products = PricelistsProducts.objects.filter(pricelist=pricelist.id)
        context['products'] = products
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Прайслисты', 'url': reverse_lazy('crm:pricelists')},
            {'title':   pricelist.pk, 'url':""},

        ]

        return context

class PricelistUpdate(PricelistInline, UpdateView):

    def get_context_data(self, **kwargs):
        pricelist = self.get_object()
        context = super(PricelistUpdate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': 'Прайслисты', 'url': ""},
            {'title': pricelist.pk, 'url': ""},
        ]

        return context


    def get_named_formsets(self):
        return {
            'pricelists_products': PricelistsProductsFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                       prefix='pricelists_products'),

        }

class PricelistsListView(LoginRequiredMixin, DataMixin, ListView):
    login_url = '/login'
    model = Pricelist
    template_name = 'crm/pricelists.html'
    context_object_name = 'pricelists'

    def get_queryset(self):
        return Pricelist.objects.filter(company__owner=self.request.user.id)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'title': 'Главная', 'url': reverse_lazy('home')},
            {'title': 'Компании', 'url': reverse_lazy('crm:companies')},
            {'title': 'Прайслисты', 'url': reverse_lazy('crm:pricelists')},


        ]
        return context


#END PRICELIST VIEW#