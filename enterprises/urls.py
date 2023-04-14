from django.urls import path
from . import views


urlpatterns = [
    path("new/", views.CompanyCreateView.as_view(), name="company_new"),
    path("", views.CompanyListView.as_view(), name="company_list"),
    path("<slug>/", views.CompanyDetailView.as_view(), name="company_detail"),
    path("<slug>/update/", views.CompanyUpdateView.as_view(), name="company_update"),
]