"""
TDD tests for agent JD routing table correctness.

RED → GREEN cycle for items identified in Phase 1 skill-bloat audit:
  - notebooklm-index must be in Linda's routing table
  - notebooklm-deep-research must be in Linda's routing table
  - ceremony-monthly-editorial-session must be in John's routing table
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / ".github" / "agents"
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

_BACKTICK_RE = re.compile(r"`([^`\n]+)`")


def _skills_in_routing_table(agent_file: Path, known_skills: set[str]) -> set[str]:
    """Return the set of known skill names backtick-referenced in *agent_file*."""
    content = agent_file.read_text(encoding="utf-8")
    return {t for t in _BACKTICK_RE.findall(content) if t in known_skills}


@pytest.fixture(scope="module")
def known_skills() -> set[str]:
    return {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}


@pytest.fixture(scope="module")
def linda_jd() -> Path:
    return AGENTS_DIR / "rl.linda.agent.md"


@pytest.fixture(scope="module")
def john_jd() -> Path:
    return AGENTS_DIR / "rl.john.agent.md"


# ---------------------------------------------------------------------------
# Linda routing table
# ---------------------------------------------------------------------------


def test_linda_routes_notebooklm_index(linda_jd: Path, known_skills: set[str]) -> None:
    """notebooklm-index must appear in Linda's routing table.

    Linda maintains index-notebooklm.xlsx — this is her skill.
    Identified as orphan in Phase 1 graph audit (2026-05-31).
    """
    routed = _skills_in_routing_table(linda_jd, known_skills)
    assert "notebooklm-index" in routed, (
        "notebooklm-index is not in Linda's routing table. "
        "Add it under 'Skills Available to Linda'."
    )


def test_linda_routes_notebooklm_deep_research(
    linda_jd: Path, known_skills: set[str]
) -> None:
    """notebooklm-deep-research must appear in Linda's routing table.

    Linda is the keeper of notebook infrastructure — deep research
    sessions that produce new notebooks are her operational concern.
    Assigned to Linda per founder decision 2026-05-31.
    """
    routed = _skills_in_routing_table(linda_jd, known_skills)
    assert "notebooklm-deep-research" in routed, (
        "notebooklm-deep-research is not in Linda's routing table. "
        "Add it under 'Skills Available to Linda'."
    )


# ---------------------------------------------------------------------------
# John routing table
# ---------------------------------------------------------------------------


def test_john_routes_ceremony_monthly_editorial_session(
    john_jd: Path, known_skills: set[str]
) -> None:
    """ceremony-monthly-editorial-session must appear in John's routing table.

    The skill processes Ground Engineering magazine issues for content and
    product signals, producing editorial calendar entries — squarely John's domain.
    Identified as orphan in Phase 1 graph audit; routed to John per founder
    decision 2026-05-31.
    """
    routed = _skills_in_routing_table(john_jd, known_skills)
    assert "ceremony-monthly-editorial-session" in routed, (
        "ceremony-monthly-editorial-session is not in John's routing table. "
        "Add it under 'Skills Available to John'."
    )
