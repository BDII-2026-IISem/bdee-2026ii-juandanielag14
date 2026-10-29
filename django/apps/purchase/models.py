from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.branch.models import Sucursal
from apps.common.models import TimeStampedModel
from apps.product.models import Product
from apps.supplier.models import Proveedor


class Compra(TimeStampedModel):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        PARCIAL = "PARCIAL", "Parcial"
        RECIBIDA = "RECIBIDA", "Recibida"
        ANULADA = "ANULADA", "Anulada"

    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.RESTRICT, related_name="compras", db_column="proveedor_id"
    )
    sucursal = models.ForeignKey(
        Sucursal, on_delete=models.RESTRICT, related_name="compras", db_column="sucursal_id"
    )
    fecha = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE)

    class Meta:
        db_table = "compras"
        verbose_name = "compra"
        verbose_name_plural = "compras"
        ordering = ["-fecha", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(subtotal__gte=0) & models.Q(impuestos__gte=0) & models.Q(total__gte=0),
                name="compra_montos_no_negativos",
            ),
        ]

    def __str__(self):
        return f"Compra {self.pk}"

    def recalcular_totales(self):
        subtotal = sum((linea.total for linea in self.detalles.all()), Decimal("0.00"))
        self.subtotal = subtotal.quantize(Decimal("0.01"))
        self.total = (self.subtotal + self.impuestos).quantize(Decimal("0.01"))
        self.save(update_fields=["subtotal", "total", "updated_at"])


class CompraDetalle(TimeStampedModel):
    compra = models.ForeignKey(
        Compra, on_delete=models.RESTRICT, related_name="detalles", db_column="compra_id"
    )
    producto = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="lineas_compra", db_column="producto_id"
    )
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cantidad_recibida = models.PositiveIntegerField(default=0)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "compra_detalles"
        verbose_name = "detalle de compra"
        verbose_name_plural = "detalles de compra"
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad_recibida__lte=models.F("cantidad")),
                name="compra_detalle_recibida_no_excede",
            ),
            models.CheckConstraint(
                condition=models.Q(valor_unitario__gte=0) & models.Q(total__gte=0),
                name="compra_detalle_montos_validos",
            ),
        ]

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

    @property
    def pendiente(self):
        return self.cantidad - self.cantidad_recibida

    def save(self, *args, **kwargs):
        self.total = (self.valor_unitario * self.cantidad).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
