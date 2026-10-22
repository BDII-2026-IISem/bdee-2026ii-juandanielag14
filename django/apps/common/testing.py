from django.urls import resolve
from apps.common.status import RecordStatus
from apps.security.models import Resource, ResourceRole, Role, RoleUser, User

PASSWORD = "PuntoStock-Test-1"


def create_active_user(username="ana", email="ana@puntostock.test", password=PASSWORD):
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        status=RecordStatus.ACTIVE,
    )


def grant(user, method, path):
    match = resolve(path)
    role, _ = Role.objects.get_or_create(
        name=f"rol-prueba-{user.pk}",
        defaults={"description": "Rol de prueba", "status": RecordStatus.ACTIVE},
    )
    RoleUser.objects.get_or_create(role=role, user=user, defaults={"status": RecordStatus.ACTIVE})
    resource, _ = Resource.objects.get_or_create(
        method=method.upper(),
        route=match.route,
        defaults={"name": f"{method.upper()} {match.route}", "status": RecordStatus.ACTIVE},
    )
    ResourceRole.objects.get_or_create(resource=resource, role=role, defaults={"status": RecordStatus.ACTIVE})
    return role


def grant_crud(user, collection, detail):
    for method in ("GET", "POST"):
        grant(user, method, collection)
    for method in ("GET", "PUT", "PATCH", "DELETE"):
        grant(user, method, detail)


def grant_business(user):
    grant_crud(user, "/api/clientes/", "/api/clientes/1/")
    grant_crud(user, "/api/productos/", "/api/productos/1/")
    grant(user, "GET", "/api/productos/disponibles/")
    grant(user, "GET", "/api/ventas/")
    grant(user, "POST", "/api/ventas/")
    grant(user, "GET", "/api/ventas/1/")
    grant(user, "DELETE", "/api/ventas/1/")
