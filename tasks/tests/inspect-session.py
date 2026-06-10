"""Dump tool calls (+ CCE mentions) from one Claude Code session transcript.

Usage: python inspect-session.py <session-id>

Transcript dir is derived from the repo root's parent path automatically,
or override with CCE_TRANSCRIPT_DIR env var.
"""
import json
import os
import re
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[2]   # repo root

def transcript_dir() -> Path:
    if env := os.environ.get("CCE_TRANSCRIPT_DIR"):
        return Path(env)
    # Standard Claude Code path: slug = drive-letter + path segments joined by -
    slug = re.sub(r"[:\\/ ]+", "-", str(PROJ)).strip("-").lower()
    # Claude Code uses C--Users-... (drive colon becomes nothing, backslash → -)
    slug = re.sub(r"^([a-z])-", r"\1--", slug)
    return Path.home() / ".claude" / "projects" / slug


sid = sys.argv[1]
tf = transcript_dir() / f"{sid}.jsonl"
tools, cce_mentions = [], 0
for ln in tf.open(encoding="utf-8", errors="replace"):
    try:
        rec = json.loads(ln)
    except Exception:
        continue
    if rec.get("type") == "assistant":
        for blk in (rec.get("message") or {}).get("content") or []:
            if isinstance(blk, dict) and blk.get("type") == "tool_use":
                inp = json.dumps(blk.get("input"))[:100]
                tools.append(f"{blk.get('name')}  {inp}")
    else:
        if "mcp__context-engine" in json.dumps(rec):
            cce_mentions += 1

print("TOOL CALLS:")
for t in tools:
    print("  ", t)
print(f"\nnon-assistant transcript lines mentioning mcp__context-engine: {cce_mentions}")

last_text = ""
for ln in tf.open(encoding="utf-8", errors="replace"):
    try:
        rec = json.loads(ln)
    except Exception:
        continue
    if rec.get("type") == "assistant":
        for blk in (rec.get("message") or {}).get("content") or []:
            if isinstance(blk, dict) and blk.get("type") == "text" and blk.get("text"):
                last_text = blk["text"]
print("\nFINAL ANSWER:\n" + last_text[:600])
