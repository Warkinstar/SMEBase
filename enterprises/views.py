from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company
from .forms import CompanyForm


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = "enterprises/company_new.html"
    form_class = CompanyForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CompanyListView(ListView):
    model = Company
    template_name = "enterprises/company_list.html"
    context_object_name = "company_list"


class CompanyDetailView(DetailView):
    model = Company
    template_name = "enterprises/company_detail.html"
    context_object_name = "company"


