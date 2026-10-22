from rest_framework import serializers

from apps.branch.models import Sucursal


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ["id", "nombre", "descripcion", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
