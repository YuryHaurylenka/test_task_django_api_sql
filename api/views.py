from djoser.views import UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework import status
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

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List User's Links",
        operation_description="Retrieve a list of links owned by the authenticated user.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved list of links.",
                schema=LinkSerializer(many=True),
            ),
            401: "Authentication credentials were not provided.",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a New Link",
        operation_description="Create a new link associated with the authenticated user. Only users with valid authentication tokens can access this endpoint.",
        request_body=LinkSerializer,
        responses={
            201: openapi.Response(
                description="Link created successfully.", schema=LinkSerializer
            ),
            400: "Bad request - validation errors.",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a Link",
        operation_description="Get detailed information about a specific link using its unique ID. Access is restricted to the owner of the link.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved link details.",
                schema=LinkSerializer,
            ),
            404: "Link not found.",
            403: "Forbidden - You do not have permission to access this link.",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a Link",
        operation_description="Update the attributes of an existing link using its ID. Only the owner of the link can perform this action.",
        request_body=LinkSerializer,
        responses={
            200: openapi.Response(
                description="Link updated successfully.", schema=LinkSerializer
            ),
            400: "Bad request - validation errors.",
            404: "Link not found.",
            403: "Forbidden - You do not have permission to update this link.",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially Update a Link",
        operation_description="Partially update attributes of an existing link using its ID. Only the owner of the link can perform this action.",
        request_body=LinkSerializer,
        responses={
            200: openapi.Response(
                description="Link partially updated successfully.",
                schema=LinkSerializer,
            ),
            400: "Bad request - validation errors.",
            404: "Link not found.",
            403: "Forbidden - You do not have permission to update this link.",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a Link",
        operation_description="Delete a link using its unique ID. Only the owner of the link can delete it.",
        responses={
            204: "Link deleted successfully.",
            404: "Link not found.",
            403: "Forbidden - You do not have permission to delete this link.",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List User's Collections",
        operation_description="Retrieve a list of collections owned by the authenticated user.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved list of collections.",
                schema=CollectionSerializer(many=True),
            ),
            401: "Authentication credentials were not provided.",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a New Collection",
        operation_description="Create a new collection associated with the authenticated user.",
        request_body=CollectionSerializer,
        responses={
            201: openapi.Response(
                description="Collection created successfully.",
                schema=CollectionSerializer,
            ),
            400: "Bad request - validation errors.",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a Collection",
        operation_description="Update the entire collection by its ID. Requires ownership of the collection.",
        request_body=CollectionSerializer,
        responses={
            200: openapi.Response(
                description="Collection updated successfully.",
                schema=CollectionSerializer,
            ),
            400: "Bad request - validation errors.",
            403: "Forbidden - You do not have permission to update this collection.",
            404: "Collection not found.",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially Update a Collection",
        operation_description="Partially update the attributes of a collection using its ID. Requires ownership of the collection.",
        request_body=CollectionSerializer,
        responses={
            200: openapi.Response(
                description="Collection partially updated successfully.",
                schema=CollectionSerializer,
            ),
            400: "Bad request - validation errors.",
            403: "Forbidden - You do not have permission to update this collection.",
            404: "Collection not found.",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a Collection",
        operation_description="Delete a collection using its unique ID. Only the owner of the collection can delete it.",
        responses={
            204: "Collection deleted successfully.",
            403: "Forbidden - You do not have permission to delete this collection.",
            404: "Collection not found.",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a Collection",
        operation_description="Get details of a specific collection using its unique ID.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved collection details.",
                schema=CollectionSerializer,
            ),
            404: "Collection not found.",
            403: "Forbidden - You do not have permission to access this collection.",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


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
