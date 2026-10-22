from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.status import RecordStatus
from apps.common.testing import PASSWORD, create_active_user


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()

    def _access(self):
        login = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        return login.data["access"]

    def test_profile_requires_token(self):
        response = self.client.get("/api/auth/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_returns_user_without_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self._access()}")
        response = self.client.get("/api/auth/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "ana")
        self.assertNotIn("password", response.data)

    def test_patch_updates_first_name(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self._access()}")
        response = self.client.patch("/api/auth/profile/", {"firstName": "Ana"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Ana")

    def test_inactive_user_loses_access_with_same_token(self):
        access = self._access()
        self.user.status = RecordStatus.INACTIVE
        self.user.save()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = self.client.get("/api/auth/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
