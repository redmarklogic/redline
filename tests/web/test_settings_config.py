"""Unit tests for web.config.Settings (TDD Red -> Green, #161 Phase 1).

Each test controls exactly the environment it needs via monkeypatch.
pydantic.ValidationError is intentionally NOT imported to avoid the
project-wide TID251 ban; raises() uses the base Exception with a match.
"""

import pytest

# Minimal required env shared by multiple tests (everything except what the
# individual test deliberately omits or overrides).
_REQUIRED_ENV = {
    "DJANGO_SECRET_KEY": "test-key-that-is-not-the-burned-literal-abc123",
    "DJANGO_ALLOWED_HOSTS": "testserver,localhost",
    "POSTGRES_DB": "testdb",
    "POSTGRES_USER": "testuser",
    "POSTGRES_PASSWORD": "testpass",
    "POSTGRES_HOST": "127.0.0.1",
    "POSTGRES_PORT": "5432",
}


def _set_env(monkeypatch, overrides: dict | None = None, omit: set | None = None):
    """Apply _REQUIRED_ENV minus *omit*, then apply *overrides*."""
    env = dict(_REQUIRED_ENV)
    for key in omit or set():
        env.pop(key, None)
    env.update(overrides or {})
    for k, v in env.items():
        monkeypatch.setenv(k, v)


class TestSettingsConfig:
    """web.config.Settings validation behaviour."""

    def test_missing_secret_key_raises(self, monkeypatch):
        """DJANGO_SECRET_KEY unset -> ValidationError naming the field (FR-002, US2)."""
        _set_env(monkeypatch, omit={"DJANGO_SECRET_KEY"})

        with pytest.raises(Exception, match="django_secret_key"):
            from web.config import Settings  # noqa: PLC0415

            Settings()

    def test_missing_required_aggregates(self, monkeypatch):
        """Several required vars unset -> one ValidationError listing all (D1 aggregation)."""
        _set_env(
            monkeypatch,
            omit={"DJANGO_SECRET_KEY", "DJANGO_ALLOWED_HOSTS", "POSTGRES_DB"},
        )

        with pytest.raises(Exception) as exc_info:
            from web.config import Settings  # noqa: PLC0415

            Settings()

        error_text = str(exc_info.value)
        assert "django_secret_key" in error_text
        assert "django_allowed_hosts" in error_text
        assert "postgres_db" in error_text

    def test_debug_defaults_false(self, monkeypatch):
        """DJANGO_DEBUG unset, other required vars present -> django_debug is False (FR-003)."""
        _set_env(monkeypatch)
        monkeypatch.delenv("DJANGO_DEBUG", raising=False)

        from web.config import Settings  # noqa: PLC0415

        settings = Settings()
        assert settings.django_debug is False

    def test_wildcard_host_rejected(self, monkeypatch):
        """DJANGO_ALLOWED_HOSTS='*' -> ValidationError (FR-004, US3 scenario 2)."""
        _set_env(monkeypatch, overrides={"DJANGO_ALLOWED_HOSTS": "*"})

        with pytest.raises(Exception, match="wildcard"):
            from web.config import Settings  # noqa: PLC0415

            Settings()

    def test_allowed_hosts_comma_split(self, monkeypatch):
        """DJANGO_ALLOWED_HOSTS='localhost, example.com' -> ['localhost', 'example.com'] (D6)."""
        _set_env(
            monkeypatch,
            overrides={"DJANGO_ALLOWED_HOSTS": "localhost, example.com"},
        )

        from web.config import Settings  # noqa: PLC0415

        settings = Settings()
        assert settings.django_allowed_hosts == ["localhost", "example.com"]

    def test_debug_off_requires_host(self, monkeypatch):
        """DEBUG=False + DJANGO_ALLOWED_HOSTS='' -> ValidationError (FR-004 / RT-159 F-001)."""
        _set_env(
            monkeypatch,
            overrides={"DJANGO_DEBUG": "False", "DJANGO_ALLOWED_HOSTS": ""},
        )

        with pytest.raises(Exception, match="ALLOWED_HOSTS"):
            from web.config import Settings  # noqa: PLC0415

            Settings()

    def test_burned_secret_key_rejected(self, monkeypatch):
        """DJANGO_SECRET_KEY=<burned literal> -> ValidationError (FR-005, US4)."""
        burned = "django-insecure-ql2$-gjhyjwygz&@)uxs4(bba=5a&q5auyv^ka!vzwcbfo!h99"  # pragma: allowlist secret
        _set_env(monkeypatch, overrides={"DJANGO_SECRET_KEY": burned})

        with pytest.raises(Exception, match="burned"):
            from web.config import Settings  # noqa: PLC0415

            Settings()

    def test_fresh_secret_key_accepted(self, monkeypatch):
        """A key that is not the burned literal is accepted without error (FR-005)."""
        _set_env(
            monkeypatch,
            overrides={"DJANGO_SECRET_KEY": "a-completely-fresh-key-xyz-987654321"},
        )

        from web.config import Settings  # noqa: PLC0415

        settings = Settings()
        assert settings.django_secret_key == "a-completely-fresh-key-xyz-987654321"
