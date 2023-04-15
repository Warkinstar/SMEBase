from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company, Employee
from .forms import CompanyForm, EmployeeForm
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


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    """Add company employee"""

    template_name = "enterprises/employee_new.html"
    form_class = EmployeeForm

    def dispatch(self, request, *args, **kwargs):
        self.company = get_object_or_404(
            Company, slug=self.kwargs["slug"], user=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def form_valid(self, form):
        form.instance.company = self.company
        if "save_and_add_another" in self.request.POST:
            form.save()
            return redirect(reverse_lazy("employee_new", args=[self.company.slug]))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("company_detail", args=[self.company.slug])


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EmployeeForm
    pk_url_kwarg = "pk"
    context_object_name = "employee"
    template_name = "enterprises/employee_update.html"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Employee, pk=self.kwargs["pk"], company__user=self.request.user)
        return obj

    def get_success_url(self):
        return reverse_lazy("company_detail", args=[self.object.company.slug])