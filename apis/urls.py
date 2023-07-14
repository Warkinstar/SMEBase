from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("users", views.UserAPIViewSet, basename="user")

app_name = "apis"

urlpatterns = [
    path("enterprises/", views.CompanyListAPIView.as_view(), name="company_list"),
    path("enterprises/<slug>/", views.CompanyDetailAPIView.as_view(), name="company_detail"),
    # path("users/", views.UserListAPIView.as_view(), name="user_list"),
    # path("users/<pk>/", views.UserDetailAPIView.as_view(), name="user_detail"),
]

urlpatterns += router.urls