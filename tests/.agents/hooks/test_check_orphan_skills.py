"""Behavioural tests for the check-orphan-skills hook.

Verifies two contracts:

1. A skill reachable only via .claude/commands/ IS reported as an orphan
   when command files are not a detection source (current behaviour before fix).

2. After adding .claude/commands/ as a detection source, the same skill is
   no longer an orphan.

Tests use a self-contained fake repo tree so they are isolated from the live
codebase and produce deterministic results.
"""

import importlib.util
from pathlib import Path

# ---------------------------------------------------------------------------
# Load the hook module once; patch its path globals per-test
# ---------------------------------------------------------------------------

_HOOK_PATH = Path(__file__).resolve().parents[3] / "hooks" / "check-orphan-skills.py"


def _load_hook():
    spec = importlib.util.spec_from_file_location("_check_orphan_skills", _HOOK_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _patch_paths(mod, tmp_path: Path) -> None:
    """Redirect all module-level path constants to the fake repo root."""
    mod._REPO = tmp_path
    mod._AGENTS_DIR = tmp_path / ".github" / "agents"
    mod._CLAUDE_AGENTS_DIR = tmp_path / ".claude" / "agents"
    mod._SKILLS_DIR = tmp_path / ".agents" / "skills"
    mod._AGENTS_MD = tmp_path / "AGENTS.md"


def _run_detection(mod) -> tuple[set[str], set[str]]:
    """Run detection using the current module state (no commands source)."""
    known = mod._known_skills()
    agent_ids, d1 = mod._degree1_edges(known)
    d2 = mod._degree2_edges(known)
    d3 = mod._degree3_edges(known)
    d1b = mod._agents_md_edges(known)
    all_edges = d1 + d2 + d3 + d1b
    reachable = mod._reachable(agent_ids, all_edges)
    return known, reachable


def _run_detection_with_commands(mod) -> tuple[set[str], set[str]]:
    """Run detection including the commands source (post-fix)."""
    known = mod._known_skills()
    agent_ids, d1 = mod._degree1_edges(known)
    d2 = mod._degree2_edges(known)
    d3 = mod._degree3_edges(known)
    d1b = mod._agents_md_edges(known)
    command_ids, dc = mod._commands_edges(known)
    all_edges = d1 + d2 + d3 + d1b + dc
    reachable = mod._reachable(agent_ids | command_ids, all_edges)
    return known, reachable


# ---------------------------------------------------------------------------
# Helpers to build minimal fake repo trees
# ---------------------------------------------------------------------------


def _make_skill(skills_dir: Path, name: str) -> None:
    (skills_dir / name).mkdir(parents=True)
    (skills_dir / name / "SKILL.md").write_text(
        f"# {name}\nNo backtick refs.\n", encoding="utf-8"
    )


def _make_agent_jd(agents_dir: Path, name: str, skills: list[str]) -> None:
    agents_dir.mkdir(parents=True, exist_ok=True)
    refs = "".join(f"`{s}`\n" for s in skills)
    (agents_dir / f"rl.{name}.agent.md").write_text(
        f"# {name}\n{refs}", encoding="utf-8"
    )


def _make_command(commands_dir: Path, name: str, skills: list[str]) -> None:
    commands_dir.mkdir(parents=True, exist_ok=True)
    refs = "".join(f"`{s}`\n" for s in skills)
    (commands_dir / f"{name}.md").write_text(f"# {name}\n{refs}", encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCommandsNotYetASource:
    """Phase 1 — RED: command-only skills are orphans before the fix."""

    def test_command_only_skill_is_unreachable(self, tmp_path):
        """A skill referenced only in a command file is not reachable."""
        skills_dir = tmp_path / ".agents" / "skills"
        _make_skill(skills_dir, "prek-find-and-fix")
        _make_skill(skills_dir, "agent-owned-skill")
        _make_agent_jd(
            tmp_path / ".github" / "agents", "kabilan", ["agent-owned-skill"]
        )
        _make_command(
            tmp_path / ".claude" / "commands", "git-push-batched", ["prek-find-and-fix"]
        )

        mod = _load_hook()
        _patch_paths(mod, tmp_path)
        known, reachable = _run_detection(mod)

        assert "prek-find-and-fix" in known
        assert "prek-find-and-fix" not in reachable, (
            "prek-find-and-fix should be an orphan when commands are not a detection source"
        )

    def test_agent_owned_skill_is_reachable(self, tmp_path):
        """Control: a skill in an agent JD is always reachable."""
        skills_dir = tmp_path / ".agents" / "skills"
        _make_skill(skills_dir, "agent-owned-skill")
        _make_agent_jd(
            tmp_path / ".github" / "agents", "kabilan", ["agent-owned-skill"]
        )

        mod = _load_hook()
        _patch_paths(mod, tmp_path)
        _known, reachable = _run_detection(mod)

        assert "agent-owned-skill" in reachable


class TestCommandsAsSource:
    """Phase 2 — GREEN: command files are a detection source after the fix."""

    def test_command_only_skill_becomes_reachable(self, tmp_path):
        """A skill referenced only in a command file is reachable after the fix."""
        skills_dir = tmp_path / ".agents" / "skills"
        _make_skill(skills_dir, "prek-find-and-fix")
        _make_skill(skills_dir, "agent-owned-skill")
        _make_agent_jd(
            tmp_path / ".github" / "agents", "kabilan", ["agent-owned-skill"]
        )
        _make_command(
            tmp_path / ".claude" / "commands", "git-push-batched", ["prek-find-and-fix"]
        )

        mod = _load_hook()
        _patch_paths(mod, tmp_path)
        mod._COMMANDS_DIR = tmp_path / ".claude" / "commands"
        _known, reachable = _run_detection_with_commands(mod)

        assert "prek-find-and-fix" in reachable, (
            "prek-find-and-fix should be reachable once commands are a detection source"
        )

    def test_skill_in_both_command_and_agent_still_reachable(self, tmp_path):
        """A skill referenced in both an agent JD and a command stays reachable."""
        skills_dir = tmp_path / ".agents" / "skills"
        _make_skill(skills_dir, "shared-skill")
        _make_agent_jd(tmp_path / ".github" / "agents", "kabilan", ["shared-skill"])
        _make_command(tmp_path / ".claude" / "commands", "some-cmd", ["shared-skill"])

        mod = _load_hook()
        _patch_paths(mod, tmp_path)
        mod._COMMANDS_DIR = tmp_path / ".claude" / "commands"
        _, reachable = _run_detection_with_commands(mod)

        assert "shared-skill" in reachable

    def test_skill_only_in_command_not_in_agent(self, tmp_path):
        """Command-only skill and agent-only skill are both reachable."""
        skills_dir = tmp_path / ".agents" / "skills"
        _make_skill(skills_dir, "command-only")
        _make_skill(skills_dir, "agent-only")
        _make_agent_jd(tmp_path / ".github" / "agents", "kabilan", ["agent-only"])
        _make_command(tmp_path / ".claude" / "commands", "cmd", ["command-only"])

        mod = _load_hook()
        _patch_paths(mod, tmp_path)
        mod._COMMANDS_DIR = tmp_path / ".claude" / "commands"
        _, reachable = _run_detection_with_commands(mod)

        assert "command-only" in reachable
        assert "agent-only" in reachable

    def test_skill_unreferenced_anywhere_remains_orphan(self, tmp_path):
        """A skill with no references anywhere is still an orphan."""
        skills_dir = tmp_path / ".agents" / "skills"
        _make_skill(skills_dir, "true-orphan")
        _make_skill(skills_dir, "agent-owned-skill")
        _make_agent_jd(
            tmp_path / ".github" / "agents", "kabilan", ["agent-owned-skill"]
        )

        mod = _load_hook()
        _patch_paths(mod, tmp_path)
        mod._COMMANDS_DIR = tmp_path / ".claude" / "commands"
        _, reachable = _run_detection_with_commands(mod)

        assert "true-orphan" not in reachable
