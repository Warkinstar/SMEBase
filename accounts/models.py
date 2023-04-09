from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True, verbose_name="отчество")
    phone_number = PhoneNumberField("номер телефона", region="KZ", null=True)
