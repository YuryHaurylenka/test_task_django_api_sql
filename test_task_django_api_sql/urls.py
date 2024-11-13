from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import HomeView

schema_view = get_schema_view(
    openapi.Info(
        title="Django API",
        default_version="v1",
        description="API documentation for the test project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="gavrilenkoyury@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("auth/", include("api.custom_auth_urls")),
    path("api/", include("api.urls")),
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"
    ),
]
