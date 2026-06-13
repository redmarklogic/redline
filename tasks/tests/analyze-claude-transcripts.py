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
from datetime import UTC, datetime, timedelta
from pathlib import Path
from statistics import median

PROJ = Path(__file__).resolve().parents[2]  # repo root
DAYS = 30

USAGE_KEYS = (
    "input_tokens",
    "output_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
)


def transcript_dir() -> Path:
    if env := os.environ.get("CCE_TRANSCRIPT_DIR"):
        return Path(env)
    slug = re.sub(r"[:\\/ ]+", "-", str(PROJ)).strip("-").lower()
    slug = re.sub(r"^([a-z])-", r"\1--", slug)
    return Path.home() / ".claude" / "projects" / slug


def parse_ts(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def recent_files(proj_dir: Path, pattern: str, cutoff: datetime) -> list[Path]:
    return [
        f
        for f in proj_dir.glob(pattern)
        if datetime.fromtimestamp(f.stat().st_mtime, tz=UTC) > cutoff
    ]


def iter_records(path: Path):
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            yield rec


def content_blocks(msg: dict, block_type: str):
    for blk in msg.get("content") or []:
        if isinstance(blk, dict) and blk.get("type") == block_type:
            yield blk


class SessionStats:
    """Accumulates tool/usage/latency stats across main-session transcripts."""

    def __init__(self):
        self.tool_count = defaultdict(int)
        self.tool_result_chars = defaultdict(int)
        self.tool_latency = defaultdict(list)
        self.usage = defaultdict(int)
        self.sessions = 0

    def add_session(self, path: Path) -> None:
        self.sessions += 1
        pending = {}
        for rec in iter_records(path):
            ts = parse_ts(rec.get("timestamp", "")) if rec.get("timestamp") else None
            if rec.get("type") == "assistant":
                self._add_assistant(rec, ts, pending)
            elif rec.get("type") == "user":
                self._add_user(rec, ts, pending)

    def _add_assistant(self, rec, ts, pending) -> None:
        msg = rec.get("message") or {}
        u = msg.get("usage") or {}
        for k in USAGE_KEYS:
            self.usage[k] += u.get(k) or 0
        for blk in content_blocks(msg, "tool_use"):
            self.tool_count[blk.get("name", "?")] += 1
            if ts:
                pending[blk.get("id")] = (blk.get("name", "?"), ts)

    def _add_user(self, rec, ts, pending) -> None:
        msg = rec.get("message") or {}
        for blk in content_blocks(msg, "tool_result"):
            content = blk.get("content")
            size = len(json.dumps(content, default=str)) if content else 0
            name, t0 = pending.pop(blk.get("tool_use_id"), ("?", None))
            self.tool_result_chars[name] += size
            if t0 and ts:
                dt = (ts - t0).total_seconds()
                if 0 <= dt < 600:
                    self.tool_latency[name].append(dt)


def count_subagent_tools(files: list[Path]) -> dict[str, int]:
    counts = defaultdict(int)
    for f in files:
        for rec in iter_records(f):
            if rec.get("type") == "assistant":
                for blk in content_blocks(rec.get("message") or {}, "tool_use"):
                    counts[blk.get("name", "?")] += 1
    return counts


def print_report(stats: SessionStats, sub_tool_count: dict, n_sub_files: int) -> None:
    print(
        f"=== {stats.sessions} main sessions, {n_sub_files} subagent transcripts, last {DAYS} days ==="
    )
    print("\n--- Token usage (main sessions, sum of per-message usage) ---")
    for k, v in sorted(stats.usage.items()):
        print(f"  {k:32s} {v:>14,}")

    print("\n--- Main-session tools: count | total result KB | median s | p90 s ---")
    rows = sorted(stats.tool_count.items(), key=lambda kv: -kv[1])
    for name, n in rows[:25]:
        lat = sorted(stats.tool_latency.get(name, []))
        med = f"{median(lat):6.1f}" if lat else "   n/a"
        p90 = f"{lat[int(len(lat) * 0.9)]:6.1f}" if len(lat) >= 5 else "   n/a"
        kb = stats.tool_result_chars.get(name, 0) / 1024
        print(f"  {name:42s} {n:>5} | {kb:>9.0f} | {med} | {p90}")

    print("\n--- Subagent tools (top 15) ---")
    for name, n in sorted(sub_tool_count.items(), key=lambda kv: -kv[1])[:15]:
        print(f"  {name:42s} {n:>5}")

    total_lat = sum(sum(v) for v in stats.tool_latency.values())
    n_lat = sum(len(v) for v in stats.tool_latency.values())
    print(
        f"\nTotal measured tool wall-clock: {total_lat / 3600:.1f} h across {n_lat} calls "
        f"(avg {total_lat / max(n_lat, 1):.1f}s/call)"
    )


def main():
    proj_dir = transcript_dir()
    cutoff = datetime.now(UTC) - timedelta(days=DAYS)
    files = recent_files(proj_dir, "*.jsonl", cutoff)
    sub_files = recent_files(proj_dir, "*/subagents/*.jsonl", cutoff)

    stats = SessionStats()
    for f in files:
        stats.add_session(f)

    sub_tool_count = count_subagent_tools(sub_files)
    print_report(stats, sub_tool_count, len(sub_files))


if __name__ == "__main__":
    sys.exit(main())
