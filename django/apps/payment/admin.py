from django.contrib import admin

from apps.payment.models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "referencia_tipo", "referencia_id", "metodo", "monto", "fecha", "estado")
    list_filter = ("referencia_tipo", "metodo", "estado")
    search_fields = ("referencia_id",)
    ordering = ("-fecha", "-id")
    readonly_fields = ("referencia_tipo", "referencia_id", "metodo", "monto", "fecha", "estado", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
