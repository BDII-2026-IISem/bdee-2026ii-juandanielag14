from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.branch.models import Sucursal
from apps.client.models import Client
from apps.inventory.models import Inventario
from apps.payment.models import Pago
from apps.payment.services import registrar_pago, registrar_pagos_mixtos
from apps.product.models import Product
from apps.purchase.models import Compra, CompraDetalle
from apps.sale.models import Venta
from apps.supplier.models import Proveedor


class PagosTests(TestCase):
    def setUp(self):
        self.sucursal = Sucursal.objects.create(nombre="Sur")
        self.cliente = Client.objects.create(tipo_documento="CC", numero_documento="9100", nombre="Marta")
        self.producto = Product.objects.create(sku="PAN-9", nombre="Pan", precio=Decimal("10.00"))
        Inventario.objects.create(sucursal=self.sucursal, producto=self.producto, cantidad=10)
        self.venta = Venta.objects.register(
            cliente=self.cliente,
            sucursal=self.sucursal,
            fecha=timezone.now(),
            items=[{"producto_id": self.producto.id, "cantidad": 2}],
        )

    def test_mixed_payment_covers_total(self):
        pagos = registrar_pagos_mixtos(
            venta=self.venta,
            pagos=[
                {"metodo": Pago.Metodo.EFECTIVO, "monto": "12.00"},
                {"metodo": Pago.Metodo.TARJETA, "monto": "8.00"},
            ],
            fecha=timezone.now(),
        )
        self.assertEqual(len(pagos), 2)
        self.assertEqual(Pago.objects.filter(referencia_id=self.venta.pk).count(), 2)

    def test_mixed_payment_must_equal_total(self):
        with self.assertRaises(ValidationError):
            registrar_pagos_mixtos(
                venta=self.venta,
                pagos=[{"metodo": Pago.Metodo.EFECTIVO, "monto": "15.00"}],
                fecha=timezone.now(),
            )
        self.assertEqual(Pago.objects.count(), 0)

    def test_payment_above_balance_is_rejected(self):
        registrar_pago(
            referencia_tipo=Pago.ReferenciaTipo.VENTA,
            referencia_id=self.venta.pk,
            metodo=Pago.Metodo.EFECTIVO,
            monto="15.00",
            fecha=timezone.now(),
        )
        with self.assertRaises(ValidationError):
            registrar_pago(
                referencia_tipo=Pago.ReferenciaTipo.VENTA,
                referencia_id=self.venta.pk,
                metodo=Pago.Metodo.TARJETA,
                monto="10.00",
                fecha=timezone.now(),
            )

    def test_cannot_pay_voided_sale(self):
        self.venta.void()
        with self.assertRaises(ValidationError):
            registrar_pago(
                referencia_tipo=Pago.ReferenciaTipo.VENTA,
                referencia_id=self.venta.pk,
                metodo=Pago.Metodo.EFECTIVO,
                monto="5.00",
                fecha=timezone.now(),
            )

    def test_payment_on_purchase_uses_same_rules(self):
        proveedor = Proveedor.objects.create(nit="900300", razon_social="Granos Andinos")
        compra = Compra.objects.create(proveedor=proveedor, sucursal=self.sucursal, fecha=timezone.now())
        CompraDetalle.objects.create(
            compra=compra, producto=self.producto, cantidad=3, valor_unitario=Decimal("1000.00")
        )
        compra.recalcular_totales()
        pago = registrar_pago(
            referencia_tipo=Pago.ReferenciaTipo.COMPRA,
            referencia_id=compra.pk,
            metodo=Pago.Metodo.TRANSFERENCIA,
            monto="1000.00",
            fecha=timezone.now(),
        )
        self.assertEqual(pago.referencia_tipo, Pago.ReferenciaTipo.COMPRA)
