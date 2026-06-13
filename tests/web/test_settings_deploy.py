"""Regression pin: deployment configuration check (#161 Phase 3, T016).

Asserts that a production-like environment produces zero warnings in the
three resolved check classes (W009 / W018 / W020) and documents the four
risk-accepted transport-security warnings (W004 / W008 / W012 / W016) as
accepted-not-silenced (research.md D7/D8).

This is a characterization pin, not a Red test — the three target warnings
are already resolved by Phase 2. The transport-security checks remain as
warnings because the defaults are off; they are documented here in executable
form so no warning is silently ignored.
"""

import django
from django.test import override_settings

# Production-like values — real key (not the burned literal), DEBUG off,
# explicit host. Transport settings left at their defaults (off/0/False) to
# document the risk-accepted state.
_PROD_LIKE = {
    "SECRET_KEY": "production-like-key-not-burned-literal-xyz-987654321-abc",  # pragma: allowlist secret
    "DEBUG": False,
    "ALLOWED_HOSTS": ["example.com"],
    "SECURE_SSL_REDIRECT": False,
    "SECURE_HSTS_SECONDS": 0,
    "SESSION_COOKIE_SECURE": False,
    "CSRF_COOKIE_SECURE": False,
}

# IDs resolved outright by this slice (FR-007).
_RESOLVED_IDS = {"security.W009", "security.W018", "security.W020"}

# IDs risk-accepted (D7/D8): transport-security, default-off for staging.
# Enabled per environment at #177. Listed here so their presence is asserted
# (accepted-not-silenced), documenting that no warning is undocumented.
_RISK_ACCEPTED_IDS = {
    "security.W004",
    "security.W008",
    "security.W012",
    "security.W016",
}


def test_deploy_check_resolved_warnings_absent():
    """Resolved check classes W009/W018/W020 absent in production-like env (FR-007)."""
    with override_settings(**_PROD_LIKE):
        django.setup()
        from django.core.checks import run_checks

        messages = run_checks(include_deployment_checks=True)

    present_ids = {m.id for m in messages}
    resolved_still_present = _RESOLVED_IDS & present_ids
    assert not resolved_still_present, (
        f"Expected resolved check IDs to be absent but found: {resolved_still_present}. "
        "The following warnings should have been fixed by #161 Phase 2."
    )


def test_deploy_check_risk_accepted_warnings_present():
    """Risk-accepted transport warnings W004/W008/W012/W016 remain (accepted-not-silenced).

    These warnings are documented in research.md D7/D8 with rationale. Their
    presence is asserted here so that silencing them (e.g. by setting the
    transport flags on unexpectedly) would break this test, making the change
    visible and deliberate.
    """
    with override_settings(**_PROD_LIKE):
        django.setup()
        from django.core.checks import run_checks

        messages = run_checks(include_deployment_checks=True)

    present_ids = {m.id for m in messages}
    missing_accepted = _RISK_ACCEPTED_IDS - present_ids
    assert not missing_accepted, (
        f"Expected risk-accepted transport warning IDs to be present but they are absent: "
        f"{missing_accepted}. If transport security was enabled, update the risk-acceptance "
        "record in research.md D7/D8 and move the IDs to _RESOLVED_IDS."
    )
