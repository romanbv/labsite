from django import forms
from django.forms import ClearableFileInput

from .models import *

class addOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = "Не выбрана"
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),

        }

class OrderFileModelForm(forms.ModelForm):
    class Meta:
        model = OrderFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
            }
            # widget is important to upload multiple files
    #number = forms.CharField(max_length=9, label='Номер')
    #company = forms.ModelChoiceField(queryset=Company.objects.all(),  label='Компания')


