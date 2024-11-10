from rest_framework import serializers

from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'user', 'url', 'title', 'description', 'created_at']
        read_only_fields = ['user', 'created_at']
