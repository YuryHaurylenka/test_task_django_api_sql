from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions, viewsets

from .models import Link
from .serializers import LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["user"]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
