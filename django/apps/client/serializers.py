from rest_framework import serializers

from apps.client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "tipo_documento",
            "numero_documento",
            "nombre",
            "telefono",
            "email",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_numero_documento(self, value):
        return value.strip()

    def validate_email(self, value):
        if value is None or str(value).strip() == "":
            return ""
        return value.strip().lower()
