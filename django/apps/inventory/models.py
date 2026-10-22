from django.db import models

from apps.branch.models import Sucursal
from apps.product.models import Product


class Inventario(models.Model):
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.RESTRICT,
        related_name="inventario",
        db_column="sucursal_id",
    )
    producto = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        related_name="inventario",
        db_column="producto_id",
    )
    cantidad = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventarios"
        verbose_name = "inventario"
        verbose_name_plural = "inventarios"
        ordering = ["sucursal_id", "producto_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["sucursal", "producto"],
                name="inventario_sucursal_producto_uq",
            ),
        ]

    def __str__(self):
        return f"{self.sucursal} - {self.producto}: {self.cantidad}"
