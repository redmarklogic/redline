"""SonarQube scan orchestration tool — typed availability check + issue glue.

Backs the `sonar-scan` skill (spec 014, Phase 4). Mirrors the package layout of
`.agents/tools/github_projects`: typed schema + thin function surface, errors
raised never sentinelled.
"""

from .functions import (
    DEFAULT_METRICS,
    SonarQubeUnavailableError,
    SonarScanError,
    current_branch,
    ensure_available,
    fetch_issues,
    fetch_metrics,
    group_issues,
)
from .schema import SonarIssue

__all__ = [
    "DEFAULT_METRICS",
    "SonarIssue",
    "SonarQubeUnavailableError",
    "SonarScanError",
    "current_branch",
    "ensure_available",
    "fetch_issues",
    "fetch_metrics",
    "group_issues",
]
