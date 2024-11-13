import os

from django.contrib.auth import get_user_model
from django.db import connection
from djoser.views import UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.serializers import (
    CustomPasswordResetConfirmSerializer,
    CustomPasswordResetSerializer,
    CustomTokenObtainPairSerializer,
)
from api.utils import save_to_csv, send_password_reset_email

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="User Login",
        operation_description="Obtain a JWT token using email and password.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User email",
                    example="user@example.com",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User password",
                    example="password123",
                ),
            },
            required=["email", "password"],
        ),
        responses={
            200: "Token successfully obtained",
            404: "User not found",
            400: "Invalid credentials",
        },
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get("access")
            if access_token:
                request.session["access_token"] = access_token
                request.session.save()

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

    @action(
        detail=False,
        methods=["post"],
        url_path="reset_password",
    )
    @swagger_auto_schema(
        operation_summary="Password reset",
        operation_description="Request a password reset email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User email address",
                    example="user@example.com",
                ),
            },
            required=["email"],
        ),
        responses={
            204: "Password reset email sent",
            400: "Invalid email",
            404: "User not found",
        },
    )
    def reset_password(self, request):
        serializer = CustomPasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get("email")
        response = send_password_reset_email(email)
        return response

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


class CustomResetPasswordConfirmView(APIView):

    @swagger_auto_schema(
        operation_summary="Reset Password Confirm",
        operation_description="Enter the reset code and a new password.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "reset_code": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password reset code",
                    example="123e4567-e89b-12d3-a456-426614174000",
                ),
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="New password",
                    example="newpassword123",
                ),
            },
            required=["reset_code", "new_password"],
        ),
        responses={
            200: "Password has been reset successfully.",
            400: "Invalid or expired reset code.",
        },
    )
    def post(self, request):
        serializer = CustomPasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        operation_description="Retrieve top 10 users with the highest number of links, sorted by date of registration.",
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
                "object": row[7],
                "error": row[8],
            }
            for row in results
        ]

        output_file_path = os.path.join(base_dir, "top_users_output.csv")
        save_to_csv(users_data, output_file_path)

        return Response(users_data, status=status.HTTP_200_OK)
