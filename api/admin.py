from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Collection, CustomUser, Link
from .utils import fetch_og_data


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "user", "type", "created_at", "updated_at")
    search_fields = ("title", "url", "description")
    list_filter = ("user", "type", "created_at")
    readonly_fields = (
        "title",
        "description",
        "image",
        "type",
        "created_at",
        "updated_at",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("user",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if change and "url" in form.changed_data or not change:
            og_data = fetch_og_data(obj.url)
            if og_data:
                obj.title = og_data.get("title", "")
                obj.description = og_data.get("description", "")
                obj.image = og_data.get("image", "")
                obj.type = og_data.get("type", obj.type)
        super().save_model(request, obj, form, change)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("user", "created_at", "updated_at")
    filter_horizontal = ("links",)
    readonly_fields = ("created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("user",)
        return self.readonly_fields
