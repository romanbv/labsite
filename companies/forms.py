from django import forms

from .models import *

class addCompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['company'].empty_label = "Не выбрана"
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

        }