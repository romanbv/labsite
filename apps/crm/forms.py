from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.forms import ClearableFileInput
from django.forms.models import inlineformset_factory

from .models import *

class OrderForm(forms.ModelForm):
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
    #file_field = forms.FileField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = "Не выбрана"
        #self.fields['file_field'].label = "Файл заказа"
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    # def save(self, commit = True):
    #     order = super().save(commit=commit)
    #     file = self.cleaned_data.get('file_field')
    #     if file:
    #         order_file = OrderFile(order=order, owner_id = order.user.pk, file = file)
    #         order_file.save()
    #
    #
    #     # OrderFile.objects.create(
    #     #             order=order,
    #     #             owner_id = order.user.pk,
    #     #             file=self.cleaned_data.get('file_field')
    #     #            )
    #     return order


class OrderedProductForm(forms.ModelForm):
    class Meta:
        model = OrderedProduct
        fields = "__all__"

    widgets = {
        'product': forms.Select(attrs={'class': 'form-control'}),
        'amount': forms.NumberInput(attrs={'class': 'form-control'}),
    }

class OrderFileForm(forms.ModelForm):
    class Meta:
        model = OrderFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
            }
            # widget is important to upload multiple files
    #number = forms.CharField(max_length=9, label='Номер')
    #company = forms.ModelChoiceField(queryset=Company.objects.all(),  label='Компания')

OrderedProductFormSet = inlineformset_factory(
    Order,
    OrderedProduct,
    form=OrderedProductForm,
    extra=0
)

OrderFileFormSet = inlineformset_factory(
    Order,
    OrderFile,
    form=OrderFileForm,
    extra=0

)

class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['type'].empty_label = "Не выбрана"
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

        }

class ProductGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['company'].empty_label = "Не выбрана"

    class Meta:
        model = ProductGroup
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['company'].empty_label = "Не выбрана"

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PricelistForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['company'].empty_label = "Не выбрана"

    class Meta:
        model = Pricelist
        fields = "__all__"
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
        }