from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company
from .forms import CompanyForm
from django.urls import reverse_lazy


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = "enterprises/company_new.html"
    form_class = CompanyForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("company_detail", kwargs={"slug": self.object.slug})


class CompanyListView(ListView):
    model = Company
    template_name = "enterprises/company_list.html"
    context_object_name = "company_list"


class CompanyDetailView(DetailView):
    model = Company
    template_name = "enterprises/company_detail.html"
    context_object_name = "company"


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "enterprises/company_update.html"
    form_class = CompanyForm

    def get_object(self, queryset=None):
        """Получить объект если автор request.user"""
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Company, slug=slug, user=self.request.user)
        return obj

    def get_success_url(self):
        return reverse_lazy("company_detail", kwargs={"slug": self.object.slug})
