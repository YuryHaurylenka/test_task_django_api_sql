from datetime import timedelta, timezone

from django.contrib.auth import get_user_model
from djoser.serializers import (
    SendEmailResetSerializer,
    UserCreateSerializer,
)
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Collection, Link, PasswordResetCode

User = get_user_model()


class LinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["url"]


class LinkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "id",
            "url",
            "title",
            "description",
            "image",
            "type",
            "created_at",
            "updated_at",
        ]


class CollectionDetailSerializer(serializers.ModelSerializer):
    links = LinkDetailSerializer(many=True, read_only=True)
    link_ids = serializers.PrimaryKeyRelatedField(
        queryset=Link.objects.all(), write_only=True, many=True, source="links"
    )

    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
            "description",
            "links",
            "link_ids",
            "created_at",
            "updated_at",
        ]


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("email", "password")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(
        help_text="Enter your email address",
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()

        if user and not user.is_active:
            raise ValidationError("This user account is deactivated.", code=403)

        return super().validate(attrs)


class CustomPasswordResetSerializer(SendEmailResetSerializer):
    email = serializers.EmailField(
        help_text="Enter your email address",
    )

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise NotFound(detail="User with this email does not exist", code=404)

        return super().validate(attrs)


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    reset_code = serializers.UUIDField(help_text="Enter the reset code")
    new_password = serializers.CharField(
        write_only=True, min_length=8, help_text="Enter your new password"
    )

    def validate(self, attrs):
        reset_code = attrs.get("reset_code")
        new_password = attrs.get("new_password")

        try:
            reset_code = PasswordResetCode.objects.get(code=reset_code)
        except PasswordResetCode.DoesNotExist:
            raise ValidationError("Invalid reset code.")

        if not reset_code.is_valid():
            raise ValidationError("Reset code has expired.")

        attrs["user"] = reset_code.user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        PasswordResetCode.objects.filter(user=user).delete()
        return user
