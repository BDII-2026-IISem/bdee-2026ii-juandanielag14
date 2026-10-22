import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from apps.common.status import RecordStatus
from apps.security.models import RefreshToken
from apps.security.serializers import LoginSerializer, RefreshSerializer, TokenPairSerializer
from apps.security.tokens import generate_refresh_value, hash_token

User = get_user_model()


def token_payload(user, raw_refresh):
    access = AccessToken.for_user(user)
    lifetime = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    return {
        "access": str(access),
        "refresh": raw_refresh,
        "token_type": "Bearer",
        "access_expires_in": lifetime,
    }


def issue_refresh(user, family_id=None):
    raw_refresh = generate_refresh_value()
    stored = RefreshToken.objects.create(
        user=user,
        token_hash=hash_token(raw_refresh),
        family_id=family_id or uuid.uuid4(),
        expires_at=RefreshToken.default_expiry(),
        status=RecordStatus.ACTIVE,
    )
    return stored, raw_refresh


def _find_user(username, email):
    if username:
        return User.objects.filter(username=username).first()
    return User.objects.filter(email__iexact=email).first()


def _unauthorized(detail="Credenciales inválidas."):
    return Response({"detail": detail}, status=status.HTTP_401_UNAUTHORIZED)


def _revoke_family(family_id):
    now = timezone.now()
    RefreshToken.objects.filter(family_id=family_id).update(
        status=RecordStatus.INACTIVE,
        revoked_at=now,
        updated_at=now,
    )


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: TokenPairSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = _find_user(data.get("username"), data.get("email"))
        if user is None or user.status != RecordStatus.ACTIVE or not user.check_password(data["password"]):
            return _unauthorized()
        _stored, raw_refresh = issue_refresh(user)
        return Response(token_payload(user, raw_refresh), status=status.HTTP_200_OK)


class RefreshAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(request=RefreshSerializer, responses={200: TokenPairSerializer})
    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw = serializer.validated_data["refresh"]
        with transaction.atomic():
            token = (
                RefreshToken.objects.select_for_update()
                .select_related("user")
                .filter(token_hash=hash_token(raw))
                .first()
            )
            if token is None:
                return _unauthorized()
            if token.replaced_by_id is not None or token.revoked_at is not None:
                _revoke_family(token.family_id)
                return _unauthorized("Refresh reutilizado. Inicie sesión de nuevo.")
            if token.expires_at <= timezone.now() or token.user.status != RecordStatus.ACTIVE:
                token.status = RecordStatus.INACTIVE
                token.save(update_fields=["status", "updated_at"])
                return _unauthorized()
            nuevo, raw_nuevo = issue_refresh(token.user, family_id=token.family_id)
            token.replaced_by = nuevo
            token.status = RecordStatus.INACTIVE
            token.save(update_fields=["replaced_by", "status", "updated_at"])
            return Response(token_payload(token.user, raw_nuevo), status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(request=RefreshSerializer, responses={204: None, 401: None})
    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw = serializer.validated_data["refresh"]
        with transaction.atomic():
            token = (
                RefreshToken.objects.select_for_update()
                .filter(token_hash=hash_token(raw))
                .first()
            )
            if token is None:
                return _unauthorized()
            if token.replaced_by_id is not None:
                _revoke_family(token.family_id)
                return _unauthorized("Refresh reutilizado. Inicie sesión de nuevo.")
            token.status = RecordStatus.INACTIVE
            token.revoked_at = timezone.now()
            token.save(update_fields=["status", "revoked_at", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)
