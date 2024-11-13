from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CollectionViewSet, CustomTopUsersViewSet, LinkViewSet

router = DefaultRouter()
router.register("links", LinkViewSet, basename="link")
router.register("collections", CollectionViewSet, basename="collection")
router.register("users", CustomTopUsersViewSet, basename="top-users")

urlpatterns = [
    path("", include(router.urls)),
]
