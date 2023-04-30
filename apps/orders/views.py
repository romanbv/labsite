from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .forms import *

from .utils import *

class OrdersView(DataMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user.id)


class ShowOrder(DataMixin, DetailView):
    model = Order
    template_name = 'orders/order.html'
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
        c_def = self.get_user_context()
        #c_def = self.get_user_context(title=context['title'])
        return dict(list(context.items()) + list(c_def.items()))


class OrderCreateView(CreateView):
    model = Order
    template_name = 'orders/add_order.html'
    fields = "__all__"
class AddOrder(LoginRequiredMixin, CreateView):
    form_class = addOrderForm
    model = Order
    template_name = 'orders/add_order.html'
    success_url = reverse_lazy('orders:add_order')
    login_url = reverse_lazy('home')
    raise_exception = True
    helper = None

    def form_valid(self, form):

        return super().form_valid(form)

    def __init__(self, *args, **kwargs):
        super(AddOrder, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-AddOrderForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'url_action_call'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn-primary'))

    def get_context_data(self, **kwargs):
        context = super(AddOrder, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context

def add_order(request):
    user = request.user
    if request.method == "POST":
        form = addOrderForm( request.POST)
        file_form = OrderFileModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        if form.is_valid() and file_form.is_valid():
            try:
                order_instance = form.save(commit=False)
                order_instance.user = user
                order_instance.save()
                for f in files:
                    file_instance = OrderFile(file=f, order=order_instance, owner = user)
                    file_instance.save()
                return redirect('userprofiles:profile', user_id=request.user.pk)
            except:
                form.add_error(None,'Ошибка создания заказа')
                file_form.add_error(None,'Ошибка загрузки файла')
    else:
        form = addOrderForm()
        file_form = OrderFileModelForm()

    return render(request, 'orders/add_order.html', {'form':form, 'title':'Добавление заказа', 'file_form':file_form})

def add_file(request):
    return render(request, 'userprofiles/profile.html')
