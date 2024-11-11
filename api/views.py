from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Collection, Link
from .permissions import IsOwnerOrReadOnly
from .serializers import CollectionSerializer, LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["type"]
    search_fields = ["title", "description"]

    @swagger_auto_schema(
        operation_summary="Get a list of links",
        operation_description="Retrieve all links created by the authenticated user.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new link",
        operation_description="Create a new link for the authenticated user.",
        responses={201: LinkSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a link",
        operation_description="Get details of a specific link by its ID.",
        responses={200: LinkSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a link",
        operation_description="Update the link details for the authenticated user.",
        responses={200: LinkSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a link",
        operation_description="Partially update the link details for the authenticated user.",
        responses={200: LinkSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a link",
        operation_description="Delete a link created by the authenticated user.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Get a list of collections",
        operation_description="Retrieve all collections created by the authenticated user.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new collection",
        operation_description="Create a new collection for the authenticated user.",
        responses={201: CollectionSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a collection",
        operation_description="Get details of a specific collection by its ID.",
        responses={200: CollectionSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a collection",
        operation_description="Update the collection details for the authenticated user.",
        responses={200: CollectionSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a collection",
        operation_description="Partially update the collection details for the authenticated user.",
        responses={200: CollectionSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a collection",
        operation_description="Delete a collection created by the authenticated user.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary="Obtain JWT token",
        operation_description="Obtain a pair of access and refresh tokens using email and password.",
        responses={
            200: openapi.Response(
                description="Token successfully obtained",
                examples={
                    "application/json": {
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR...",
                        "access": "eyJhbGciOiJIUzI1NiIsInR...",
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
