from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models, transaction

from apps.branch.models import Sucursal
from apps.client.models import Client
from apps.common.models import TimeStampedModel
from apps.inventory.models import Inventario
from apps.product.models import Product
from apps.sale.managers import VentaManager


class Venta(TimeStampedModel):
    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA", "Activa"
        ANULADA = "ANULADA", "Anulada"

    cliente = models.ForeignKey(
        Client,
        on_delete=models.RESTRICT,
        related_name="ventas",
        db_column="cliente_id",
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.RESTRICT,
        related_name="ventas",
        db_column="sucursal_id",
    )
    fecha = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    estado = models.CharField(max_length=8, choices=Estado.choices, default=Estado.ACTIVA)

    objects = VentaManager()

    class Meta:
        db_table = "ventas"
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        ordering = ["-fecha", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(subtotal__gte=0)
                & models.Q(impuestos__gte=0)
                & models.Q(total__gte=0),
                name="venta_montos_no_negativos",
            ),
        ]

    def __str__(self):
        return f"Venta {self.pk}"

    def void(self):
        with transaction.atomic():
            venta = Venta.objects.select_for_update().get(pk=self.pk)
            if venta.estado == Venta.Estado.ANULADA:
                return venta
            detalles = venta.detalles.select_for_update().order_by("producto_id")
            for detalle in detalles:
                inventario = Inventario.objects.select_for_update().get(
                    sucursal_id=venta.sucursal_id,
                    producto_id=detalle.producto_id,
                )
                inventario.cantidad += detalle.cantidad
                inventario.save(update_fields=["cantidad", "updated_at"])
            venta.estado = Venta.Estado.ANULADA
            venta.save(update_fields=["estado", "updated_at"])
            return venta


class VentaDetalle(TimeStampedModel):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.RESTRICT,
        related_name="detalles",
        db_column="venta_id",
    )
    producto = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        related_name="lineas_venta",
        db_column="producto_id",
    )
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "venta_detalles"
        verbose_name = "detalle de venta"
        verbose_name_plural = "detalles de venta"
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gte=1)
                & models.Q(valor_unitario__gte=0)
                & models.Q(total__gte=0),
                name="venta_detalle_montos_validos",
            ),
        ]

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

    def save(self, *args, **kwargs):
        self.total = (self.valor_unitario * self.cantidad).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
