from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product, ProductType, ProductCategory


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
