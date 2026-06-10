"""Aggregate Claude Code transcript stats: tool usage, tokens, latency.

Scans main-session .jsonl transcripts for a project, pairs each tool_use with
its tool_result to measure wall-clock latency (= permission + hooks + tool),
and sums token usage from assistant message metadata.
"""
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median

PROJ = Path(__file__).resolve().parents[2]   # repo root
DAYS = 30


def transcript_dir() -> Path:
    if env := os.environ.get("CCE_TRANSCRIPT_DIR"):
        return Path(env)
    slug = re.sub(r"[:\\/ ]+", "-", str(PROJ)).strip("-").lower()
    slug = re.sub(r"^([a-z])-", r"\1--", slug)
    return Path.home() / ".claude" / "projects" / slug


def parse_ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def main():
    proj_dir = transcript_dir()
    cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)
    files = [f for f in proj_dir.glob("*.jsonl")
             if datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc) > cutoff]
    sub_files = [f for f in proj_dir.glob("*/subagents/*.jsonl")
                 if datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc) > cutoff]

    tool_count = defaultdict(int)
    tool_result_chars = defaultdict(int)
    tool_latency = defaultdict(list)
    usage = defaultdict(int)
    sessions = 0
    pending = {}

    for f in files:
        sessions += 1
        pending.clear()
        with f.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                ts = parse_ts(rec.get("timestamp", "")) if rec.get("timestamp") else None
                msg = rec.get("message") or {}
                if rec.get("type") == "assistant":
                    u = msg.get("usage") or {}
                    for k in ("input_tokens", "output_tokens",
                              "cache_read_input_tokens", "cache_creation_input_tokens"):
                        usage[k] += u.get(k) or 0
                    for blk in (msg.get("content") or []):
                        if isinstance(blk, dict) and blk.get("type") == "tool_use":
                            tool_count[blk.get("name", "?")] += 1
                            if ts:
                                pending[blk.get("id")] = (blk.get("name", "?"), ts)
                elif rec.get("type") == "user":
                    for blk in (msg.get("content") or []):
                        if isinstance(blk, dict) and blk.get("type") == "tool_result":
                            content = blk.get("content")
                            size = len(json.dumps(content, default=str)) if content else 0
                            tid = blk.get("tool_use_id")
                            name, t0 = pending.pop(tid, ("?", None))
                            tool_result_chars[name] += size
                            if t0 and ts:
                                dt = (ts - t0).total_seconds()
                                if 0 <= dt < 600:
                                    tool_latency[name].append(dt)

    sub_tool_count = defaultdict(int)
    for f in sub_files:
        with f.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if rec.get("type") == "assistant":
                    for blk in ((rec.get("message") or {}).get("content") or []):
                        if isinstance(blk, dict) and blk.get("type") == "tool_use":
                            sub_tool_count[blk.get("name", "?")] += 1

    print(f"=== {sessions} main sessions, {len(sub_files)} subagent transcripts, last {DAYS} days ===")
    print("\n--- Token usage (main sessions, sum of per-message usage) ---")
    for k, v in sorted(usage.items()):
        print(f"  {k:32s} {v:>14,}")

    print("\n--- Main-session tools: count | total result KB | median s | p90 s ---")
    rows = sorted(tool_count.items(), key=lambda kv: -kv[1])
    for name, n in rows[:25]:
        lat = sorted(tool_latency.get(name, []))
        med = f"{median(lat):6.1f}" if lat else "   n/a"
        p90 = f"{lat[int(len(lat) * 0.9)]:6.1f}" if len(lat) >= 5 else "   n/a"
        kb = tool_result_chars.get(name, 0) / 1024
        print(f"  {name:42s} {n:>5} | {kb:>9.0f} | {med} | {p90}")

    print("\n--- Subagent tools (top 15) ---")
    for name, n in sorted(sub_tool_count.items(), key=lambda kv: -kv[1])[:15]:
        print(f"  {name:42s} {n:>5}")

    total_lat = sum(sum(v) for v in tool_latency.values())
    n_lat = sum(len(v) for v in tool_latency.values())
    print(f"\nTotal measured tool wall-clock: {total_lat/3600:.1f} h across {n_lat} calls "
          f"(avg {total_lat/max(n_lat,1):.1f}s/call)")


if __name__ == "__main__":
    sys.exit(main())
