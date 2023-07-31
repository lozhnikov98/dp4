from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("accounts/", include("allauth.urls")),  # Оставили только allauth
    path("news/", include("newapp.urls")),
]