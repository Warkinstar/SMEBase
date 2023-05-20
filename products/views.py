from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from .models import Product, ProductType, ProductCategory
from enterprises.models import Company
from .filters import ProductFilter
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .forms import ProductForm


class ProductListView(ListView):
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        f = ProductFilter(self.request.GET, queryset=Product.objects.all())
        return f


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_new.html"

    def get_form_kwargs(self):
        """Передает ключевые аргументы в форму для построения"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def test_func(self):
        """Проверяет что у пользователя есть созданная компания(и)"""
        if self.request.user.companies.exists():
            return True
