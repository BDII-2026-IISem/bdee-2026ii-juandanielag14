from django.urls import resolve
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.status import RecordStatus
from apps.common.testing import create_active_user
from apps.security.models import Resource, ResourceRole, Role, RoleUser
from apps.security.permissions import HasResourceAccess


class HasResourceAccessTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()
        self.role = Role.objects.create(name="CAJA", status=RecordStatus.ACTIVE)
        self.assignment = RoleUser.objects.create(role=self.role, user=self.user, status=RecordStatus.ACTIVE)
        self.resource = Resource.objects.create(
            name="Listar clientes", method="GET", route="api/clientes/", status=RecordStatus.ACTIVE
        )
        self.grant = ResourceRole.objects.create(
            resource=self.resource, role=self.role, status=RecordStatus.ACTIVE
        )

    def _allowed(self, user=None, method="get", path="/api/clientes/"):
        django_request = getattr(APIRequestFactory(), method)(path)
        request = Request(django_request)
        request.user = user if user is not None else self.user
        request.resolver_match = resolve(path)
        return HasResourceAccess().has_permission(request, None)

    def test_user_without_grant_is_denied(self):
        self.grant.delete()
        self.assertFalse(self._allowed())

    def test_anonymous_is_denied(self):
        from django.contrib.auth.models import AnonymousUser
        self.assertFalse(self._allowed(user=AnonymousUser()))

    def test_full_active_chain_is_allowed(self):
        self.assertTrue(self._allowed())

    def test_each_inactive_link_denies(self):
        for obj in (self.user, self.assignment, self.role, self.resource, self.grant):
            with self.subTest(link=type(obj).__name__):
                if type(obj).__name__ == "User":
                    obj.status = RecordStatus.INACTIVE
                    obj.save()
                else:
                    obj.status = RecordStatus.INACTIVE
                    obj.save(update_fields=["status", "updated_at"])
                self.assertFalse(self._allowed())
                obj.status = RecordStatus.ACTIVE
                if type(obj).__name__ == "User":
                    obj.save()
                else:
                    obj.save(update_fields=["status", "updated_at"])
