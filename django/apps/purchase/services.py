from django.core.exceptions import ValidationError
from django.db import transaction

from apps.inventory.models import Inventario
from apps.purchase.models import Compra, CompraDetalle


def recibir_compra(compra, recepciones):
    if compra.estado == Compra.Estado.ANULADA:
        raise ValidationError({"compra": ["La compra está anulada."]})
    if not recepciones:
        raise ValidationError({"recepciones": ["Debe indicar al menos una línea."]})

    cantidades = {}
    for item in recepciones:
        cantidad = int(item["cantidad"])
        if cantidad < 1:
            raise ValidationError({"recepciones": ["La cantidad recibida debe ser al menos 1."]})
        detalle_id = int(item["detalle_id"])
        cantidades[detalle_id] = cantidades.get(detalle_id, 0) + cantidad

    with transaction.atomic():
        compra = Compra.objects.select_for_update().get(pk=compra.pk)
        if not compra.sucursal.is_active:
            raise ValidationError({"sucursal": ["La sucursal no está activa."]})

        detalles = {
            d.pk: d
            for d in CompraDetalle.objects.select_for_update().filter(compra=compra, pk__in=cantidades)
        }
        if len(detalles) != len(cantidades):
            raise ValidationError({"recepciones": ["Hay líneas que no pertenecen a esta compra."]})

        for detalle_id, cantidad in cantidades.items():
            detalle = detalles[detalle_id]
            if cantidad > detalle.pendiente:
                raise ValidationError(
                    {"recepciones": [f"Se intenta recibir {cantidad} de {detalle.producto}, pendientes: {detalle.pendiente}."]}
                )

        for detalle_id in sorted(cantidades):
            detalle = detalles[detalle_id]
            cantidad = cantidades[detalle_id]
            inventario, _ = Inventario.objects.get_or_create(
                sucursal=compra.sucursal,
                producto=detalle.producto,
                defaults={"cantidad": 0},
            )
            inventario = Inventario.objects.select_for_update().get(pk=inventario.pk)
            inventario.cantidad += cantidad
            inventario.save(update_fields=["cantidad", "updated_at"])

            detalle.cantidad_recibida += cantidad
            detalle.save(update_fields=["cantidad_recibida", "updated_at"])

        pendientes = sum(d.pendiente for d in compra.detalles.all())
        compra.estado = Compra.Estado.RECIBIDA if pendientes == 0 else Compra.Estado.PARCIAL
        compra.save(update_fields=["estado", "updated_at"])
        return compra
