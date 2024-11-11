from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    CustomUserViewSet,
)

urlpatterns = [
    path(
        "login/",
        CustomTokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "jwt/refresh/",
        CustomTokenRefreshView.as_view(),
        name="jwt-refresh",
    ),
    path(
        "jwt/verify/",
        CustomTokenVerifyView.as_view(),
        name="jwt-verify",
    ),
    path(
        "register/",
        CustomUserViewSet.as_view({"post": "create"}),
        name="register",
    ),
    path(
        "register/",
        CustomUserViewSet.as_view({"post": "create"}),
        name="register",
    ),
    path(
        "users/reset_password/",
        CustomUserViewSet.as_view({"post": "reset_password"}),
        name="reset-password",
    ),
    path(
        "users/set_password/",
        CustomUserViewSet.as_view({"post": "set_password"}),
        name="set-password",
    ),
]
