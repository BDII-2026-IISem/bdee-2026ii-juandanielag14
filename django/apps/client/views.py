from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.client.models import Client
from apps.client.serializers import ClientSerializer
from apps.security.permissions import HasResourceAccess


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
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
