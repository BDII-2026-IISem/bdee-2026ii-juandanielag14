from decimal import Decimal
from unittest.mock import patch

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.branch.models import Sucursal
from apps.client.models import Client
from apps.common.testing import create_active_user, grant_business
from apps.inventory.models import Inventario
from apps.product.models import Product
from apps.sale.models import Venta, VentaDetalle


class VentaRegistroTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()
        grant_business(self.user)
        self.client.force_authenticate(user=self.user)
        self.sucursal = Sucursal.objects.create(nombre="Centro")
        self.cliente = Client.objects.create(tipo_documento="CC", numero_documento="8001", nombre="Ana")
        self.agua = Product.objects.create(sku="AGUA-11", nombre="Agua", precio=Decimal("10.00"))
        self.pan = Product.objects.create(sku="PAN-11", nombre="Pan", precio=Decimal("4.50"))
        self.inv_agua = Inventario.objects.create(sucursal=self.sucursal, producto=self.agua, cantidad=5)
        self.inv_pan = Inventario.objects.create(sucursal=self.sucursal, producto=self.pan, cantidad=2)

    def _payload(self, items, impuestos="0.00"):
        return {
            "clienteId": self.cliente.id,
            "sucursalId": self.sucursal.id,
            "fecha": timezone.now().isoformat(),
            "impuestos": impuestos,
            "items": items,
        }

    def test_register_computes_totals_and_discounts_stock(self):
        response = self.client.post(
            "/api/ventas/",
            self._payload(
                [
                    {"productoId": self.agua.id, "cantidad": 2},
                    {"productoId": self.pan.id, "cantidad": 1},
                ],
                impuestos="1.00",
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["subtotal"], "24.50")
        self.assertEqual(response.data["total"], "25.50")
        self.assertEqual(response.data["estado"], "ACTIVA")
        self.inv_agua.refresh_from_db()
        self.inv_pan.refresh_from_db()
        self.assertEqual(self.inv_agua.cantidad, 3)
        self.assertEqual(self.inv_pan.cantidad, 1)

    def test_detail_keeps_price_when_catalog_changes(self):
        response = self.client.post(
            "/api/ventas/",
            self._payload([{"productoId": self.agua.id, "cantidad": 1}]),
            format="json",
        )
        Product.objects.filter(pk=self.agua.pk).update(precio=Decimal("99.00"))
        detalle = VentaDetalle.objects.get(venta_id=response.data["id"])
        self.assertEqual(detalle.valor_unitario, Decimal("10.00"))

    def test_insufficient_stock_is_rejected_without_rows(self):
        response = self.client.post(
            "/api/ventas/",
            self._payload([{"productoId": self.pan.id, "cantidad": 3}]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Venta.objects.count(), 0)
        self.inv_pan.refresh_from_db()
        self.assertEqual(self.inv_pan.cantidad, 2)

    def test_failure_during_stock_update_rolls_back_everything(self):
        original = Inventario.save

        def fail_on_stock(inventario, *args, **kwargs):
            if "cantidad" in (kwargs.get("update_fields") or []):
                raise RuntimeError("fallo al descontar inventario")
            return original(inventario, *args, **kwargs)

        with patch.object(Inventario, "save", fail_on_stock):
            with self.assertRaises(RuntimeError):
                self.client.post(
                    "/api/ventas/",
                    self._payload([{"productoId": self.agua.id, "cantidad": 1}]),
                    format="json",
                )
        self.assertEqual(Venta.objects.count(), 0)
        self.assertEqual(VentaDetalle.objects.count(), 0)
        self.inv_agua.refresh_from_db()
        self.assertEqual(self.inv_agua.cantidad, 5)

    def test_inactive_product_is_rejected(self):
        self.pan.is_active = False
        self.pan.save(update_fields=["is_active", "updated_at"])
        response = self.client.post(
            "/api/ventas/",
            self._payload([{"productoId": self.pan.id, "cantidad": 1}]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Venta.objects.count(), 0)


class VentaLecturaTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()
        grant_business(self.user)
        self.client.force_authenticate(user=self.user)
        self.sucursal = Sucursal.objects.create(nombre="Sur")
        self.cliente = Client.objects.create(tipo_documento="CC", numero_documento="8101", nombre="Luis")
        self.agua = Product.objects.create(sku="AGUA-12", nombre="Agua", precio=Decimal("10.00"))
        self.inventario = Inventario.objects.create(sucursal=self.sucursal, producto=self.agua, cantidad=5)

    def _crear_venta(self, cantidad):
        response = self.client.post(
            "/api/ventas/",
            {
                "clienteId": self.cliente.id,
                "sucursalId": self.sucursal.id,
                "fecha": timezone.now().isoformat(),
                "impuestos": "0.00",
                "items": [{"productoId": self.agua.id, "cantidad": cantidad}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        return response.data["id"]

    def test_list_returns_the_registered_sale(self):
        venta_id = self._crear_venta(1)
        listed = self.client.get("/api/ventas/")
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertTrue(any(row["id"] == venta_id for row in listed.data))

    def test_detail_keeps_historical_price(self):
        venta_id = self._crear_venta(1)
        Product.objects.filter(pk=self.agua.pk).update(precio=Decimal("99.00"))
        detail = self.client.get(f"/api/ventas/{venta_id}/")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["detalles"][0]["valor_unitario"], "10.00")

    def test_void_restores_inventory_once(self):
        venta_id = self._crear_venta(2)
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.cantidad, 3)
        first = self.client.delete(f"/api/ventas/{venta_id}/")
        second = self.client.delete(f"/api/ventas/{venta_id}/")
        self.assertEqual(first.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(second.status_code, status.HTTP_204_NO_CONTENT)
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.cantidad, 5)
        self.assertEqual(Venta.objects.get(pk=venta_id).estado, Venta.Estado.ANULADA)
