from decimal import Decimal
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.branch.models import Sucursal
from apps.inventory.models import Inventario
from apps.product.models import Product
from apps.purchase.models import Compra, CompraDetalle
from apps.purchase.services import recibir_compra
from apps.supplier.models import Proveedor


class RecepcionCompraTests(TestCase):
    def setUp(self):
        self.proveedor = Proveedor.objects.create(nit="900200", razon_social="Lácteos del Sur")
        self.sucursal = Sucursal.objects.create(nombre="Norte")
        self.producto = Product.objects.create(sku="LECHE-2", nombre="Leche", precio=Decimal("3000.00"))
        self.compra = Compra.objects.create(proveedor=self.proveedor, sucursal=self.sucursal, fecha=timezone.now())
        self.linea = CompraDetalle.objects.create(
            compra=self.compra, producto=self.producto, cantidad=5, valor_unitario=Decimal("1000.00")
        )

    def test_partial_reception_adds_inventory_and_sets_parcial(self):
        recibir_compra(self.compra, [{"detalle_id": self.linea.pk, "cantidad": 2}])
        inventario = Inventario.objects.get(sucursal=self.sucursal, producto=self.producto)
        self.assertEqual(inventario.cantidad, 2)
        self.compra.refresh_from_db()
        self.assertEqual(self.compra.estado, Compra.Estado.PARCIAL)

    def test_full_reception_sets_recibida(self):
        recibir_compra(self.compra, [{"detalle_id": self.linea.pk, "cantidad": 2}])
        recibir_compra(self.compra, [{"detalle_id": self.linea.pk, "cantidad": 3}])
        inventario = Inventario.objects.get(sucursal=self.sucursal, producto=self.producto)
        self.assertEqual(inventario.cantidad, 5)
        self.compra.refresh_from_db()
        self.assertEqual(self.compra.estado, Compra.Estado.RECIBIDA)

    def test_over_reception_is_rejected(self):
        with self.assertRaises(ValidationError):
            recibir_compra(self.compra, [{"detalle_id": self.linea.pk, "cantidad": 6}])
        self.assertFalse(Inventario.objects.filter(sucursal=self.sucursal, producto=self.producto).exists())

    def test_failure_during_inventory_update_rolls_back(self):
        original = Inventario.save

        def fail_on_stock(inventario, *args, **kwargs):
            if "cantidad" in (kwargs.get("update_fields") or []):
                raise RuntimeError("fallo al sumar inventario")
            return original(inventario, *args, **kwargs)

        with patch.object(Inventario, "save", fail_on_stock):
            with self.assertRaises(RuntimeError):
                recibir_compra(self.compra, [{"detalle_id": self.linea.pk, "cantidad": 2}])
        self.linea.refresh_from_db()
        self.compra.refresh_from_db()
        self.assertEqual(self.linea.cantidad_recibida, 0)
        self.assertEqual(self.compra.estado, Compra.Estado.PENDIENTE)
        self.assertFalse(Inventario.objects.filter(sucursal=self.sucursal, producto=self.producto).exists())
