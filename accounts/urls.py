from django.urls import path, include


urlpatterns = [
    # all path of django-allauth
    path("", include("allauth.urls")),
]