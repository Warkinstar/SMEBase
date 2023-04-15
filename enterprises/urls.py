from django.urls import path
from . import views


urlpatterns = [
    path("", views.CompanyListView.as_view(), name="company_list"),

    path("new/", views.CompanyCreateView.as_view(), name="company_new"),
    path("<slug>/", views.CompanyDetailView.as_view(), name="company_detail"),
    path("<slug>/update/", views.CompanyUpdateView.as_view(), name="company_update"),
    path("<slug>/employees/new/", views.EmployeeCreateView.as_view(), name="employee_new"),
]