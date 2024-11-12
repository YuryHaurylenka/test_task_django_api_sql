from djoser.views import UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from ..models import Collection, Link
from ..permissions import IsOwnerOrReadOnly
from ..serializers import (
    CollectionDetailSerializer,
    LinkCreateSerializer,
    LinkDetailSerializer,
)
from ..utils import fetch_og_data


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Obtain JWT token",
        operation_description="Obtain a pair of access and refresh tokens using email and password.",
        responses={
            200: openapi.Response(
                description="Token successfully obtained",
                examples={
                    "application/json": {
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    }
                },
            ),
            401: "Invalid credentials",
        },
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get("access")

            if access_token:
                request.session["access_token"] = access_token
        return response


class CustomUserViewSet(UserViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="User registration",
        operation_description="Register a new user with email and password.",
        responses={
            201: "User successfully registered",
            400: "Bad request - invalid data",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Password reset",
        operation_description="Request a password reset email.",
        responses={
            200: "Password reset email sent",
            400: "Bad request - invalid email",
        },
    )
    def reset_password(self, request, *args, **kwargs):
        return super().reset_password(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Set new password",
        operation_description="Set a new password for the authenticated user.",
        responses={
            204: "Password successfully updated",
            400: "Bad request - invalid data",
            401: "Authentication credentials were not provided",
        },
    )
    def set_password(self, request, *args, **kwargs):
        return super().set_password(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary="Refresh JWT token",
        operation_description="Refresh access token using a refresh token.",
        responses={
            200: openapi.Response(
                description="Token successfully refreshed",
                examples={
                    "application/json": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                },
            ),
            401: "Invalid refresh token",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        operation_summary="Verify JWT token",
        operation_description="Verify if the given token is valid.",
        responses={
            200: "Token is valid",
            401: "Invalid or expired token",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
