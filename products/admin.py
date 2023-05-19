from django.contrib import admin
from .models import *


admin.site.register(ProductCategory)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "product_category"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "company"]
    list_filter = ["price"]
