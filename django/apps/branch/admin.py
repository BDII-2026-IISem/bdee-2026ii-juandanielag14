from django.contrib import admin

from apps.branch.models import Sucursal


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("nombre", "descripcion")
    list_editable = ("is_active",)
    ordering = ("nombre", "id")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Información", {"fields": ("nombre", "descripcion")}),
        ("Estado", {"fields": ("is_active",)}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def has_delete_permission(self, request, obj=None):
        return False
