"""Tests for CCE integration - binary availability, skill bootstrap, and workflow mandates."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MCE_SKILL = REPO_ROOT / ".agents" / "skills" / "mcp-cce" / "SKILL.md"
ARCH_SKILL = REPO_ROOT / ".agents" / "skills" / "arch-engineering" / "SKILL.md"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
AGENTS_DIR = REPO_ROOT / ".github" / "agents"
HOOKS_DIR = REPO_ROOT / ".github" / "hooks"
VSCODE_SETTINGS = REPO_ROOT / ".vscode" / "settings.json"

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
    """Every rl.*.agent.md frontmatter tools: must include context-engine/*.

    CCE MCP server is registered as 'context-engine' in .vscode/mcp.json.
    The frontmatter tools: glob must match this name exactly — 'context-engin/*'
    (without the 'e') produces 'Unknown tool' warnings and is silently ignored.
    """

    @pytest.mark.parametrize(
        "jd_path",
        RL_AGENT_JDS,
        ids=[p.stem for p in RL_AGENT_JDS],
    )
    def test_agent_frontmatter_allows_cce_tools(self, jd_path: Path) -> None:
        content = jd_path.read_text(encoding="utf-8")
        assert "context-engine/*" in content, (
            f"{jd_path.name} frontmatter tools: missing `context-engine/*`. "
            "CCE MCP server is 'context-engine' in .vscode/mcp.json."
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


class TestCceSubagentUsage:
    """mcp-cce SKILL.md must document subagent frontmatter requirements.

    Subagents need context-engine/* in frontmatter tools: and the server
    name must match .vscode/mcp.json exactly.
    """

    def test_subagent_usage_documented(self) -> None:
        content = MCE_SKILL.read_text(encoding="utf-8")
        assert "subagent" in content.lower(), (
            "mcp-cce SKILL.md missing subagent usage documentation."
        )

    def test_correct_server_name_documented(self) -> None:
        content = MCE_SKILL.read_text(encoding="utf-8")
        assert "context-engine/*" in content, (
            "mcp-cce SKILL.md missing correct server name `context-engine/*`."
        )


class TestCceHookEnforcement:
    """Agent hooks must exist to deterministically inject CCE context into subagents.

    JD text constraints are advisory — the model may ignore them. Hooks provide
    a code-executed defence layer (Swiss Cheese Model: diverse layer types).
    """

    def test_subagent_hook_config_exists(self) -> None:
        hook_file = HOOKS_DIR / "cce-subagent.json"
        assert hook_file.exists(), (
            ".github/hooks/cce-subagent.json missing. "
            "This hook injects CCE context into subagent conversations."
        )

    def test_subagent_hook_config_valid_json(self) -> None:
        hook_file = HOOKS_DIR / "cce-subagent.json"
        content = hook_file.read_text(encoding="utf-8")
        data = json.loads(content)
        assert "hooks" in data, "Hook config missing top-level 'hooks' key"
        assert "SubagentStart" in data["hooks"], (
            "Hook config missing 'SubagentStart' event"
        )

    def test_subagent_hook_references_script(self) -> None:
        hook_file = HOOKS_DIR / "cce-subagent.json"
        content = hook_file.read_text(encoding="utf-8")
        assert "cce-inject.ps1" in content, (
            "Hook config does not reference cce-inject.ps1 script"
        )

    def test_hook_script_exists(self) -> None:
        script = HOOKS_DIR / "cce-inject.ps1"
        assert script.exists(), (
            ".github/hooks/cce-inject.ps1 missing. "
            "This script calls CCE and returns additionalContext JSON."
        )

    def test_hook_script_returns_additional_context(self) -> None:
        script = HOOKS_DIR / "cce-inject.ps1"
        content = script.read_text(encoding="utf-8")
        assert "additionalContext" in content, (
            "cce-inject.ps1 missing 'additionalContext' in output — "
            "hook must return hookSpecificOutput.additionalContext."
        )

    def test_hook_script_mentions_context_search(self) -> None:
        script = HOOKS_DIR / "cce-inject.ps1"
        content = script.read_text(encoding="utf-8")
        assert "context_search" in content, (
            "cce-inject.ps1 missing 'context_search' instruction — "
            "injected context must tell subagent to use context_search."
        )

    def test_vscode_settings_enables_agent_hooks(self) -> None:
        content = VSCODE_SETTINGS.read_text(encoding="utf-8")
        assert "chat.useCustomAgentHooks" in content, (
            ".vscode/settings.json missing 'chat.useCustomAgentHooks'. "
            "Agent-scoped hooks require this setting to be enabled."
        )

