from django.core.management.base import BaseCommand, CommandError
from django.urls import resolve

from apps.common.status import RecordStatus
from apps.security.models import Resource, ResourceRole, Role, RoleUser, User

ADMIN_ROLE = "admin"

MATRIZ = ["users", "roles", "role-users", "resources", "resource-roles"]
RECURSOS = [
    ("GET", "/api/clientes/"), ("POST", "/api/clientes/"),
    ("GET", "/api/clientes/1/"), ("PUT", "/api/clientes/1/"),
    ("PATCH", "/api/clientes/1/"), ("DELETE", "/api/clientes/1/"),
    ("GET", "/api/productos/"), ("POST", "/api/productos/"),
    ("GET", "/api/productos/1/"), ("PUT", "/api/productos/1/"),
    ("PATCH", "/api/productos/1/"), ("DELETE", "/api/productos/1/"),
    ("GET", "/api/productos/disponibles/"),
    ("GET", "/api/ventas/"), ("POST", "/api/ventas/"),
    ("GET", "/api/ventas/1/"), ("DELETE", "/api/ventas/1/"),
]
for _base in MATRIZ:
    RECURSOS += [
        ("GET", f"/api/{_base}/"), ("POST", f"/api/{_base}/"),
        ("GET", f"/api/{_base}/1/"), ("PUT", f"/api/{_base}/1/"),
        ("PATCH", f"/api/{_base}/1/"), ("DELETE", f"/api/{_base}/1/"),
    ]


class Command(BaseCommand):
    help = "Carga la matriz RBAC desde las rutas reales y concede todo al rol admin."

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Asigna el rol admin a este usuario.")

    def handle(self, *args, **options):
        role, _ = Role.objects.get_or_create(
            name=ADMIN_ROLE,
            defaults={"description": "Administrador", "status": RecordStatus.ACTIVE},
        )
        if role.status != RecordStatus.ACTIVE:
            role.status = RecordStatus.ACTIVE
            role.save(update_fields=["status", "updated_at"])

        nuevos = 0
        for method, sample in RECURSOS:
            route = resolve(sample).route
            resource, creado = Resource.objects.get_or_create(
                method=method,
                route=route,
                defaults={"name": f"{method} {route}", "status": RecordStatus.ACTIVE},
            )
            _grant, concedido = ResourceRole.objects.get_or_create(
                resource=resource,
                role=role,
                defaults={"status": RecordStatus.ACTIVE},
            )
            nuevos += int(creado) + int(concedido)

        if options["username"]:
            user = User.objects.filter(username=options["username"]).first()
            if user is None:
                raise CommandError(f"No existe el usuario {options['username']}.")
            RoleUser.objects.get_or_create(role=role, user=user, defaults={"status": RecordStatus.ACTIVE})

        self.stdout.write(f"Recursos RBAC sincronizados. Nuevos: {nuevos}.")
