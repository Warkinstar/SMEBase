from django.urls import path
from . import views


urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("new/", views.ProductCreateView.as_view(), name="product_new"),
]