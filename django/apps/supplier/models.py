from django.core.validators import MinLengthValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Proveedor(TimeStampedModel):
    nit = models.CharField(max_length=30, unique=True)
    razon_social = models.CharField(max_length=150, validators=[MinLengthValidator(2)])
    contacto = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "proveedores"
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"
        ordering = ["razon_social", "id"]

    def __str__(self):
        return self.razon_social

    def save(self, *args, **kwargs):
        self.nit = self.nit.strip()
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)
