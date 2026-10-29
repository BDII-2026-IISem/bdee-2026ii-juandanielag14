from django.contrib import admin

from apps.product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "nombre", "precio", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("sku", "nombre", "descripcion")
    list_editable = ("precio", "is_active")
    ordering = ("nombre", "id")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Información", {"fields": ("sku", "nombre", "descripcion")}),
        ("Precio y estado", {"fields": ("precio", "is_active")}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def has_delete_permission(self, request, obj=None):
        return False
