from drf_yasg import openapi
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets

from ..models import Collection
from ..permissions import IsOwnerOrReadOnly
from ..serializers import (
    CollectionDetailSerializer,
)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List User's Collections",
        operation_description="Retrieve a list of collections owned by the authenticated user.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved list of collections.",
                schema=CollectionDetailSerializer(many=True),
            ),
            401: "Authentication credentials were not provided.",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a New Collection",
        operation_description="Create a new collection associated with the authenticated user.",
        request_body=CollectionDetailSerializer,
        responses={
            201: openapi.Response(
                description="Collection created successfully.",
                schema=CollectionDetailSerializer,
            ),
            400: "Bad request - validation errors.",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a Collection",
        operation_description="Update the entire collection by its ID. Requires ownership of the collection.",
        request_body=CollectionDetailSerializer,
        responses={
            200: openapi.Response(
                description="Collection updated successfully.",
                schema=CollectionDetailSerializer,
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
        request_body=CollectionDetailSerializer,
        responses={
            200: openapi.Response(
                description="Collection partially updated successfully.",
                schema=CollectionDetailSerializer,
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
                schema=CollectionDetailSerializer,
            ),
            404: "Collection not found.",
            403: "Forbidden - You do not have permission to access this collection.",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
