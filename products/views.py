from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product, ProductType, ProductCategory
from .filters import ProductFilter


class ProductListView(ListView):
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        f = ProductFilter(self.request.GET, queryset=Product.objects.all())
        return f
