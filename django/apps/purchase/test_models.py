from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.branch.models import Sucursal
from apps.product.models import Product
from apps.purchase.models import Compra, CompraDetalle
from apps.supplier.models import Proveedor


class CompraModelTests(TestCase):
    def setUp(self):
        self.proveedor = Proveedor.objects.create(nit="900100", razon_social="Distribuidora Norte")
        self.sucursal = Sucursal.objects.create(nombre="Centro")
        self.producto = Product.objects.create(sku="ARROZ-1", nombre="Arroz", precio=Decimal("3000.00"))
        self.compra = Compra.objects.create(
            proveedor=self.proveedor,
            sucursal=self.sucursal,
            fecha=timezone.now(),
            impuestos=Decimal("100.00"),
        )

    def test_total_includes_taxes(self):
        CompraDetalle.objects.create(
            compra=self.compra, producto=self.producto, cantidad=2, valor_unitario=Decimal("1500.00")
        )
        self.compra.recalcular_totales()
        self.compra.refresh_from_db()
        self.assertEqual(self.compra.subtotal, Decimal("3000.00"))
        self.assertEqual(self.compra.total, Decimal("3100.00"))

    def test_partial_reception_keeps_pending_quantity(self):
        linea = CompraDetalle.objects.create(
            compra=self.compra, producto=self.producto, cantidad=5, valor_unitario=Decimal("1000.00")
        )
        linea.cantidad_recibida = 2
        linea.save(update_fields=["cantidad_recibida", "updated_at"])
        linea.refresh_from_db()
        self.assertEqual(linea.pendiente, 3)

    def test_cannot_receive_more_than_ordered(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            CompraDetalle.objects.create(
                compra=self.compra,
                producto=self.producto,
                cantidad=2,
                cantidad_recibida=3,
                valor_unitario=Decimal("1000.00"),
            )

    def test_nit_is_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Proveedor.objects.create(nit="900100", razon_social="Otro proveedor")
