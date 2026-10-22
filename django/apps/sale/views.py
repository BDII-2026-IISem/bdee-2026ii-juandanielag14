from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.sale.models import Venta
from apps.sale.serializers import VentaRegistroSerializer, VentaSerializer
from apps.security.permissions import HasResourceAccess


def _ventas_con_lineas():
    return Venta.objects.select_related("cliente", "sucursal").prefetch_related("detalles__producto")


class VentaRegistroAPIView(APIView):
    permission_classes = [IsAuthenticated, HasResourceAccess]

    @extend_schema(responses=VentaSerializer(many=True))
    def get(self, request):
        return Response(VentaSerializer(_ventas_con_lineas(), many=True).data)

    @extend_schema(request=VentaRegistroSerializer, responses={201: VentaSerializer})
    def post(self, request):
        serializer = VentaRegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        venta = serializer.save()
        return Response(VentaSerializer(venta).data, status=status.HTTP_201_CREATED)


class VentaReadViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = _ventas_con_lineas()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]

    def perform_destroy(self, instance):
        instance.void()
