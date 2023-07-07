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
        fields = ["id", "name"]


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = ["pk", "name"]


class CompanySerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    # user = serializers.StringRelatedField()
    # user = serializers.SlugRelatedField(read_only=True, slug_field="email")
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username", default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # ownership_type = OwnershipTypeSerializer(read_only=True)
    # business_type = BusinessTypeSerializer(read_only=True)

    class Meta:
        model = Company
        exclude = ["slug"]
        # depth = 1  # Specifying nested serialization