from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.testing import PASSWORD, create_active_user
from apps.security.models import RefreshToken
from apps.security.tokens import hash_token


class RefreshRotationTests(APITestCase):
    def setUp(self):
        create_active_user()

    def _login(self):
        response = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["refresh"]

    def _refresh(self, raw):
        return self.client.post("/api/auth/refresh/", {"refresh": raw}, format="json")

    def test_refresh_rotates_the_token(self):
        first = self._login()
        rotated = self._refresh(first)
        self.assertEqual(rotated.status_code, status.HTTP_200_OK)
        self.assertNotEqual(first, rotated.data["refresh"])

    def test_reuse_revokes_the_whole_family(self):
        first = self._login()
        second = self._refresh(first).data["refresh"]
        reused = self._refresh(first)
        self.assertEqual(reused.status_code, status.HTTP_401_UNAUTHORIZED)
        after_reuse = self._refresh(second)
        self.assertEqual(after_reuse.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_token_is_rejected_without_revoking_family(self):
        raw = self._login()
        RefreshToken.objects.filter(token_hash=hash_token(raw)).update(
            expires_at=timezone.now() - timedelta(minutes=1)
        )
        response = self._refresh(raw)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(RefreshToken.objects.get(token_hash=hash_token(raw)).revoked_at)
