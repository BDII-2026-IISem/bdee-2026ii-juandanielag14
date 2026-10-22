from django.contrib import admin

from apps.inventory.models import Inventario


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ("sucursal", "producto", "cantidad", "stock_minimo", "updated_at")
    list_filter = ("sucursal",)
    search_fields = ("producto__sku", "producto__nombre", "sucursal__nombre")
    list_editable = ("stock_minimo",)
    ordering = ("sucursal", "producto")
    readonly_fields = ("cantidad", "updated_at")
    fieldsets = (
        ("Ubicación", {"fields": ("sucursal", "producto")}),
        ("Existencias", {"fields": ("cantidad", "stock_minimo")}),
        ("Auditoría", {"fields": ("updated_at",), "classes": ("collapse",)}),
    )
