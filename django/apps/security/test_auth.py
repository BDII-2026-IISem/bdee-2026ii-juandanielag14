from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.status import RecordStatus
from apps.common.testing import PASSWORD, create_active_user
from apps.security.models import RefreshToken
from apps.security.tokens import hash_token


class AuthFlowTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()

    def test_login_with_username_returns_tokens_and_stores_hash(self):
        response = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertNotIn("password", response.data)
        stored = RefreshToken.objects.get()
        self.assertEqual(stored.token_hash, hash_token(response.data["refresh"]))

    def test_login_with_email_is_case_insensitive(self):
        response = self.client.post(
            "/api/auth/login/",
            {"email": "ANA@PUNTOSTOCK.TEST", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inactive_user_gets_401(self):
        self.user.status = RecordStatus.INACTIVE
        self.user.save()
        response = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_password_gets_same_401(self):
        response = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": "otra-clave"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Credenciales inválidas.")
