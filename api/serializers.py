from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

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
