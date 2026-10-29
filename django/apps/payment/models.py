from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Pago(TimeStampedModel):
    class ReferenciaTipo(models.TextChoices):
        VENTA = "VENTA", "Venta"
        COMPRA = "COMPRA", "Compra"

    class Metodo(models.TextChoices):
        EFECTIVO = "EFECTIVO", "Efectivo"
        TARJETA = "TARJETA", "Tarjeta"
        TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"

    class Estado(models.TextChoices):
        APLICADO = "APLICADO", "Aplicado"
        ANULADO = "ANULADO", "Anulado"

    referencia_tipo = models.CharField(max_length=10, choices=ReferenciaTipo.choices)
    referencia_id = models.PositiveIntegerField()
    metodo = models.CharField(max_length=15, choices=Metodo.choices)
    monto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.APLICADO)

    class Meta:
        db_table = "pagos"
        verbose_name = "pago"
        verbose_name_plural = "pagos"
        ordering = ["-fecha", "-id"]
        indexes = [models.Index(fields=["referencia_tipo", "referencia_id"], name="pago_referencia_idx")]
        constraints = [
            models.CheckConstraint(condition=models.Q(monto__gt=0), name="pago_monto_positivo"),
        ]

    def __str__(self):
        return f"{self.referencia_tipo} {self.referencia_id} - {self.monto}"
