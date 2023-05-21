import django_filters
from .models import Product, ProductCategory, ProductType


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Поиск по имени")
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    type__product_category = django_filters.ModelChoiceFilter(queryset=ProductCategory.objects.all(), label="Категория")


    class Meta:
        model = Product
        fields = ["name", "type__product_category", "type", "company", "price", "price__gt", "price__lt"]
