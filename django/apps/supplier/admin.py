from django.contrib import admin

from apps.supplier.models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "nit", "telefono", "email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("razon_social", "nit", "email")
    list_editable = ("is_active",)
    ordering = ("razon_social", "id")
    readonly_fields = ("created_at", "updated_at")
