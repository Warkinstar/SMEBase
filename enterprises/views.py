from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company, Employee, Financials
from .forms import CompanyForm, EmployeeForm, CompanyFilterForm, FinancialsForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from .filters import CompanyFilter


class CompanyOwnerTestMixin(UserPassesTestMixin):
    def test_func(self):
        self.company = get_object_or_404(Company, slug=self.kwargs["slug"])
        return self.company.user == self.request.user


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = "enterprises/company_new.html"
    form_class = CompanyForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("company_detail", kwargs={"slug": self.object.slug})


class CompanyListView(TemplateResponseMixin, View):
    model = Company
    template_name = "enterprises/company_list.html"

    # def company_list_filter(self, request, qs):
    #     """Если фильтр есть, то выполнить фильтрацию"""
    #     business_type = request.GET.get("business_type")
    #     ownership_type = request.GET.get("ownership_type")
    #     if business_type and ownership_type:
    #         return qs.filter(business_type=business_type, ownership_type=ownership_type)
    #     if business_type:
    #         return qs.filter(business_type=business_type)
    #     if ownership_type:
    #         return qs.filter(ownership_type=ownership_type)
    #
    #     else:
    #         return qs

    def get(self, request):
        # qs = Company.objects.all()
        # company_filter_form = CompanyFilterForm(data=request.GET)
        # company_list = self.company_list_filter(request, qs)

        # one string of django-filter, but many without
        f = CompanyFilter(request.GET, queryset=Company.objects.all())


        return self.render_to_response(
            {"company_list": "company_list", "company_filter_form": "company_filter_form", "filter": f}
        )


class CompanyDetailView(DetailView):
    model = Company
    template_name = "enterprises/company_detail.html"
    context_object_name = "company"


class CompanyUpdateView(LoginRequiredMixin, CompanyOwnerTestMixin, UpdateView):
    template_name = "enterprises/company_update.html"
    form_class = CompanyForm

    def get_object(self, queryset=None):
        """Получить объект если автор request.user"""
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Company, slug=slug, user=self.request.user)
        return obj

    def get_success_url(self):
        return reverse_lazy("company_detail", kwargs={"slug": self.object.slug})


class CompanyDeleteView(LoginRequiredMixin, CompanyOwnerTestMixin, DeleteView):
    model = Company
    success_url = reverse_lazy("company_list")
    context_object_name = "company"
    template_name = "enterprises/company_delete.html"



class EmployeeCreateView(LoginRequiredMixin, CompanyOwnerTestMixin, CreateView):
    """Add company employee"""

    template_name = "enterprises/employee_new.html"
    form_class = EmployeeForm

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


class EmployeeUpdateView(LoginRequiredMixin, CompanyOwnerTestMixin, UpdateView):
    form_class = EmployeeForm
    pk_url_kwarg = "pk"
    context_object_name = "employee"
    template_name = "enterprises/employee_update.html"

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            Employee, pk=self.kwargs["pk"], company__user=self.request.user
        )
        return obj

    def get_success_url(self):
        return reverse_lazy("company_detail", args=[self.object.company.slug])


@login_required()
def employee_delete(request, slug, pk):
    # if request.is_ajax(): # Этот метод устарел
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        company = get_object_or_404(Company, slug=slug, user=request.user)
        employee = get_object_or_404(Employee, pk=pk, company=company)
        # employee = Employee.objects.get(pk=pk)
        employee.delete()
        return JsonResponse({"status": "success"})


class FinancialsCreateView(LoginRequiredMixin, CompanyOwnerTestMixin, CreateView):
    model = Financials
    form_class = FinancialsForm
    template_name = "enterprises/financials_new.html"

    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def get_success_url(self):
        return self.company.get_absolute_url()


class FinancialsUpdateView(LoginRequiredMixin, CompanyOwnerTestMixin, UpdateView):
    model = Financials
    form_class = FinancialsForm
    pk_url_kwarg = "pk"
    template_name = "enterprises/financials_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def get_success_url(self):
        return self.company.get_absolute_url()

class FinancialsDeleteView(LoginRequiredMixin, CompanyOwnerTestMixin, DeleteView):
    model = Financials
    pk_url_kwarg = "pk"
    template_name = "enterprises/financials_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def get_success_url(self):
        return self.company.get_absolute_url()

class CompanySearchView(ListView):
    model = Company
    template_name = "enterprises/company_search.html"

    def get_context_data(self, **kwargs):
        q = self.request.GET.get("q")
        context = super().get_context_data(**kwargs)
        print(q)
        if q:
            context["company_search_results"] = Company.objects.filter(
                Q(name__icontains=q)
                | Q(description__icontains=q)
                | Q(ownership_type__name__icontains=q)
                | Q(business_type__name__icontains=q)
            )
        return context
