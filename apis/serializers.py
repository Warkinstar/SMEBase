from rest_framework import serializers
from enterprises.models import Company, OwnershipType, BusinessType
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email", "phone_number"]

class OwnershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnershipType
        fields = ["name"]


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = ["name"]


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    ownership_type = OwnershipTypeSerializer()
    business_type = BusinessTypeSerializer()

    class Meta:
        model = Company
        fields = "__all__"