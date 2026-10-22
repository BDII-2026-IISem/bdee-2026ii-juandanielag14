from django.core.validators import MinLengthValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Sucursal(TimeStampedModel):
    nombre = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    descripcion = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "sucursales"
        verbose_name = "sucursal"
        verbose_name_plural = "sucursales"
        ordering = ["nombre", "id"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip()
        super().save(*args, **kwargs)
