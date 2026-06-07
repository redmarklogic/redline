"""CLI-free SonarQube availability probe shared by scan.ps1 / scan.sh.

Single source of truth for the pre-flight check: delegates to ``ensure_available``
so the scan scripts and the review tool agree on what "available" means. The
instance URL is read from the environment (configured by the caller, per
AGENTS.md); the process exits 0 when the instance is UP and 1 with remediation
otherwise.

Run: ``PYTHONPATH=.agents/tools uv run python -m sonar_scan.healthcheck``
"""

import os
import sys

from .functions import SonarQubeUnavailableError, ensure_available


def main() -> int:
    """Probe the configured instance and return a process exit code.

    Returns:
        0 if SonarQube is reachable and UP; 1 if no URL is configured or the
        instance is unavailable (remediation is printed to stderr).
    """
    url = os.environ.get("SONARQUBE_URL") or os.environ.get("SONAR_HOST_URL")
    if not url:
        print(
            "ERROR: set SONARQUBE_URL or SONAR_HOST_URL before the health check "
            "(the environment is configured by the caller).",
            file=sys.stderr,
        )
        return 1
    try:
        ensure_available(url)
    except SonarQubeUnavailableError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
