"""12-factor configuration schema for the web application.

Reads every environment-varying value from the process environment through a
single pydantic-settings Settings class. No .env file is loaded here — that
is the shell/dev-tooling responsibility (ADR-021).
"""

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# The burned key is committed in git history and in already-built images; it
# must never be reused. The constant is the rejection target, not a live
# credential. pragma suppresses detect-secrets false-positive (FR-005).
_BURNED_SECRET_KEY = (  # pragma: allowlist secret
    "django-insecure-ql2$-gjhyjwygz&@)uxs4(bba=5a&q5auyv^ka!vzwcbfo!h99"
)


class Settings(BaseSettings):
    """Environment-driven configuration for the Django web application.

    All fields with no default are required; absence raises pydantic
    ValidationError at import time, preventing a misconfigured process from
    starting silently (ADR-021, FR-002).
    """

    model_config = SettingsConfigDict(env_file=None, enable_decoding=False)

    # --- Django core ---
    django_secret_key: str
    django_debug: bool = False
    django_allowed_hosts: list[str]

    # --- PostgreSQL ---
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    # --- Transport security (default-off, risk-accepted for staging; FR-007 / D7) ---
    django_secure_ssl_redirect: bool = False
    django_secure_hsts_seconds: int = 0
    django_session_cookie_secure: bool = False
    django_csrf_cookie_secure: bool = False

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @field_validator("django_allowed_hosts", mode="before")
    @classmethod
    def _split_and_validate_hosts(cls, value: object) -> list[str]:
        """Split comma-separated host string; reject wildcard entries (FR-004)."""
        if isinstance(value, str):
            hosts = [h.strip() for h in value.split(",") if h.strip()]
        elif isinstance(value, list):
            hosts = [str(h).strip() for h in value if str(h).strip()]
        else:
            hosts = []

        if "*" in hosts:
            msg = "wildcard '*' is not a permitted value for DJANGO_ALLOWED_HOSTS (FR-004)"
            raise ValueError(msg)

        return hosts

    @field_validator("django_secret_key", mode="after")
    @classmethod
    def _reject_burned_key(cls, value: str) -> str:
        """Reject the committed burned literal (FR-005 / RT-159 F-008)."""
        if value == _BURNED_SECRET_KEY:
            msg = (
                "DJANGO_SECRET_KEY equals the burned django-insecure- literal committed "
                "in git history. Generate a fresh key and inject it from Secret Manager "
                "(ADR-023)."
            )
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def _require_hosts_when_debug_off(self) -> Settings:
        """Require at least one ALLOWED_HOST when DEBUG is False (FR-004 / RT-159 F-001).

        An empty ALLOWED_HOSTS with DEBUG=False causes every request — including
        the Cloud Run startup probe — to return 400 Bad Request.
        """
        if not self.django_debug and not self.django_allowed_hosts:
            msg = (
                "ALLOWED_HOSTS must contain at least one hostname when DEBUG is False. "
                "An empty list causes every request (including the deploy probe) to "
                "return 400 Bad Request."
            )
            raise ValueError(msg)
        return self
