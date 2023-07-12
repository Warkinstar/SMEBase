from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.core.exceptions import ValidationError as DjangoValidationError


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, label="Имя")
    last_name = serializers.CharField(max_length=30, label="Фамилия")
    middle_name = serializers.CharField(max_length=30, label="Отчество")
    phone_number = PhoneNumberField(region="KZ", label="Номер телефона")

    def get_cleaned_data(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "middle_name": self.validated_data.get("middle_name", ""),
            "phone_number": self.validated_data.get("phone_number", ""),
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def custom_signup(self, request, user):
        user.phone_number = self.validated_data.get("phone_number")
        user.middle_name = self.validated_data.get("middle_name")
        user.save()

    # native save function
"""
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
"""
