from allauth.account.forms import SignupForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class CustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label="Имя")
    last_name = forms.CharField(max_length=30, label="Фамилия")
    middle_name = forms.CharField(max_length=30, label="Отчество")
    phone_number = PhoneNumberField(
        region="KZ", label="Номер телефона", widget=PhoneNumberPrefixWidget(initial="KZ")
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.middle_name = self.cleaned_data["middle_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.save()
        return user

