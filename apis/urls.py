from django.urls import path
from .views import CompanyAPIView


urlpatterns = [
    path("enterprises/", CompanyAPIView.as_view(), name="company_list_api"),
]