from rest_framework import generics
from enterprises.models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated

class CompanyListAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]


class CompanyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    lookup_field = "slug"
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]
