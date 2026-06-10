"""TDD suite: CCE must connect, be discoverable, get used, and save tokens.

Fast config tests run by default. Slow/expensive tests are opt-in:
    pytest tasks/tests/                                # config + connection-lint
    pytest tasks/tests/ -m connect                     # spawns claude mcp list (~60s)
    pytest tasks/tests/ -m behavioral                  # headless claude -p runs (costs tokens)
"""
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

import pytest

PROJ = Path(__file__).resolve().parents[2]   # repo root
MCP_JSON = PROJ / ".mcp.json"
SETTINGS = PROJ / ".claude" / "settings.json"
INJECT = PROJ / ".claude" / "hooks" / "cce-inject.ps1"
SKILL = PROJ / ".agents" / "skills" / "mcp-cce" / "SKILL.md"


def _find_claude_exe() -> Path:
    """Locate claude.exe: PATH first, then known VS Code extension install dirs."""
    found = shutil.which("claude")
    if found:
        return Path(found)
    # VS Code extension install convention on Windows
    ext_base = Path(os.environ.get("USERPROFILE", "")) / ".vscode" / "extensions"
    if ext_base.exists():
        candidates = sorted(ext_base.glob("anthropic.claude-code-*/resources/native-binary/claude.exe"),
                            reverse=True)
        if candidates:
            return candidates[0]
    raise FileNotFoundError(
        "claude.exe not found on PATH or in ~/.vscode/extensions. "
        "Install Claude Code VS Code extension or add claude.exe to PATH.")


def _transcript_dir() -> Path:
    if env := os.environ.get("CCE_TRANSCRIPT_DIR"):
        return Path(env)
    slug = re.sub(r"[:\\/ ]+", "-", str(PROJ)).strip("-").lower()
    slug = re.sub(r"^([a-z])-", r"\1--", slug)
    return Path.home() / ".claude" / "projects" / slug


CLAUDE = _find_claude_exe()
TRANSCRIPTS = _transcript_dir()


# Copilot-era tool names that do not exist in Claude Code. Their presence in
# instructions makes the instructions unfollowable.
COPILOT_VOCAB = ["semantic_search", "read_file", "list_dir", "file_search",
                 "mcp_context-engin", '"tool_search"', "'tool_search'"]


# ---------- T1: config must be expansion-free and resolvable ----------

def test_mcp_command_has_no_unexpanded_vars():
    cfg = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    ce = cfg["mcpServers"]["context-engine"]
    blob = json.dumps(ce)
    assert "${" not in blob, (
        f"context-engine config relies on ${{VAR}} expansion which has failed "
        f"twice on this machine (see commit 7cfac13): {blob}")


def test_mcp_command_resolves():
    cfg = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    cmd = cfg["mcpServers"]["context-engine"]["command"]
    if "\\" in cmd or "/" in cmd:
        assert Path(cmd).exists(), f"configured binary missing: {cmd}"
    else:
        r = subprocess.run(["where.exe", cmd], capture_output=True, text=True)
        assert r.returncode == 0, f"'{cmd}' not on PATH"


def test_sonarqube_no_pull_always():
    cfg = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    args = cfg["mcpServers"]["sonarqube"]["args"]
    assert "--pull=always" not in args


# ---------- T2: instructions must use tool names that exist ----------

def test_inject_hook_uses_claude_code_vocabulary():
    text = INJECT.read_text(encoding="utf-8")
    bad = [w for w in COPILOT_VOCAB if w in text]
    assert not bad, f"cce-inject.ps1 references non-existent tools: {bad}"
    assert "mcp__context-engine__context_search" in text, (
        "inject hook must name the real MCP tool so agents can actually call it")


def test_skill_uses_claude_code_vocabulary():
    text = SKILL.read_text(encoding="utf-8")
    bad = [w for w in COPILOT_VOCAB if w in text]
    assert not bad, f"mcp-cce SKILL.md references non-existent tools: {bad}"
    assert "context_search" in text


# ---------- T3: a routing nudge must exist at exploration time ----------

