"""Offline acceptance tests for the SonarQube skill entry points.

Acceptance criteria — when SonarQube is unreachable ALL of these must hold:
  - Exit code is 1 (never 0 / silent pass).
  - stderr contains the SonarQubeUnavailableError message.
  - stderr contains remediation text pointing to `docker compose up -d`.
  - Execution stops before scanning or retrieving issues.

Port 19999 is used as a guaranteed-closed URL so these tests are
Docker-state-independent and safe to run in CI.

scan.ps1 offline behaviour is transitively verified: the script delegates its
availability gate to `sonar_scan.healthcheck` (scan.ps1 line 51), so
TestHealthcheckCliOffline covers it. No automated scan.ps1 test is included
because scan.ps1 also triggers a full Docker-based scan when Docker IS online.
"""

import os
import subprocess
from pathlib import Path

import pytest
from sonar_scan import UNAVAILABLE_REMEDIATION

_REPO_ROOT = Path(__file__).parents[4]
_OFFLINE_URL = "http://localhost:19999"
_MSG_UNAVAILABLE = "SonarQube is not available"
_MSG_REMEDIATION = UNAVAILABLE_REMEDIATION


def _env_offline() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("SONARQUBE_URL", None)
    env.pop("SONAR_HOST_URL", None)
    env["SONARQUBE_URL"] = _OFFLINE_URL
    env["PYTHONPATH"] = str(_REPO_ROOT / ".agents" / "tools")
    return env


# ---------------------------------------------------------------------------
# 1. sonar_scan.healthcheck CLI
#    Used by scan.ps1 as its availability gate (scan.ps1 line 51).
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def healthcheck_offline() -> subprocess.CompletedProcess:
    return subprocess.run(
        ["uv", "run", "python", "-m", "sonar_scan.healthcheck"],
        cwd=_REPO_ROOT,
        env=_env_offline(),
        capture_output=True,
        text=True,
    )


class TestHealthcheckCliOffline:
    """healthcheck exits 1 + remediation when SonarQube unreachable."""

    def test_exit_code(self, healthcheck_offline: subprocess.CompletedProcess) -> None:
        assert healthcheck_offline.returncode == 1

    def test_stderr_unavailable_message(
        self, healthcheck_offline: subprocess.CompletedProcess
    ) -> None:
        assert _MSG_UNAVAILABLE in healthcheck_offline.stderr

    def test_stderr_remediation(
        self, healthcheck_offline: subprocess.CompletedProcess
    ) -> None:
        assert _MSG_REMEDIATION in healthcheck_offline.stderr


# ---------------------------------------------------------------------------
# 2. sonarqube-review Step 0 (Python entry point)
#    Mirrors the procedure's Step 0 snippet exactly.
# ---------------------------------------------------------------------------

_REVIEW_STEP0_SCRIPT = """
import os
from sonar_scan import SonarQubeUnavailableError, ensure_available
url = os.environ["SONARQUBE_URL"]
try:
    ensure_available(url)
except SonarQubeUnavailableError as exc:
    raise SystemExit(str(exc)) from None
print("REACHED: should not get here")
"""


@pytest.fixture(scope="module")
def review_step0_offline() -> subprocess.CompletedProcess:
    return subprocess.run(
        ["uv", "run", "python", "-c", _REVIEW_STEP0_SCRIPT],
        cwd=_REPO_ROOT,
        env=_env_offline(),
        capture_output=True,
        text=True,
    )


class TestReviewStep0Offline:
    """review Step 0 exits 1 + remediation when SonarQube unreachable."""

    def test_exit_code(self, review_step0_offline: subprocess.CompletedProcess) -> None:
        assert review_step0_offline.returncode == 1

    def test_stderr_unavailable_message(
        self, review_step0_offline: subprocess.CompletedProcess
    ) -> None:
        assert _MSG_UNAVAILABLE in review_step0_offline.stderr

    def test_stderr_remediation(
        self, review_step0_offline: subprocess.CompletedProcess
    ) -> None:
        assert _MSG_REMEDIATION in review_step0_offline.stderr

    def test_does_not_reach_issue_retrieval(
        self, review_step0_offline: subprocess.CompletedProcess
    ) -> None:
        assert "REACHED" not in review_step0_offline.stdout
