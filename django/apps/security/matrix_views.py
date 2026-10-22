from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.status import RecordStatus
from apps.security.matrix_serializers import (
    ResourceRoleSerializer,
    ResourceSerializer,
    RoleSerializer,
    RoleUserSerializer,
    UserSerializer,
)
from apps.security.models import Resource, ResourceRole, Role, RoleUser, User
from apps.security.permissions import HasResourceAccess


class MatrixViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasResourceAccess]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param.strip().lower())
        return queryset

    def perform_destroy(self, instance):
        instance.status = RecordStatus.INACTIVE
        instance.save(update_fields=["status", "updated_at"])


class UserViewSet(MatrixViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        instance.status = RecordStatus.INACTIVE
        instance.save()


class RoleViewSet(MatrixViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleUserViewSet(MatrixViewSet):
    queryset = RoleUser.objects.select_related("role", "user")
    serializer_class = RoleUserSerializer


class ResourceViewSet(MatrixViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ResourceRoleViewSet(MatrixViewSet):
    queryset = ResourceRole.objects.select_related("resource", "role")
    serializer_class = ResourceRoleSerializer
