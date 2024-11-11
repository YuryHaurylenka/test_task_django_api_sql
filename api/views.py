from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions, viewsets

from .models import Link
from .serializers import LinkSerializer
from .utils import fetch_og_data


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["user"]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        url = self.request.data.get("url")
        og_data = fetch_og_data(url)

        if og_data:
            serializer.save(
                user=self.request.user,
                url=url,
                title=og_data.get("title"),
                description=og_data.get("description"),
                image=og_data.get("image"),
                type=og_data.get("type"),
            )
        else:
            serializer.save(user=self.request.user)
