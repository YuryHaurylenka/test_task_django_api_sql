from rest_framework import serializers

from .models import Collection, Link


class LinkSerializer(serializers.ModelSerializer):
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


class CollectionSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)
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
