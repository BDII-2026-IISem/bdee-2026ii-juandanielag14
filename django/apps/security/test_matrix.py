from rest_framework import status
from rest_framework.test import APITestCase

from apps.common.status import RecordStatus
from apps.common.testing import PASSWORD, create_active_user, grant_crud
from apps.security.models import User


class SecurityMatrixApiTests(APITestCase):
    def setUp(self):
        self.admin = create_active_user(username="admin", email="admin@puntostock.test")
        for collection, detail in (
            ("/api/users/", "/api/users/1/"),
            ("/api/roles/", "/api/roles/1/"),
            ("/api/role-users/", "/api/role-users/1/"),
            ("/api/resources/", "/api/resources/1/"),
            ("/api/resource-roles/", "/api/resource-roles/1/"),
        ):
            grant_crud(self.admin, collection, detail)
        self.client.force_authenticate(user=self.admin)

    def test_role_crud_and_soft_delete(self):
        created = self.client.post("/api/roles/", {"name": "caja", "status": "active"}, format="json")
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        role_id = created.data["id"]
        self.assertEqual(self.client.get(f"/api/roles/{role_id}/").status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(f"/api/roles/{role_id}/").status_code, status.HTTP_204_NO_CONTENT)
        from apps.security.models import Role
        self.assertEqual(Role.objects.get(pk=role_id).status, RecordStatus.INACTIVE)

    def test_user_role_resource_chain_controls_access(self):
        role = self.client.post("/api/roles/", {"name": "bodega", "status": "active"}, format="json").data
        user = self.client.post(
            "/api/users/",
            {"username": "bodega1", "email": "bodega1@puntostock.test", "password": PASSWORD, "status": "active"},
            format="json",
        )
        self.assertEqual(user.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", user.data)
        stored = User.objects.get(pk=user.data["id"])
        self.assertNotEqual(stored.password, PASSWORD)
        self.assertTrue(stored.check_password(PASSWORD))

        self.client.force_authenticate(user=stored)
        self.assertEqual(self.client.get("/api/clientes/").status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        self.client.post(
            "/api/role-users/",
            {"role": role["id"], "user": stored.pk, "status": "active"},
            format="json",
        )
        self.client.force_authenticate(user=stored)
        self.assertEqual(self.client.get("/api/clientes/").status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        resource = self.client.post(
            "/api/resources/",
            {"name": "Listar clientes", "method": "GET", "route": "api/clientes/", "status": "active"},
            format="json",
        ).data
        self.client.force_authenticate(user=stored)
        self.assertEqual(self.client.get("/api/clientes/").status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        self.client.post(
            "/api/resource-roles/",
            {"resource": resource["id"], "role": role["id"], "status": "active"},
            format="json",
        )
        self.client.force_authenticate(user=stored)
        self.assertEqual(self.client.get("/api/clientes/").status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post("/api/clientes/", {}, format="json").status_code, status.HTTP_403_FORBIDDEN)
