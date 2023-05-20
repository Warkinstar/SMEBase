from django import forms
from .models import *
from enterprises.models import Company


class ProductForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=None, label="Компания")

    class Meta:
        model = Product
        fields = ["company", "type", "name", "price", "description", "image"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["company"].queryset = user.companies.all()


