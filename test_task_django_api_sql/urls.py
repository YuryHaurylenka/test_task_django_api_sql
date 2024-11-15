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
        description="API documentation for the project. You can view the source code on [GitHub](https://github.com/YuryHaurylenka/test_task_django_api_sql).",
        terms_of_service="https://github.com/YuryHaurylenka/test_task_django_api_sql/blob/main/LICENSE",
        contact=openapi.Contact(
            email="gavrilenkoyury@gmail.com",
            url="https://t.me/yuraaaaaaaaaaaaaaaaaaaaaaa",
            name="Telegram"
        ),
        license=openapi.License(name="MIT License", url="https://opensource.org/licenses/MIT"),
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
