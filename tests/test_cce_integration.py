"""Tests for CCE integration - binary availability, skill bootstrap, and workflow mandates."""

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MCE_SKILL = REPO_ROOT / ".agents" / "skills" / "mcp-cce" / "SKILL.md"
ARCH_SKILL = REPO_ROOT / ".agents" / "skills" / "arch-engineering" / "SKILL.md"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
AGENTS_DIR = REPO_ROOT / ".github" / "agents"

# Every rl.*.agent.md file — these are the Redline agent JDs
RL_AGENT_JDS = sorted(AGENTS_DIR.glob("rl.*.agent.md"))


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


class TestAgentJdCceSkillRouting:
    """Every rl.*.agent.md must include mcp-cce in its skill routing table."""

    @pytest.mark.parametrize(
        "jd_path",
        RL_AGENT_JDS,
        ids=[p.stem for p in RL_AGENT_JDS],
    )
    def test_agent_jd_references_mcp_cce(self, jd_path: Path) -> None:
        content = jd_path.read_text(encoding="utf-8")
        assert "mcp-cce" in content, (
            f"{jd_path.name} missing `mcp-cce` in skill routing table. "
            "Subagents do not inherit AGENTS.md — CCE must be in each JD."
        )


class TestAgentJdSessionRecallMandate:
    """Every rl.*.agent.md must mandate session_recall at session start.

    Subagents do not inherit AGENTS.md. The session_recall mandate must be
    stated in each agent's own JD so the agent calls it when invoked as a
    subagent.
    """

    @pytest.mark.parametrize(
        "jd_path",
        RL_AGENT_JDS,
        ids=[p.stem for p in RL_AGENT_JDS],
    )
    def test_agent_jd_mandates_session_recall(self, jd_path: Path) -> None:
        content = jd_path.read_text(encoding="utf-8")
        assert "session_recall" in content, (
            f"{jd_path.name} missing `session_recall` session-start mandate. "
            "Add a Session Start section or constraint requiring session_recall "
            "before any file exploration."
        )


class TestAgentJdCceToolSearchBootstrap:
    """Every rl.*.agent.md must inline the tool_search bootstrap for CCE.

    CCE tools are deferred. Without an explicit tool_search call, the CCE
    tools are invisible and the agent silently falls back to read_file.
    The JD must inline this step — agents cannot rely on loading the
    mcp-cce skill first because the skill routing table is advisory.
    """

    @pytest.mark.parametrize(
        "jd_path",
        RL_AGENT_JDS,
        ids=[p.stem for p in RL_AGENT_JDS],
    )
    def test_agent_jd_has_tool_search_bootstrap(self, jd_path: Path) -> None:
        content = jd_path.read_text(encoding="utf-8")
        assert "tool_search" in content, (
            f"{jd_path.name} missing `tool_search` bootstrap for CCE. "
            "CCE tools are deferred — without tool_search the agent cannot "
            "see them and silently falls back to read_file."
        )


class TestAgentJdCceToolsAllowlist:
    """Every rl.*.agent.md frontmatter tools: must include context-engin/*.

    CCE MCP tools are served by the context-engin MCP server. If the agent's
    frontmatter tools: list does not include context-engin/*, the subagent
    infrastructure blocks CCE tool calls regardless of JD instructions.
    """

    @pytest.mark.parametrize(
        "jd_path",
        RL_AGENT_JDS,
        ids=[p.stem for p in RL_AGENT_JDS],
    )
    def test_agent_frontmatter_allows_cce_tools(self, jd_path: Path) -> None:
        content = jd_path.read_text(encoding="utf-8")
        assert "context-engin/*" in content, (
            f"{jd_path.name} frontmatter tools: missing `context-engin/*`. "
            "CCE MCP tools are blocked at infrastructure level without this."
        )


class TestAgentJdCceDiscoveryConstraint:
    """Every rl.*.agent.md must mandate context_search for discovery.

    Without this constraint, agents default to read_file sweeps for
    exploration — consuming excessive tokens and bypassing the CCE index.
    """

    @pytest.mark.parametrize(
        "jd_path",
        RL_AGENT_JDS,
        ids=[p.stem for p in RL_AGENT_JDS],
    )
    def test_agent_jd_mandates_context_search(self, jd_path: Path) -> None:
        content = jd_path.read_text(encoding="utf-8")
        assert "context_search" in content, (
            f"{jd_path.name} missing `context_search` discovery constraint. "
            "Agents must use context_search (not read_file) for codebase "
            "exploration and discovery."
        )


class TestCceSubagentLimitation:
    """mcp-cce SKILL.md must document the subagent MCP limitation.

    Subagents invoked via runSubagent cannot call deferred MCP tools.
    The skill must document this and prescribe the orchestrator pattern
    where the calling agent calls CCE and passes results to the subagent.
    """

    def test_subagent_limitation_documented(self) -> None:
        content = MCE_SKILL.read_text(encoding="utf-8")
        assert "subagent" in content.lower(), (
            "mcp-cce SKILL.md missing subagent limitation documentation."
        )

    def test_orchestrator_pattern_documented(self) -> None:
        content = MCE_SKILL.read_text(encoding="utf-8")
        assert "orchestrator" in content.lower(), (
            "mcp-cce SKILL.md missing orchestrator pattern for passing "
            "CCE results to subagents via prompt injection."
        )
