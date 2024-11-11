from django.urls import path
from djoser.views import UserViewSet
from api.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(
        "login/",
        CustomTokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "jwt/refresh/",
        TokenRefreshView.as_view(),
        name="jwt-refresh",
    ),
    path(
        "jwt/verify/",
        TokenVerifyView.as_view(),
        name="jwt-verify",
    ),
    path(
        "register/",
        UserViewSet.as_view({"post": "create"}),
        name="register",
    ),
    path(
        "users/set_password/",
        UserViewSet.as_view({"post": "set_password"}),
        name="set-password",
    ),
    path(
        "users/reset_password/",
        UserViewSet.as_view({"post": "reset_password"}),
        name="reset-password",
    ),
    path(
        "users/reset_password_confirm/",
        UserViewSet.as_view({"post": "reset_password_confirm"}),
        name="reset-password-confirm",
    ),
]
