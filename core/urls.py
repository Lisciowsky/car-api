from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/", include("api.urls")),
]
