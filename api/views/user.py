import os

from django.db import connection
from djoser.views import UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.utils import save_to_csv


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


class CustomTopUsersViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        methods=["get"],
        url_path="top-users",
    )
    @swagger_auto_schema(
        operation_summary="Top 10 Users",
        operation_description="Retrieve top 10 users with the highest number of saved links, sorted by date of registration.",
        responses={
            200: openapi.Response(
                description="Top 10 users retrieved successfully",
                examples={
                    "application/json": [
                        {
                            "email": "user1@example.com",
                            "count_links": 99,
                            "date_joined": "2024-01-12T10:30:45",
                        },
                        {
                            "email": "user2@example.com",
                            "count_links": 95,
                            "date_joined": "2024-02-03T14:22:10",
                        },
                    ]
                },
            ),
            404: "SQL file not found",
        },
    )
    def top_users(self, request):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        sql_file_path = os.path.join(base_dir, "top_users.sql")

        if not os.path.exists(sql_file_path):
            return Response(
                {"error": "SQL file not found"}, status=status.HTTP_404_NOT_FOUND
            )

        with open(sql_file_path, "r") as file:
            query = file.read()

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        users_data = [
            {
                "email": row[0],
                "count_links": row[1],
                "website": row[2],
                "book": row[3],
                "article": row[4],
                "music": row[5],
                "video": row[6],
                "company": row[7],
                "object": row[8],
                "error": row[9],
            }
            for row in results
        ]

        output_file_path = os.path.join(base_dir, "top_users_output.csv")
        save_to_csv(users_data, output_file_path)

        return Response(users_data, status=status.HTTP_200_OK)
