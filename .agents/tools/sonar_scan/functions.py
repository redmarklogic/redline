"""SonarQube scan orchestration glue (spec 014, Phase 4, D16).

Thin, unit-tested helpers behind the `sonar-scan` skill:

- `ensure_available(url)` — probes the local instance and RAISES a typed
  `SonarQubeUnavailableError` when it is unreachable or not UP. Never returns a
  sentinel or an empty result on failure (Constitution Principle X).
- `current_branch()` — the checked-out git branch the scan attributes issues to.
- `fetch_issues(...)` — retrieve open issues for a project/branch via the Web API.
  The official `mcp/sonarqube` MCP server is the primary retrieval path the skill
  uses; this glue is the typed, testable fallback (and the parity check in T024).
- `group_issues(...)` — group issues by file or severity for the triage display.

Conventions mirror `.agents/tools/github_projects`:
- subprocess always `shell=False`, arguments as a list (no shell interpolation);
- public functions return typed values or raise typed errors — no sentinel returns;
- the token is supplied by the caller (from untracked `.env`); this module never
  reads secrets from tracked files.
"""

import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from .schema import SonarIssue

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_STATUS_PATH = "/api/system/status"
_ISSUES_PATH = "/api/issues/search"
_MEASURES_PATH = "/api/measures/component"
_DEFAULT_TIMEOUT = 5.0
# Open work only: a finding marked FALSE-POSITIVE / WONTFIX moves to RESOLVED and
# is excluded here, so it is not re-surfaced on the next scan (FR-025).
_OPEN_STATUSES = ("OPEN", "CONFIRMED", "REOPENED")
_ISSUES_PAGE_SIZE = 500
# Standard pre-PR quality metrics.
DEFAULT_METRICS: tuple[str, ...] = (
    "coverage",
    "complexity",
    "cognitive_complexity",
    "duplicated_lines_density",
    "duplicated_blocks",
    "duplicated_lines",
    "ncloc",
    "lines",
    "statements",
    "bugs",
    "vulnerabilities",
    "code_smells",
    "security_hotspots",
)


# ---------------------------------------------------------------------------
# Typed errors (Constitution Principle X)
# ---------------------------------------------------------------------------


class SonarScanError(Exception):
    """Base class for sonar_scan failures."""


class SonarQubeUnavailableError(SonarScanError):
    """Raised when the local SonarQube instance cannot be reached or is not UP.

    Carries the probed URL and the underlying reason so the skill can surface
    actionable remediation (start the local stack) instead of failing silently
    or returning an empty issue set.
    """

    def __init__(self, url: str, *, reason: str) -> None:
        self.url = url
        self.reason = reason
        super().__init__(
            f"SonarQube is not available at {url}: {reason}. "
            "Start the local stack (redmark-sonarqube: ./infra/docker/setup.ps1 "
            "or `docker compose up -d`) and retry."
        )


# ---------------------------------------------------------------------------
# URL normalisation
# ---------------------------------------------------------------------------


def _normalise_url(url: str) -> str:
    """Rewrite host.docker.internal to localhost for host-side callers.

    SONARQUBE_URL in .env points to host.docker.internal so the MCP and scanner
    containers can reach the host-published port. Python callers run on the host
    and must use localhost instead; this rewrite is applied automatically so
    callers never need to know about the distinction.
    """
    return url.replace("host.docker.internal", "localhost")


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


