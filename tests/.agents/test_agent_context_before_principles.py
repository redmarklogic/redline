"""Tests that Advisory Board agent JDs contain a Context-Before-Principles filter.

Every agent that consumes framework knowledge from notebooks risks producing
generic textbook advice instead of Redline-grounded recommendations. Peter's JD
already includes an explicit Context-Before-Principles output gate. These tests
verify all Advisory Board agents have an equivalent safeguard in their Session
Discipline section.
"""

from pathlib import Path

import pytest

AGENTS_DIR = Path(__file__).parents[2] / ".github" / "agents"

ADVISORY_BOARD_AGENTS = ["ron", "mark", "graeme", "john", "matt"]

CONTEXT_FILTER_PHRASES = [
    "redline-specific constraints",
    "current stage",
    "kill criteria",
]


@pytest.fixture(params=ADVISORY_BOARD_AGENTS)
def agent_jd(request: pytest.FixtureRequest) -> tuple[str, str]:
    """Return (agent_name, file_content) for each Advisory Board agent."""
    agent_name: str = request.param
    path = AGENTS_DIR / f"rl.{agent_name}.agent.md"
    return agent_name, path.read_text(encoding="utf-8")


def test_session_discipline_contains_context_before_principles_filter(
    agent_jd: tuple[str, str],
) -> None:
    """Each agent's Session Discipline must require filtering principles through
    Redline-specific constraints before stating recommendations."""
    agent_name, content = agent_jd

    session_section = _extract_section(content, "Session Discipline")
    assert session_section is not None, (
        f"{agent_name}: missing 'Session Discipline' section"
    )

    session_lower = session_section.lower()
    for phrase in CONTEXT_FILTER_PHRASES:
        assert phrase in session_lower, (
            f"{agent_name}: Session Discipline missing '{phrase}'"
        )


def _extract_section(markdown: str, heading: str) -> str | None:
    """Extract content under a markdown heading (## level) until the next heading."""
    lines = markdown.split("\n")
    capture = False
    result: list[str] = []
    for line in lines:
        if line.startswith("## ") and heading.lower() in line.lower():
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            result.append(line)
    return "\n".join(result) if result else None
