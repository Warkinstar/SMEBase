from rest_framework import generics
from enterprises.models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrReadOnly


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