def ensure_available(url: str, *, timeout: float = _DEFAULT_TIMEOUT) -> str:
    """Return the instance status when SonarQube is reachable and UP.

    Probes `GET {url}/api/system/status`. Raises `SonarQubeUnavailableError` when
    the instance cannot be reached, returns a non-JSON body, or reports a status
    other than UP. On success the return value is always the string "UP" — callers
    rely on the exception, never on a falsy return, to detect an unavailable
    instance.

    Args:
        url: Base URL of the instance, e.g. "http://localhost:9000".
        timeout: Socket timeout in seconds (bounded — never blocks indefinitely).
    """
    url = _normalise_url(url)
    status_url = url.rstrip("/") + _STATUS_PATH
    try:
        with urllib.request.urlopen(status_url, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SonarQubeUnavailableError(url, reason=str(exc)) from exc
    except json.JSONDecodeError as exc:
        raise SonarQubeUnavailableError(
            url, reason="status endpoint returned a non-JSON body"
        ) from exc

    status = payload.get("status")
    if status != "UP":
        raise SonarQubeUnavailableError(url, reason=f"status={status!r}")
    return status


# ---------------------------------------------------------------------------
# Git branch
# ---------------------------------------------------------------------------


def current_branch() -> str:
    """Return the checked-out git branch name.

    Raises `SonarScanError` if the branch cannot be determined (detached HEAD,
    not a git repo). Never returns an empty string.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    branch = result.stdout.strip()
    if result.returncode != 0 or not branch or branch == "HEAD":
        raise SonarScanError(
            "Could not determine the current git branch "
            f"(rc={result.returncode}): {result.stderr.strip() or branch!r}"
        )
    return branch


# ---------------------------------------------------------------------------
# Issue retrieval (Web-API glue / MCP parity check)
# ---------------------------------------------------------------------------


def fetch_issues(
    url: str,
    *,
    project: str,
    branch: str,
    token: str,
    timeout: float = _DEFAULT_TIMEOUT,
) -> list[SonarIssue]:
    """Return open issues for `project` on `branch` via the Web API.

    Calls `ensure_available(url)` first, so an unreachable instance raises
    `SonarQubeUnavailableError` rather than yielding an empty list (FR-024,
    Principle X). On success returns the parsed, typed issue list (possibly
    empty when the branch genuinely has no open issues). Only open work is
    returned (`_OPEN_STATUSES`), so a finding triaged as a false positive
    (moved to RESOLVED) is not re-surfaced.

    Args:
        url: Base instance URL, e.g. "http://localhost:9000".
        project: SonarQube project key, e.g. "redline".
        branch: Branch name to filter issues by.
        token: SonarQube user token (from untracked `.env`); sent as a bearer.
        timeout: Per-request socket timeout in seconds.
    """
    url = _normalise_url(url)
    ensure_available(url, timeout=timeout)
    query = urllib.parse.urlencode(
        {
            "componentKeys": project,
            "branch": branch,
            "statuses": ",".join(_OPEN_STATUSES),
            "ps": _ISSUES_PAGE_SIZE,
        }
    )
    request = urllib.request.Request(
        url.rstrip("/") + _ISSUES_PATH + "?" + query,
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SonarScanError(f"Issue search failed against {url}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SonarScanError(
            f"Issue search returned a non-JSON body from {url}"
        ) from exc

    return [_to_issue(raw) for raw in payload.get("issues", [])]


def _to_issue(raw: dict[str, object]) -> SonarIssue:
    """Map one raw `/api/issues/search` record to a typed SonarIssue."""
    return SonarIssue(
        key=str(raw.get("key", "")),
        rule=str(raw.get("rule", "")),
        severity=str(raw.get("severity", "")),
        component=str(raw.get("component", "")),
        line=raw.get("line") if isinstance(raw.get("line"), int) else None,
        message=str(raw.get("message", "")),
        status=str(raw.get("status", "")),
    )


# ---------------------------------------------------------------------------
# Metrics retrieval
# ---------------------------------------------------------------------------


def fetch_metrics(  # noqa: PLR0913
    url: str,
    *,
    project: str,
    branch: str,
    token: str,
    metrics: tuple[str, ...] = DEFAULT_METRICS,
    timeout: float = _DEFAULT_TIMEOUT,
) -> dict[str, float]:
    """Return quality metrics for `project` on `branch` as a float dict.

    Calls `ensure_available(url)` first — an unreachable instance raises
    `SonarQubeUnavailableError` rather than returning empty results. Only
    metrics present in the API response are included in the return value.

    Args:
        url: Base instance URL, e.g. "http://localhost:9000".
        project: SonarQube project key.
        branch: Branch name to filter metrics by.
        token: SonarQube user token (from untracked `.env`).
        metrics: Metric keys to fetch; defaults to `DEFAULT_METRICS`.
        timeout: Per-request socket timeout in seconds.
    """
    url = _normalise_url(url)
    ensure_available(url, timeout=timeout)
    query = urllib.parse.urlencode(
        {
            "component": project,
            "branch": branch,
            "metricKeys": ",".join(metrics),
        }
    )
    request = urllib.request.Request(
        url.rstrip("/") + _MEASURES_PATH + "?" + query,
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SonarScanError(f"Metrics fetch failed against {url}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SonarScanError(
            f"Metrics fetch returned a non-JSON body from {url}"
        ) from exc

    return {
        m["metric"]: float(m["value"])
        for m in payload.get("component", {}).get("measures", [])
        if "value" in m
    }


# ---------------------------------------------------------------------------
# Grouping for triage
# ---------------------------------------------------------------------------


def group_issues(
    issues: list[SonarIssue], *, by: str = "file"
) -> dict[str, list[SonarIssue]]:
    """Group issues for the triage display.

    Args:
        issues: Issues to group.
        by: "file" (group on `file_path`) or "severity".

    Raises:
        SonarScanError: if `by` is not "file" or "severity".
    """
    if by == "file":
        key = lambda issue: issue.file_path  # noqa: E731
    elif by == "severity":
        key = lambda issue: issue.severity  # noqa: E731
    else:
        raise SonarScanError(f"group_issues: unknown grouping {by!r}")

    grouped: dict[str, list[SonarIssue]] = {}
    for issue in issues:
        grouped.setdefault(key(issue), []).append(issue)
    return grouped
