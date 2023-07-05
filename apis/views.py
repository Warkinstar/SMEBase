from rest_framework import generics
from enterprises.models import Company
from .serializers import CompanySerializer

class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetailAPIView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    lookup_field = "slug"
    serializer_class = CompanySerializer
