import contextlib

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


class HardDeleteAdmin(admin.ModelAdmin):
    def get_queryset(self, request):  # noqa: ARG002
        return self.model.all_objects.all()


def auto_register_admin(app_label: str, skip_models: list | None = None) -> None:
    """
    Automatically registers all models in the given app with dynamic ModelAdmin
    classes using model-defined admin attributes:
        - admin_list_display
        - admin_search_fields
        - admin_list_filter
        - admin_ordering
        - admin_readonly_fields.

    Usage in admin.py:
        auto_register_admin("core", skip_models=["User"])
    """  # noqa: D205
    app_config = apps.get_app_config(app_label)
    app_models = app_config.get_models()

    skip_models = skip_models or []

    for model in app_models:
        if model.__name__ in skip_models:
            continue

        # Extract admin metadata from model, provide safe defaults
        list_display = getattr(
            model,
            "admin_list_display",
            [f.name for f in model._meta.fields if f.concrete],  # noqa: SLF001
        )
        search_fields = getattr(model, "admin_search_fields", [])
        list_filter = getattr(model, "admin_list_filter", [])
        ordering = getattr(model, "admin_ordering", [])
        readonly_fields = getattr(model, "admin_readonly_fields", [])

        # Dynamic attributes dict
        class_attrs = {
            "list_display": list_display,
            "search_fields": search_fields,
            "list_filter": list_filter,
            "ordering": ordering,
            "readonly_fields": readonly_fields,
        }

        # Create dynamic ModelAdmin class
        admin_class = type(
            f"{model.__name__}Admin",
            (admin.ModelAdmin,),
            class_attrs,
        )

        # Safe registration
        with contextlib.suppress(AlreadyRegistered):
            admin.site.register(model, admin_class)
