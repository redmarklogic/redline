"""Git hook: detect orphan skills (zero reachability from any agent node).

An orphan skill is one that no agent can reach — directly or transitively
through skill-to-skill cross-references or AGENTS.md mentions.
Orphans consume token budget on every session without ever being triggered.

Detection sources (in order):
  Degree-1  agent JD backtick mentions     (.github/agents/rl.*.agent.md,
                                             .github/agents/speckit.*.agent.md,
                                             .claude/agents/*.md)
  Degree-2  skill SKILL.md backtick refs   (.agents/skills/*/SKILL.md)
  Degree-1b AGENTS.md backtick mentions

Excluded from orphan detection:
  - Skills with prefix ``speckit-``  (vendor SpecKit extension hooks —
    invoked by .specify/extensions.yml, never manually loaded)
  - ``using-superpowers``             (framework bootstrap, operates
    before any routing table is consulted — adding it to JDs would be circular)
  - Skills listed in KNOWN_ORPHANS   (accepted / pending-deletion; add new
    entries here with a one-line comment explaining the status)

Exit codes:
    0 — no unaccepted orphans found
    1 — new orphan skills detected (not in KNOWN_ORPHANS)
"""
# no-adr: enforces agent-skill reachability invariant; governance rule lives in
# ADR-009 (docs/adr/adr-009-skill-taxonomy-and-governance-registry.md)

from __future__ import annotations

import re
import sys
from collections import deque
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parents[1]
_AGENTS_DIR = _REPO / ".github" / "agents"
_CLAUDE_AGENTS_DIR = _REPO / ".claude" / "agents"
_SKILLS_DIR = _REPO / ".agents" / "skills"
_AGENTS_MD = _REPO / "AGENTS.md"

# ---------------------------------------------------------------------------
# Exclusions
# ---------------------------------------------------------------------------

_VENDOR_PREFIX = "speckit-"

_FRAMEWORK_BOOTSTRAPS: frozenset[str] = frozenset({"using-superpowers"})

# Skills that are known orphans, accepted or pending deletion.
# Format: skill_name -> reason (displayed in output so reviewers understand status)
KNOWN_ORPHANS: dict[str, str] = {
    "executing-plans": "SUPERSEDED stub (overrides vendor skill); pending deletion per spec-011 T-008",
    "writing-plans": "SUPERSEDED stub (overrides vendor skill); pending deletion per spec-011 T-008",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_BACKTICK_RE = re.compile(r"`([^`\n]+)`")
_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+\.md[^)]*)\)")


def _backtick_tokens(text: str) -> list[str]:
    return _BACKTICK_RE.findall(text)


def _skill_from_url(url: str, known: set[str]) -> str | None:
    """Return the first path segment in *url* that matches a known skill name.

    Handles relative file links like ``../mental-models/strategic_decisions/rice.md``
    where ``mental-models`` is a known skill.
    """
    parts = url.replace("\\", "/").split("/")
    for part in parts:
        clean = part.split("#")[0].split("?")[0].removesuffix(".md")
        if clean in known:
            return clean
    return None


def _agent_id(path: Path) -> str:
    stem = path.stem  # e.g. "rl.kabilan.agent"
    if stem.startswith("rl."):
        return stem.split(".")[1]
    if stem.startswith("speckit."):
        parts = stem.split(".")
        return ".".join(parts[:-1])
    return stem.removesuffix(".agent")


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------


def _known_skills() -> set[str]:
    return {
        d.name
        for d in _SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    }


def _degree1_edges(known: set[str]) -> tuple[set[str], list[tuple[str, str]]]:
    """Return (agent_ids, edges) from agent JD backtick mentions."""
    agents: set[str] = set()
    edges: list[tuple[str, str]] = []

    patterns = (
        list(_AGENTS_DIR.glob("rl.*.agent.md"))
        + list(_AGENTS_DIR.glob("speckit.*.agent.md"))
        + list(_CLAUDE_AGENTS_DIR.glob("*.md"))
    )
    for path in sorted(patterns):
        aid = _agent_id(path)
        agents.add(aid)
        content = path.read_text(encoding="utf-8")
        seen: set[str] = set()
        for tok in _backtick_tokens(content):
            skill = tok.strip()
            if skill in known and skill not in seen:
                edges.append((aid, skill))
                seen.add(skill)

    return agents, edges


