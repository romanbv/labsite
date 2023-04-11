from django import forms

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


    #number = forms.CharField(max_length=9, label='Номер')
    #company = forms.ModelChoiceField(queryset=Company.objects.all(),  label='Компания')


