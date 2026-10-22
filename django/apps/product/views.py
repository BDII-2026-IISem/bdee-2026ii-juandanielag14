from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.security.permissions import HasResourceAccess


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]

    def get_queryset(self):
        queryset = super().get_queryset()
        activo = self.request.query_params.get("is_active")
        if activo is not None:
            queryset = queryset.filter(is_active=activo.strip().lower() in {"1", "true", "yes", "on"})
        return queryset

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])


class ProductoDisponibleListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]

    @extend_schema(
        parameters=[OpenApiParameter("sucursal", int, required=True, description="ID de la sucursal")],
        responses=ProductSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        sucursal_id = self.request.query_params.get("sucursal")
        if not sucursal_id:
            raise ValidationError({"sucursal": "Este parámetro es obligatorio."})
        return Product.objects.filter(
            is_active=True,
            inventario__sucursal_id=sucursal_id,
            inventario__cantidad__gt=0,
        ).distinct()
