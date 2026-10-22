from django.contrib import admin

from apps.client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nombre", "numero_documento", "tipo_documento", "email", "telefono", "is_active", "created_at")
    list_filter = ("is_active", "tipo_documento")
    search_fields = ("nombre", "numero_documento", "email", "telefono")
    list_editable = ("is_active",)
    ordering = ("nombre", "id")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Documento", {"fields": ("tipo_documento", "numero_documento")}),
        ("Contacto", {"fields": ("nombre", "telefono", "email")}),
        ("Estado", {"fields": ("is_active",)}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
