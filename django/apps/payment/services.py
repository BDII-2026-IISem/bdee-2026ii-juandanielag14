from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum

from apps.payment.models import Pago
from apps.purchase.models import Compra
from apps.sale.models import Venta


def _referencia(referencia_tipo, referencia_id):
    modelo = {Pago.ReferenciaTipo.VENTA: Venta, Pago.ReferenciaTipo.COMPRA: Compra}.get(referencia_tipo)
    if modelo is None:
        raise ValidationError({"referencia_tipo": ["Tipo de referencia no válido."]})
    try:
        return modelo.objects.select_for_update().get(pk=referencia_id)
    except modelo.DoesNotExist:
        raise ValidationError({"referencia_id": ["No existe la referencia indicada."]})


def registrar_pago(*, referencia_tipo, referencia_id, metodo, monto, fecha):
    monto = Decimal(monto).quantize(Decimal("0.01"))
    if monto <= 0:
        raise ValidationError({"monto": ["El monto debe ser mayor que cero."]})
    with transaction.atomic():
        referencia = _referencia(referencia_tipo, referencia_id)
        if referencia.estado == "ANULADA":
            raise ValidationError({"referencia_id": ["La referencia está anulada."]})
        pagado = (
            Pago.objects.filter(
                referencia_tipo=referencia_tipo,
                referencia_id=referencia_id,
                estado=Pago.Estado.APLICADO,
            ).aggregate(total=Sum("monto"))["total"]
            or Decimal("0.00")
        )
        saldo = referencia.total - pagado
        if monto > saldo:
            raise ValidationError({"monto": [f"El pago supera el saldo pendiente ({saldo})."]})
        return Pago.objects.create(
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id,
            metodo=metodo,
            monto=monto,
            fecha=fecha,
        )


def registrar_pagos_mixtos(*, venta, pagos, fecha):
    suma = sum((Decimal(p["monto"]).quantize(Decimal("0.01")) for p in pagos), Decimal("0.00"))
    if suma != venta.total:
        raise ValidationError(
            {"pagos": [f"La suma de los pagos ({suma}) debe ser igual al total de la venta ({venta.total})."]}
        )
    with transaction.atomic():
        return [
            registrar_pago(
                referencia_tipo=Pago.ReferenciaTipo.VENTA,
                referencia_id=venta.pk,
                metodo=p["metodo"],
                monto=p["monto"],
                fecha=fecha,
            )
            for p in pagos
        ]
