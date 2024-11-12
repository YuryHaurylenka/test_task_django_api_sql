from django.db import models
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..models import Link
from ..permissions import IsOwnerOrReadOnly
from ..serializers import (
    LinkCreateSerializer,
    LinkDetailSerializer,
)
from ..utils import extract_uri, fetch_og_data


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List User's Links",
        operation_description="Retrieve a list of links owned by the authenticated user.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved list of links.",
                schema=LinkDetailSerializer(many=True),
            ),
            401: "Authentication credentials were not provided.",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a New Link",
        operation_description="Create a new link using only the URL. Other fields will be populated automatically.",
        request_body=LinkCreateSerializer,
        responses={
            201: openapi.Response(
                "Link created successfully.", schema=LinkDetailSerializer
            ),
            400: "Bad request - validation errors.",
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]

        if Link.objects.filter(user=self.request.user, url=url).exists():
            raise ValidationError({"detail": "You have already added this link."})

        og_data = fetch_og_data(url)

        if og_data:
            link = serializer.save(
                user=self.request.user,
                title=og_data.get("title", ""),
                description=og_data.get("description", ""),
                image=og_data.get("image", ""),
                type=og_data.get("type", "website"),
            )
        else:
            link = serializer.save(user=self.request.user)

        detail_serializer = LinkDetailSerializer(link)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve a Link",
        operation_description="Get information about a specific link. Access is restricted to the owner of the link.",
        responses={
            200: openapi.Response(
                description="Successfully retrieved link details.",
                schema=LinkDetailSerializer,
            ),
            404: "Link not found.",
            403: "Forbidden - You do not have permission to access this link.",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        url_path="search",
        permission_classes=[permissions.IsAuthenticated],
    )
    @swagger_auto_schema(
        operation_summary="Search Links by URL",
        operation_description="Search for links owned by the authenticated user using match on 'url'.",
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search by match on URL (URI part only)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully found links",
                schema=LinkDetailSerializer(many=True),
            ),
            400: "Bad request - validation errors.",
        },
    )
    def search(self, request, *args, **kwargs):
        search_query = request.query_params.get("search", "").strip().lower()

        if not search_query:
            return Response(
                {"detail": "Search parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cleaned_search_query = extract_uri(search_query)

        links = Link.objects.filter(user=request.user).filter(
            models.Q(title__iexact=search_query)
            | models.Q(url__icontains=cleaned_search_query)
        )

        if not links.exists():
            return Response(
                {"detail": "No links found matching the search criteria."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(links, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a Link",
        operation_description="Update the attributes of an existing link using its ID. Only the owner of the link can perform this action.",
        request_body=LinkDetailSerializer,
        responses={
            200: openapi.Response(
                description="Link updated successfully.", schema=LinkDetailSerializer
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
        request_body=LinkDetailSerializer,
        responses={
            200: openapi.Response(
                description="Link partially updated successfully.",
                schema=LinkDetailSerializer,
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