def test_settings_has_exploration_routing_nudge():
    cfg = json.loads(SETTINGS.read_text(encoding="utf-8"))
    pre = cfg.get("hooks", {}).get("PreToolUse", [])
    nudges = [e for e in pre
              if re.search(r"Grep|Glob", e.get("matcher", ""))
              and any("context_search" in h.get("command", "")
                      or "cce-route" in h.get("command", "")
                      for h in e.get("hooks", []))]
    assert nudges, ("no PreToolUse routing nudge on Grep/Glob pointing the "
                    "model at context_search")


# ---------- T4: server connects (slow) ----------

@pytest.mark.connect
def test_claude_reports_context_engine_connected():
    r = subprocess.run([str(CLAUDE), "mcp", "list"], capture_output=True,
                       text=True, cwd=PROJ, timeout=180)
    line = next((ln for ln in r.stdout.splitlines() if "context-engine" in ln), "")
    assert "Connected" in line and "Failed" not in line, (
        f"context-engine not connected: {line or r.stdout[-400:]}")


@pytest.mark.connect
def test_handshake_under_15s():
    probe = Path(__file__).parent / "probe-cce-mcp.py"
    venv_py = PROJ / ".venv" / "Scripts" / "python.exe"
    py = str(venv_py) if venv_py.exists() else shutil.which("python") or "python"
    r = subprocess.run([py, str(probe)], capture_output=True, text=True, timeout=180)
    m = re.search(r"initialize OK in ([\d.]+)s", r.stdout)
    assert m, f"probe failed: {r.stdout[-400:]} {r.stderr[-400:]}"
    assert float(m.group(1)) < 15, f"handshake too slow: {m.group(1)}s"


# ---------- T5: behavioral — a real session must USE context_search ----------

EXPLORE_PROMPTS = [
    "Where is the Cloud Run service configured in this repo and which secrets does it reference? Give file paths only, one line each.",
    "Which hooks run on Write or Edit tool calls in this project and what does each do? One line per hook.",
]


def run_headless(prompt: str):
    r = subprocess.run(
        [str(CLAUDE), "-p", prompt, "--output-format", "json",
         "--allowedTools", "mcp__context-engine", "--model", "sonnet"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=PROJ, timeout=600)
    out = json.loads(r.stdout)
    sid = out.get("session_id")
    tools_used = []
    tf = TRANSCRIPTS / f"{sid}.jsonl"
    if sid and tf.exists():
        for ln in tf.open(encoding="utf-8", errors="replace"):
            try:
                rec = json.loads(ln)
            except Exception:
                continue
            if rec.get("type") == "assistant":
                for blk in (rec.get("message") or {}).get("content") or []:
                    if isinstance(blk, dict) and blk.get("type") == "tool_use":
                        tools_used.append(blk.get("name"))
    return out, tools_used


@pytest.mark.behavioral
def test_exploration_prompts_use_context_search():
    hits = 0
    for p in EXPLORE_PROMPTS:
        out, tools = run_headless(p)
        used = [t for t in tools if t and t.startswith("mcp__context-engine")]
        print(f"\nPROMPT: {p[:60]}...\n  tools: {tools}\n  cce: {used}\n"
              f"  cost: ${out.get('total_cost_usd', 0):.3f}  "
              f"turns: {out.get('num_turns')}")
        if used:
            hits += 1
    assert hits >= 1, "no headless exploration session used any CCE tool"


@pytest.mark.behavioral
def test_cce_savings_counter_increases():
    def query_count():
        r = subprocess.run(["cce", "savings"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           cwd=PROJ, timeout=120)
        m = re.search(r"(\d+)\s+quer", r.stdout or "")
        return int(m.group(1)) if m else 0

    before = query_count()
    _, tools = run_headless(EXPLORE_PROMPTS[0])
    used = [t for t in tools if t and t.startswith("mcp__context-engine")]
    assert used, f"session did not call any CCE tool (tools: {tools})"

    after = before
    deadline = time.time() + 60
    while time.time() < deadline:
        after = query_count()
        if after > before:
            break
        time.sleep(5)
    print(f"\ncce savings queries: {before} -> {after}")
    assert after > before, ("context_search was called but the savings "
                            "counter never recorded it within 60s")