def _degree2_edges(known: set[str]) -> list[tuple[str, str]]:
    """Return skill→skill edges from SKILL.md backtick mentions."""
    edges: list[tuple[str, str]] = []
    for skill_dir in sorted(_SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        sid = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text(encoding="utf-8")
        seen: set[str] = set()
        for tok in _backtick_tokens(content):
            target = tok.strip()
            if target in known and target != sid and target not in seen:
                edges.append((sid, target))
                seen.add(target)
    return edges


def _degree3_edges(known: set[str]) -> list[tuple[str, str]]:
    """Return skill→skill edges from markdown file links inside skill directories.

    Scans every .md file inside each skill directory for links whose URL
    contains a path segment matching a known skill name.  These represent
    implicit references, e.g. ``[RICE](../mental-models/strategic_decisions/rice.md)``
    counts as skill ``pm-prioritization`` referencing skill ``mental-models``.
    """
    edges: list[tuple[str, str]] = []
    for skill_dir in sorted(_SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        sid = skill_dir.name
        seen: set[str] = set()
        for md_file in skill_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
            except OSError:
                continue
            for m in _MD_LINK_RE.finditer(content):
                target = _skill_from_url(m.group(2), known)
                if target and target != sid and target not in seen:
                    edges.append((sid, target))
                    seen.add(target)
    return edges


def _agents_md_edges(known: set[str]) -> list[tuple[str, str]]:
    """Return virtual 'agents.md'→skill edges from AGENTS.md backtick mentions."""
    if not _AGENTS_MD.exists():
        return []
    content = _AGENTS_MD.read_text(encoding="utf-8")
    edges: list[tuple[str, str]] = []
    seen: set[str] = set()
    for tok in _backtick_tokens(content):
        skill = tok.strip()
        if skill in known and skill not in seen:
            edges.append(("agents.md", skill))
            seen.add(skill)
    return edges


def _reachable(agent_ids: set[str], all_edges: list[tuple[str, str]]) -> set[str]:
    """BFS from agent nodes (+ agents.md) to find all reachable skills."""
    adj: dict[str, list[str]] = {}
    for src, dst in all_edges:
        adj.setdefault(src, []).append(dst)

    visited: set[str] = set()
    queue: deque[str] = deque(agent_ids)
    queue.append("agents.md")

    while queue:
        node = queue.popleft()
        for neighbour in adj.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return visited


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    known = _known_skills()

    agent_ids, d1 = _degree1_edges(known)
    d2 = _degree2_edges(known)
    d3 = _degree3_edges(known)
    d1b = _agents_md_edges(known)

    all_edges = d1 + d2 + d3 + d1b
    reached = _reachable(agent_ids, all_edges)

    # Classify unreachable skills
    unreachable = sorted(known - reached)
    vendor = [s for s in unreachable if s.startswith(_VENDOR_PREFIX)]
    bootstrap = [s for s in unreachable if s in _FRAMEWORK_BOOTSTRAPS]
    accepted = [
        s
        for s in unreachable
        if s in KNOWN_ORPHANS
        and not s.startswith(_VENDOR_PREFIX)
        and s not in _FRAMEWORK_BOOTSTRAPS
    ]
    new_orphans = [
        s
        for s in unreachable
        if not s.startswith(_VENDOR_PREFIX)
        and s not in _FRAMEWORK_BOOTSTRAPS
        and s not in KNOWN_ORPHANS
    ]

    if not new_orphans:
        if accepted:
            print(
                f"check-orphan-skills: {len(accepted)} accepted orphan(s) on watchlist "
                f"(pending action): {', '.join(accepted)}"
            )
        print(
            f"check-orphan-skills: OK — {len(known)} skills, "
            f"{len(agent_ids)} agents, "
            f"{len(vendor)} vendor-extensions excluded, "
            f"{len(bootstrap)} framework-bootstraps excluded."
        )
        return 0

    print(
        "ERROR: Orphan skills detected — not reachable from any agent.", file=sys.stderr
    )
    print(
        "Each orphan wastes token budget on every session. "
        "Fix: add to an agent JD routing table, or delete the skill directory.",
        file=sys.stderr,
    )
    print(file=sys.stderr)
    for skill in new_orphans:
        print(f"  ORPHAN  {skill}", file=sys.stderr)
    print(file=sys.stderr)
    if accepted:
        print(
            f"  Accepted/watchlist orphans ({len(accepted)} — not blocking):",
            file=sys.stderr,
        )
        for skill in accepted:
            print(f"    {skill}  # {KNOWN_ORPHANS[skill]}", file=sys.stderr)
    print(file=sys.stderr)
    print(
        "To accept a new orphan temporarily, add it to KNOWN_ORPHANS in "
        "hooks/check-orphan-skills.py with a reason and a tracking reference.",
        file=sys.stderr,
    )
    print(
        "See ADR-009 (docs/adr/adr-009-skill-taxonomy-and-governance-registry.md) "
        "for governance rules.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
