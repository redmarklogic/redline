"""Behavioral tests for the CCE health-gate PreToolUse hook.

The hook (`.claude/hooks/cce-health-gate.ps1`) gates tool calls on Code Context
Engine health. These tests pin the behaviour that keeps it from wedging a session
(the failure mode observed in practice):

- it must NEVER gate ``AskUserQuestion`` or mutation tools (the human-escalation
  valve, and tools that do not consume CCE);
- on a ``cce status`` failure it must escalate to ``ask`` (not a hard ``deny``),
  so a flaky/locked engine cannot block the session;
- it must NEVER persist a sticky ``bad`` verdict (no 10-minute poison);
- it must still let ``cce``/``mcp`` repair commands through (escape hatch);
- when healthy it allows and caches a positive ``ok`` verdict.

The hook is exercised as a subprocess with a fake ``cce`` on PATH (controlling its
exit code) and an isolated ``TEMP`` so the cache flag can be inspected.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    shutil.which("powershell") is None and shutil.which("pwsh") is None,
    reason="PowerShell is required to execute the PreToolUse hook",
)

_HOOK_REL = Path(".claude/hooks/cce-health-gate.ps1")


def _powershell() -> str:
    return shutil.which("powershell") or shutil.which("pwsh")


def _run_hook(repo_root, tmp_path, *, tool_name=None, command=None, cce_exit=0):
    """Run the hook with a fake ``cce`` (given exit code) and isolated TEMP.

    Returns the completed process and the isolated temp dir (where the cache flag,
    if any, is written).
    """
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir(exist_ok=True)
    (fake_bin / "cce.bat").write_text(f"@echo off\r\nexit /b {cce_exit}\r\n")

    temp_dir = tmp_path / "temp"
    temp_dir.mkdir(exist_ok=True)

    tool_input = {}
    if command is not None:
        tool_input["command"] = command
    payload = {"hook_event_name": "PreToolUse", "tool_input": tool_input}
    if tool_name is not None:
        payload["tool_name"] = tool_name

    env = dict(os.environ)
    env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
    env["TEMP"] = str(temp_dir)
    env["TMP"] = str(temp_dir)
    env["CLAUDE_PROJECT_DIR"] = str(repo_root)

    proc = subprocess.run(
        [
            _powershell(),
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(repo_root / _HOOK_REL),
        ],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        check=False,
    )
    return proc, temp_dir


def _decision(stdout: str):
    """Return the hook's permissionDecision, or None when it allows (no output)."""
    stdout = stdout.strip()
    if not stdout:
        return None
    return json.loads(stdout)["hookSpecificOutput"]["permissionDecision"]


class TestCceHealthGate:
    """Anti-wedge contract for the CCE health-gate hook."""

    def test_ask_user_question_allowed_when_cce_down(self, repo_root, tmp_path):
        """AskUserQuestion must never be gated -- it is the escape valve."""
        proc, _ = _run_hook(
            repo_root, tmp_path, tool_name="AskUserQuestion", cce_exit=1
        )
        assert proc.returncode == 0
        assert _decision(proc.stdout) is None

    def test_write_allowed_when_cce_down(self, repo_root, tmp_path):
        """Mutation tools do not consume CCE and must not be gated."""
        proc, _ = _run_hook(repo_root, tmp_path, tool_name="Write", cce_exit=1)
        assert _decision(proc.stdout) is None

    def test_health_failure_escalates_to_ask_not_deny(self, repo_root, tmp_path):
        """A failing health check escalates to `ask`, never a hard `deny`."""
        proc, _ = _run_hook(repo_root, tmp_path, tool_name="Read", cce_exit=1)
        assert _decision(proc.stdout) == "ask"

    def test_health_failure_writes_no_bad_cache(self, repo_root, tmp_path):
        """A failure must not persist a sticky `bad` verdict (no 10-min poison)."""
        _, temp_dir = _run_hook(repo_root, tmp_path, tool_name="Read", cce_exit=1)
        for flag in temp_dir.glob("cce-health-*.flag"):
            assert "bad" not in flag.read_text().lower()

    def test_escape_hatch_allows_cce_command(self, repo_root, tmp_path):
        """Repair/diagnostic `cce` commands are always allowed (escape hatch)."""
        proc, _ = _run_hook(
            repo_root, tmp_path, tool_name="Bash", command="cce status", cce_exit=1
        )
        assert _decision(proc.stdout) is None

    def test_healthy_allows_and_caches_ok(self, repo_root, tmp_path):
        """When `cce status` succeeds the call is allowed and `ok` is cached."""
        proc, temp_dir = _run_hook(repo_root, tmp_path, tool_name="Read", cce_exit=0)
        assert _decision(proc.stdout) is None
        flags = list(temp_dir.glob("cce-health-*.flag"))
        assert flags, "expected an 'ok' cache flag to be written"
        assert flags[0].read_text().strip() == "ok"
