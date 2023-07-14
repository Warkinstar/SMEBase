from rest_framework import generics, viewsets
from enterprises.models import Company
from .serializers import CompanySerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model


class CompanyListAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthorOrReadOnly]


class CompanyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    lookup_field = "slug"
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthorOrReadOnly]


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
