from django.contrib import admin

from apps.sale.models import Venta, VentaDetalle


class VentaDetalleInline(admin.TabularInline):
    model = VentaDetalle
    extra = 0
    can_delete = False
    fields = ("producto", "cantidad", "valor_unitario", "total", "observaciones")
    readonly_fields = ("producto", "cantidad", "valor_unitario", "total", "observaciones")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "sucursal", "fecha", "subtotal", "impuestos", "total", "estado")
    list_filter = ("estado", "sucursal")
    search_fields = ("cliente__nombre", "cliente__numero_documento")
    ordering = ("-fecha", "-id")
    date_hierarchy = "fecha"
    readonly_fields = ("cliente", "sucursal", "fecha", "subtotal", "impuestos", "total", "estado", "created_at", "updated_at")
    fieldsets = (
        ("Venta", {"fields": ("cliente", "sucursal", "fecha", "estado")}),
        ("Totales", {"fields": ("subtotal", "impuestos", "total")}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    inlines = (VentaDetalleInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("cliente", "sucursal")
