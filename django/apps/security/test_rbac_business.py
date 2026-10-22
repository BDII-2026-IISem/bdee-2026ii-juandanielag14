from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.testing import create_active_user


class BusinessRbacTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()

    def test_missing_grant_is_403(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/clientes/",
            {"tipoDocumento": "CC", "numeroDocumento": "9001", "nombre": "Sin Permiso"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_identity_is_401(self):
        response = self.client.get("/api/clientes/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
