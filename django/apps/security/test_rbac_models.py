from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import resolve

from apps.common.status import RecordStatus
from apps.security.models import Resource, ResourceRole, Role, RoleUser, User


class RbacModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", email="ana@ejemplo.com", password="ClaveSegura-2026")
        self.role = Role.objects.create(name="CAJA")
        self.resource = Resource.objects.create(name="Crear venta", method="POST", route="api/ventas/")

    def test_default_status_is_inactive(self):
        self.assertEqual(self.role.status, RecordStatus.INACTIVE)
        self.assertEqual(RoleUser.objects.create(role=self.role, user=self.user).status, RecordStatus.INACTIVE)

    def test_role_user_pair_is_unique(self):
        RoleUser.objects.create(role=self.role, user=self.user)
        with self.assertRaises(IntegrityError), transaction.atomic():
            RoleUser.objects.create(role=self.role, user=self.user)

    def test_method_and_route_are_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Resource.objects.create(name="Otra", method="POST", route="api/ventas/")

    def test_resource_role_pair_is_unique(self):
        ResourceRole.objects.create(resource=self.resource, role=self.role)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ResourceRole.objects.create(resource=self.resource, role=self.role)

    def test_route_pattern_comes_from_resolve(self):
        match = resolve("/api/clientes/1/")
        self.assertEqual(match.route, "api/clientes/<str:pk>/")
