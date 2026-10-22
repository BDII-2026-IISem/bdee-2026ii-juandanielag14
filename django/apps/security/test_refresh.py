import hashlib
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.common.status import RecordStatus
from apps.security.models import RefreshToken, User
from apps.security.tokens import generate_refresh_value, hash_token


class RefreshTokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ana",
            email="ana@ejemplo.com",
            password="ClaveSegura-2026",
            status=RecordStatus.ACTIVE,
        )

    def _crear(self, raw, **extra):
        return RefreshToken.objects.create(
            user=self.user,
            token_hash=hash_token(raw),
            expires_at=RefreshToken.default_expiry(),
            **extra,
        )

    def test_stored_hash_is_not_the_raw_token(self):
        raw = generate_refresh_value()
        token = self._crear(raw)
        self.assertNotEqual(token.token_hash, raw)
        self.assertNotIn(raw, token.token_hash)

    def test_hash_matches_sha256(self):
        raw = generate_refresh_value()
        token = self._crear(raw)
        self.assertEqual(token.token_hash, hashlib.sha256(raw.encode("utf-8")).hexdigest())

    def test_revoked_or_expired_token_is_not_usable(self):
        revocado = self._crear(generate_refresh_value(), revoked_at=timezone.now())
        expirado = RefreshToken.objects.create(
            user=self.user,
            token_hash=hash_token(generate_refresh_value()),
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        self.assertFalse(revocado.is_usable)
        self.assertFalse(expirado.is_usable)
