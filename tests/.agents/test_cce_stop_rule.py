"""
TDD: CCE enforcement via SubagentStart hook + slim JDs.

Session 84e79a61 proved the approach works:
  - 3 tool calls (tool_search, session_recall, context_search)
  - 0 read_file calls
  - 46K input tokens (down from 505K)
  - Information query budget respected

Architecture: cce-inject.ps1 hook carries enforcement rules (Stop Rule,
semantic_search ban, info query budget). JDs reference CCE in one slim
bullet. mcp-cce skill documents the concept concisely.

Layers:
  A. JDs reference CCE in one slim bullet (not verbose paragraphs)
  B. AGENTS.md subagent dispatch rule (no prescribed discovery)
  C. SubagentStart hook carries Stop Rule, semantic_search ban, info budget
  D. mcp-cce skill has Stop Rule essentials
  E. Mark has information query budget reference
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / ".github" / "agents"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
CCE_SKILL = REPO_ROOT / ".agents" / "skills" / "mcp-cce" / "SKILL.md"
CCE_HOOK = REPO_ROOT / ".github" / "hooks" / "cce-inject.ps1"
MARK_JD = AGENTS_DIR / "rl.mark.agent.md"

AGENT_JDS = sorted(AGENTS_DIR.glob("rl.*.agent.md"))


def _extract_section(content: str, heading: str) -> str:
    """Extract text between a ## heading and the next ## heading."""
    pattern = rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1) if match else ""


@pytest.fixture(scope="module", params=[p.name for p in AGENT_JDS], ids=lambda n: n)
def agent_jd(request: pytest.FixtureRequest) -> Path:
    return AGENTS_DIR / request.param


# ---------------------------------------------------------------------------
# Layer A: JDs reference CCE in one slim bullet (not bloated)
# ---------------------------------------------------------------------------


def test_agent_jd_has_cce_reference(agent_jd: Path) -> None:
    """Every agent JD must reference CCE in Session Discipline."""
    section = _extract_section(
        agent_jd.read_text(encoding="utf-8"), "Session Discipline"
    )
    assert "CCE" in section, f"{agent_jd.name}: Session Discipline must reference CCE."


def test_agent_jd_cce_is_slim(agent_jd: Path) -> None:
    """Session Discipline must have at most 1 CCE bullet.

    CCE enforcement lives in cce-inject.ps1 SubagentStart hook, not in JDs.
    JDs carry a brief reference; the hook carries the detailed rules.
    """
    section = _extract_section(
        agent_jd.read_text(encoding="utf-8"), "Session Discipline"
    )
    cce_bullets = [
        line for line in section.split("\n") if line.strip().startswith("- **CCE")
    ]
    assert len(cce_bullets) <= 1, (
        f"{agent_jd.name}: has {len(cce_bullets)} CCE bullets in Session Discipline "
        f"(max 1). Move enforcement to cce-inject.ps1 hook."
    )


# ---------------------------------------------------------------------------
# Layer B: AGENTS.md subagent dispatch rule
# ---------------------------------------------------------------------------


def test_agents_md_has_subagent_dispatch_rule() -> None:
    """AGENTS.md must instruct the default agent NOT to prescribe discovery
    methods when invoking named agents."""
    content = AGENTS_MD.read_text(encoding="utf-8")
    assert "Subagent Dispatch" in content


def test_agents_md_dispatch_rule_prohibits_prescribing_discovery() -> None:
    """The dispatch rule must explicitly prohibit prescribing discovery methods."""
    content = AGENTS_MD.read_text(encoding="utf-8")
    assert re.search(
        r"(do not|never|must not).*(prescrib|direct|instruct).*(director|file|read|examine)",
        content,
        re.IGNORECASE,
    )


# ---------------------------------------------------------------------------
# Layer C: SubagentStart hook carries CCE enforcement
# ---------------------------------------------------------------------------


def test_hook_has_stop_rule() -> None:
    """cce-inject.ps1 must carry the Stop Rule so JDs don't need to."""
    content = CCE_HOOK.read_text(encoding="utf-8")
    assert re.search(r"stop.rule", content, re.IGNORECASE), (
        "cce-inject.ps1 must contain Stop Rule enforcement."
    )


def test_hook_bans_semantic_search() -> None:
    """cce-inject.ps1 must ban semantic_search for workspace exploration."""
    content = CCE_HOOK.read_text(encoding="utf-8")
    assert re.search(
        r"(do not|never|don.t).*semantic_search",
        content,
        re.IGNORECASE,
    ), "cce-inject.ps1 must ban semantic_search."


def test_hook_has_info_query_guidance() -> None:
    """cce-inject.ps1 must include information query budget guidance."""
    content = CCE_HOOK.read_text(encoding="utf-8")
    assert re.search(
        r"information.query|status.check|priorit",
        content,
        re.IGNORECASE,
    ), "cce-inject.ps1 must include information query budget guidance."


# ---------------------------------------------------------------------------
# Layer D: mcp-cce skill has essentials
# ---------------------------------------------------------------------------


def test_cce_skill_has_stop_rule() -> None:
    """The mcp-cce SKILL.md must contain the Stop Rule section."""
    content = CCE_SKILL.read_text(encoding="utf-8")
    assert "### Stop Rule" in content


def test_cce_skill_bans_semantic_search() -> None:
    """The mcp-cce skill must ban semantic_search when CCE is available."""
    content = CCE_SKILL.read_text(encoding="utf-8")
    assert re.search(
        r"(never|do not|don.t).*(semantic_search|`semantic_search`)",
        content,
        re.IGNORECASE,
    )


# ---------------------------------------------------------------------------
# Layer E: Mark has information query budget
# ---------------------------------------------------------------------------


def test_mark_has_information_query_budget() -> None:
    """Mark's JD must reference the information query budget."""
    content = MARK_JD.read_text(encoding="utf-8")
    assert re.search(r"information query budget", content, re.IGNORECASE)
