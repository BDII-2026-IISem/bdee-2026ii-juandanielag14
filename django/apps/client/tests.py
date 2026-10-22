import json

from rest_framework import status
from rest_framework.test import APITestCase

from apps.client.models import Client
from apps.common.testing import create_active_user, grant_business


class ClientApiTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()
        grant_business(self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_returns_camel_case_and_normalizes_email(self):
        response = self.client.post(
            "/api/clientes/",
            {
                "tipoDocumento": "CC",
                "numeroDocumento": "3001",
                "nombre": "María García",
                "email": "Maria@Example.com",
                "telefono": "3001234567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["is_active"])
        wire = json.loads(response.content)
        self.assertIn("numeroDocumento", wire)
        self.assertNotIn("numero_documento", wire)
        stored = Client.objects.get(pk=response.data["id"])
        self.assertEqual(stored.email, "maria@example.com")

    def test_invalid_name_is_rejected(self):
        response = self.client.post(
            "/api/clientes/",
            {"tipoDocumento": "CC", "numeroDocumento": "3002", "nombre": "A"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_document_is_rejected(self):
        payload = {"tipoDocumento": "CC", "numeroDocumento": "3003", "nombre": "Luis Mora"}
        self.assertEqual(self.client.post("/api/clientes/", payload, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/clientes/", payload, format="json").status_code, 400)

    def test_delete_is_soft_and_list_filters_active(self):
        cliente = Client.objects.create(tipo_documento="CC", numero_documento="3004", nombre="Pedro León")
        Client.objects.create(tipo_documento="CC", numero_documento="3005", nombre="Inactivo", is_active=False)
        response = self.client.delete(f"/api/clientes/{cliente.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cliente.refresh_from_db()
        self.assertFalse(cliente.is_active)
        activos = self.client.get("/api/clientes/?is_active=true")
        self.assertEqual(activos.status_code, status.HTTP_200_OK)
        self.assertEqual(activos.data, [])
