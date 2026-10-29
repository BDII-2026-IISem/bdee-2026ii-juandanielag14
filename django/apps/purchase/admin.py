from django.contrib import admin

from apps.purchase.models import Compra, CompraDetalle


class CompraDetalleInline(admin.TabularInline):
    model = CompraDetalle
    extra = 0
    fields = ("producto", "cantidad", "cantidad_recibida", "valor_unitario", "total", "observaciones")
    readonly_fields = ("cantidad_recibida", "total")


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "proveedor", "sucursal", "fecha", "subtotal", "impuestos", "total", "estado")
    list_filter = ("estado", "sucursal")
    search_fields = ("proveedor__razon_social", "proveedor__nit")
    ordering = ("-fecha", "-id")
    readonly_fields = ("subtotal", "total", "estado", "created_at", "updated_at")
    inlines = (CompraDetalleInline,)
