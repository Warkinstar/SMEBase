from rest_framework import generics
from enterprises.models import Company
from .serializers import CompanySerializer

class CompanyAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
