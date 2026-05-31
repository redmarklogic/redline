"""Tests for skill quality constraints across .agents/skills/."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SYSTEMATIC_DEBUGGING_SKILL = (
    REPO_ROOT / ".agents" / "skills" / "systematic-debugging" / "SKILL.md"
)


class TestSystematicDebuggingFiveWhysGate:
    """systematic-debugging SKILL.md must mandate Five Whys root cause analysis.

    Stopping at the proximate cause and declaring a system-level limitation
    without checking actual config/state is a diagnostic failure pattern.
    The skill must enforce Five Whys to a falsifiable fact before any fix.
    """

    def test_five_whys_referenced(self) -> None:
        content = SYSTEMATIC_DEBUGGING_SKILL.read_text(encoding="utf-8")
        assert "five whys" in content.lower(), (
            "systematic-debugging SKILL.md missing Five Whys mandate. "
            "Phase 1 Root Cause must require Five Whys to a falsifiable fact."
        )

    def test_proximate_cause_anti_pattern_documented(self) -> None:
        content = SYSTEMATIC_DEBUGGING_SKILL.read_text(encoding="utf-8")
        assert "proximate cause" in content.lower(), (
            "systematic-debugging SKILL.md missing proximate cause anti-pattern. "
            "Common Mistakes must warn against stopping at the proximate cause."
        )

    def test_falsifiable_fact_required(self) -> None:
        content = SYSTEMATIC_DEBUGGING_SKILL.read_text(encoding="utf-8")
        assert "falsifiable" in content.lower(), (
            "systematic-debugging SKILL.md missing falsifiable fact requirement. "
            "Root cause must land on a falsifiable fact, not an architectural theory."
        )
