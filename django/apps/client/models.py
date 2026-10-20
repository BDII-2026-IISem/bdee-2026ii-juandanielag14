from django.core.validators import MinLengthValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Client(TimeStampedModel):
    class DocumentType(models.TextChoices):
        CC = "CC", "Cédula de ciudadanía"
        NIT = "NIT", "NIT"
        CE = "CE", "Cédula de extranjería"
        PASAPORTE = "PASAPORTE", "Pasaporte"

    tipo_documento = models.CharField(max_length=10, choices=DocumentType.choices)
    numero_documento = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150, validators=[MinLengthValidator(2)])
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "clientes"
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ["nombre", "id"]

    def __str__(self):
        return f"{self.nombre} ({self.numero_documento})"

    def save(self, *args, **kwargs):
        self.numero_documento = self.numero_documento.strip()
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)
