from djoser.views import UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions
from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .models import Collection, Link
from .permissions import IsOwnerOrReadOnly
from .serializers import CollectionSerializer, LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Get a list of links",
        operation_description="Retrieve all links created by the authenticated user.",
        responses={
            200: LinkSerializer(many=True),
            401: "Authentication credentials were not provided.",
        },
    )
    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided."
            )
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new link",
        operation_description="Create a new link for the authenticated user.",
        responses={
            201: LinkSerializer,
            401: "Authentication credentials were not provided.",
        },
    )
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided."
            )
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a link",
        operation_description="Get details of a specific link by its ID.",
        responses={
            200: LinkSerializer,
            401: "Authentication credentials were not provided.",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided."
            )
        return super().retrieve(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Get a list of collections",
        operation_description="Retrieve all collections created by the authenticated user.",
        responses={
            200: CollectionSerializer(many=True),
            401: "Authentication credentials were not provided.",
        },
    )
    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided."
            )
        return super().list(request, *args, **kwargs)


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
        return super().post(request, *args, **kwargs)


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
