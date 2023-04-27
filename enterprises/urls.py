from django.urls import path
from . import views


urlpatterns = [
    path("", views.CompanyListView.as_view(), name="company_list"),

    path("new/", views.CompanyCreateView.as_view(), name="company_new"),
    path("<slug>/", views.CompanyDetailView.as_view(), name="company_detail"),
    path("<slug>/update/", views.CompanyUpdateView.as_view(), name="company_update"),
    path("<slug>/delete/", views.CompanyDeleteView.as_view(), name="company_delete"),

    path("<slug>/employees/new/", views.EmployeeCreateView.as_view(), name="employee_new"),
    path("<slug>/employees/<pk>/update/", views.EmployeeUpdateView.as_view(), name="employee_update"),
    path("<slug>/employees/<pk>/delete/", views.employee_delete, name="employee_delete"),

    path("<slug>/financials/new/", views.FinancialsCreateView.as_view(), name="financials_new"),
    path("<slug>/financials/<pk>/update/", views.FinancialsUpdateView.as_view(), name="financials_update"),
    path("<slug>/financials/<pk>/delete/", views.FinancialsDeleteView.as_view(), name="financials_delete"),

    path("company/search/", views.CompanySearchView.as_view(), name="company_search"),
]