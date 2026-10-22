from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from apps.branch.models import Sucursal
from apps.common.testing import create_active_user, grant_business
from apps.inventory.models import Inventario
from apps.product.models import Product


class ProductoApiTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()
        grant_business(self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_normalizes_sku_and_is_active_by_default(self):
        response = self.client.post(
            "/api/productos/",
            {"sku": "agua-600", "nombre": "Agua 600ml", "precio": "1500.00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["sku"], "AGUA-600")
        self.assertTrue(response.data["is_active"])

    def test_duplicate_sku_is_rejected(self):
        payload = {"sku": "CAFE-1", "nombre": "Café", "precio": "3000.00"}
        self.assertEqual(self.client.post("/api/productos/", payload, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/productos/", payload, format="json").status_code, 400)

    def test_negative_price_is_rejected(self):
        response = self.client.post(
            "/api/productos/",
            {"sku": "JUGO-1", "nombre": "Jugo", "precio": "-5.00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_and_soft_delete(self):
        producto = Product.objects.create(sku="LECHE-1", nombre="Leche", precio=Decimal("3200.00"))
        patch = self.client.patch(f"/api/productos/{producto.pk}/", {"precio": "3500.00"}, format="json")
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        delete = self.client.delete(f"/api/productos/{producto.pk}/")
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        producto.refresh_from_db()
        self.assertFalse(producto.is_active)
        self.assertEqual(Product.objects.count(), 1)


class ProductoDisponibleTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()
        grant_business(self.user)
        self.client.force_authenticate(user=self.user)
        self.sucursal = Sucursal.objects.create(nombre="Norte")
        self.producto = Product.objects.create(sku="PAN-1", nombre="Pan", precio=Decimal("800.00"))
        self.inventario = Inventario.objects.create(
            sucursal=self.sucursal, producto=self.producto, cantidad=4
        )

    def test_lists_products_with_stock_in_branch(self):
        response = self.client.get(f"/api/productos/disponibles/?sucursal={self.sucursal.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_empty_when_stock_is_zero(self):
        self.inventario.cantidad = 0
        self.inventario.save(update_fields=["cantidad", "updated_at"])
        response = self.client.get(f"/api/productos/disponibles/?sucursal={self.sucursal.pk}")
        self.assertEqual(response.data, [])

    def test_sucursal_is_required(self):
        response = self.client.get("/api/productos/disponibles/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
