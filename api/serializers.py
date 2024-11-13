from django.contrib.auth import get_user_model
from djoser.serializers import (
    PasswordResetConfirmSerializer,
    SendEmailResetSerializer,
    UserCreateSerializer,
)
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Collection, Link

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


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        token = attrs.get("token")
        new_password = attrs.get("new_password")

        user = User.objects.filter(email=email).first()
        if not user:
            raise NotFound("User with this email does not exist.")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user
