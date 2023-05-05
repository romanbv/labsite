from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.forms import ClearableFileInput

from .models import *

class addOrderForm(forms.ModelForm):
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
    file_field = forms.FileField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = "Не выбрана"
        self.fields['file_field'].label = "Файл заказа"
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def save(self, commit = True):
        order = super().save(commit=commit)
        file = self.cleaned_data.get('file_field')
        if file:
            order_file = OrderFile(order=order, owner_id = order.user.pk, file = file)
            order_file.save()


        # OrderFile.objects.create(
        #             order=order,
        #             owner_id = order.user.pk,
        #             file=self.cleaned_data.get('file_field')
        #            )
        return order

class updateOrderForm(forms.ModelForm):
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
    file_field = forms.FileField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = "Не выбрана"
        self.fields['file_field'].label = "Файл заказа"
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
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

class addCompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['type'].empty_label = "Не выбрана"
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

        }

class updateCompanyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['company'].empty_label = "Не выбрана"

    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }