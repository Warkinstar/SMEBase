from django.urls import path
from . import views

app_name = "apis"

urlpatterns = [
    path("enterprises/", views.CompanyListAPIView.as_view(), name="company_list"),
    path("enterprises/<slug>/", views.CompanyDetailAPIView.as_view(), name="company_detail"),
]