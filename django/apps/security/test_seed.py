from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from apps.security.models import Resource, Role


class SeedRbacTests(TestCase):
    def test_seed_is_idempotent_and_uses_route_patterns(self):
        call_command("seed_rbac", stdout=StringIO())
        total = Resource.objects.count()
        call_command("seed_rbac", stdout=StringIO())
        self.assertEqual(Resource.objects.count(), total)
        self.assertTrue(Resource.objects.filter(route="api/clientes/<str:pk>/", method="PATCH").exists())
        self.assertTrue(Resource.objects.filter(route="api/ventas/<int:pk>/", method="DELETE").exists())
        self.assertEqual(Role.objects.get(name="admin").status, "active")
