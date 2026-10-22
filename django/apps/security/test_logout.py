from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.testing import PASSWORD, create_active_user


class LogoutTests(APITestCase):
    def setUp(self):
        create_active_user()

    def _login(self):
        response = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        return response.data["refresh"]

    def test_logout_returns_204_without_bearer(self):
        raw = self._login()
        response = self.client.post("/api/auth/logout/", {"refresh": raw}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_refresh_after_logout_is_rejected(self):
        raw = self._login()
        self.client.post("/api/auth/logout/", {"refresh": raw}, format="json")
        again = self.client.post("/api/auth/refresh/", {"refresh": raw}, format="json")
        self.assertEqual(again.status_code, status.HTTP_401_UNAUTHORIZED)
