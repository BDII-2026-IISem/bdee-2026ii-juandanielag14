from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from apps.client.views import ClientViewSet
from apps.product.views import ProductoDisponibleListAPIView, ProductoViewSet
from apps.sale.views import VentaReadViewSet, VentaRegistroAPIView
from apps.security.auth_views import LoginAPIView, LogoutAPIView, RefreshAPIView
from apps.security.rbac_views import ProfileAPIView
from apps.security.matrix_views import ResourceRoleViewSet, ResourceViewSet, RoleUserViewSet, RoleViewSet, UserViewSet

router = SimpleRouter(use_regex_path=False)
router.register("clientes", ClientViewSet, basename="cliente")
router.register("productos", ProductoViewSet, basename="producto")
router.register("users", UserViewSet, basename="user")
router.register("roles", RoleViewSet, basename="role")
router.register("role-users", RoleUserViewSet, basename="role-user")
router.register("resources", ResourceViewSet, basename="resource")
router.register("resource-roles", ResourceRoleViewSet, basename="resource-role")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/auth/login/", LoginAPIView.as_view(), name="auth-login"),
    path("api/auth/refresh/", RefreshAPIView.as_view(), name="auth-refresh"),
    path("api/auth/logout/", LogoutAPIView.as_view(), name="auth-logout"),
    path("api/auth/profile/", ProfileAPIView.as_view(), name="auth-profile"),
    path("api/productos/disponibles/", ProductoDisponibleListAPIView.as_view(), name="producto-disponibles"),
    path("api/ventas/", VentaRegistroAPIView.as_view(), name="venta-registro"),
    path(
        "api/ventas/<int:pk>/",
        VentaReadViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="venta-detalle",
    ),
    path("api/", include(router.urls)),
]
