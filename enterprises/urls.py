from django.urls import path
from . import views


urlpatterns = [
    path("new/", views.CompanyCreateView.as_view(), name="company_new"),
    path("companies/", views.CompanyListView.as_view(), name="company_list"),
]