from decimal import Decimal

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.branch.models import Sucursal
from apps.client.models import Client
from apps.product.models import Product
from apps.sale.models import Venta, VentaDetalle


class VentaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaDetalle
        fields = ["id", "producto", "cantidad", "valor_unitario", "total", "observaciones", "created_at", "updated_at"]
        read_only_fields = ["id", "valor_unitario", "total", "created_at", "updated_at"]


class VentaSerializer(serializers.ModelSerializer):
    detalles = VentaDetalleSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = [
            "id",
            "cliente",
            "sucursal",
            "fecha",
            "subtotal",
            "impuestos",
            "total",
            "estado",
            "detalles",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "subtotal", "impuestos", "total", "estado", "created_at", "updated_at"]


class VentaItemSerializer(serializers.Serializer):
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="producto")
    cantidad = serializers.IntegerField(min_value=1)
    observaciones = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")


class VentaRegistroSerializer(serializers.Serializer):
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source="cliente")
    sucursal_id = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all(), source="sucursal")
    fecha = serializers.DateTimeField()
    impuestos = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        required=False,
        default=Decimal("0.00"),
    )
    items = VentaItemSerializer(many=True, allow_empty=False)

    def create(self, validated_data):
        items = [
            {
                "producto_id": item["producto"].id,
                "cantidad": item["cantidad"],
                "observaciones": item["observaciones"],
            }
            for item in validated_data["items"]
        ]
        try:
            return Venta.objects.register(
                cliente=validated_data["cliente"],
                sucursal=validated_data["sucursal"],
                fecha=validated_data["fecha"],
                impuestos=validated_data["impuestos"],
                items=items,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                exc.message_dict if hasattr(exc, "error_dict") else exc.messages
            ) from exc
