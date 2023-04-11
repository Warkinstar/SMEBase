from .models import Company
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ["slug", "user"]
        widgets = {"phone_number": PhoneNumberPrefixWidget(initial="KZ"),
                   "description": forms.Textarea(attrs={'rows': 3, 'style': 'height: 50px;'})
                   }
