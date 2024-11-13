from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, CollectionViewSet, CustomTopUsersViewSet

router = DefaultRouter()
router.register("links", LinkViewSet, basename="link")
router.register("collections", CollectionViewSet, basename="collection")
router.register("users", CustomTopUsersViewSet, basename="top-users")

urlpatterns = [
    path("", include(router.urls)),
]
