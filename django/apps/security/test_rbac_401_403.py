from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.status import RecordStatus
from apps.common.testing import create_active_user, grant
from apps.security.models import Resource, ResourceRole, Role, RoleUser


class RbacTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()

    def test_missing_grant_is_403_and_missing_identity_is_401(self):
        self.client.force_authenticate(user=self.user)
        denied = self.client.get("/api/clientes/")
        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=None)
        anonymous = self.client.get("/api/clientes/")
        self.assertEqual(anonymous.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_each_inactive_link_denies(self):
        role = grant(self.user, "GET", "/api/clientes/")
        self.client.force_authenticate(user=self.user)
        self.assertEqual(self.client.get("/api/clientes/").status_code, status.HTTP_200_OK)

        role_user = RoleUser.objects.get(role=role, user=self.user)
        resource_role = ResourceRole.objects.get(role=role)
        resource = Resource.objects.get(method="GET", route="api/clientes/")
        for link in (role, role_user, resource_role, resource):
            with self.subTest(link=type(link).__name__):
                link.status = RecordStatus.INACTIVE
                link.save(update_fields=["status", "updated_at"])
                self.assertEqual(self.client.get("/api/clientes/").status_code, status.HTTP_403_FORBIDDEN)
                link.status = RecordStatus.ACTIVE
                link.save(update_fields=["status", "updated_at"])
