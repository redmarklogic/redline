"""Tests for CCE integration - binary availability, skill bootstrap, and workflow mandates."""

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MCE_SKILL = REPO_ROOT / ".agents" / "skills" / "mcp-cce" / "SKILL.md"
ARCH_SKILL = REPO_ROOT / ".agents" / "skills" / "arch-engineering" / "SKILL.md"
AGENTS_MD = REPO_ROOT / "AGENTS.md"


class TestCceBinaryOnPath:
    """CCE binary must be discoverable on PATH so cce savings works."""

    def test_cce_on_path(self) -> None:
        assert shutil.which("cce") is not None, (
            "cce not found on PATH. Add C:\\Users\\harel\\.local\\bin to PATH."
        )

    def test_cce_version_runs(self) -> None:
        result = subprocess.run(
            ["cce", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"cce --version failed: {result.stderr}"


class TestMcpCceSkillBootstrap:
    """mcp-cce SKILL.md must instruct agents to call tool_search before CCE tools."""

    def test_tool_search_prerequisite_present(self) -> None:
        content = MCE_SKILL.read_text(encoding="utf-8")
        assert "tool_search" in content, (
            "mcp-cce SKILL.md missing tool_search bootstrap step"
        )

    def test_session_recall_at_session_start(self) -> None:
        content = MCE_SKILL.read_text(encoding="utf-8")
        assert "session_recall" in content, (
            "mcp-cce SKILL.md missing session_recall guidance"
        )


class TestSessionRecallMandate:
    """AGENTS.md must mandate session_recall as first call."""

    def test_agents_md_mandates_session_recall(self) -> None:
        content = AGENTS_MD.read_text(encoding="utf-8")
        assert "session_recall" in content, (
            "AGENTS.md missing session_recall mandate in CCE section"
        )


class TestRecordDecisionMandate:
    """arch-engineering SKILL.md must mandate record_decision for design choices."""

    def test_record_decision_in_arch_skill(self) -> None:
        content = ARCH_SKILL.read_text(encoding="utf-8")
        assert "record_decision" in content, (
            "arch-engineering SKILL.md missing record_decision mandate"
        )
