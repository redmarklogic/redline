"""Git hook: detect cycles in the skill-to-skill dependency graph.

Scans .agents/skills/*/SKILL.md for references to other skills (both
backtick-wrapped and plain-text mentions), builds a directed graph of
skill-to-skill edges, and detects mutual references and longer cycles.

Section-aware: references inside routing sections ("Does Not Cover",
"Out of Scope") are excluded from edge detection.  These sections tell
agents *where to go instead* and are not dependency declarations.

Exit codes:
    0 — no cycles found (DAG is clean)
    1 — cycles detected (not a DAG)
"""
# no-adr: enforces DAG invariant on skill cross-references

import re
import sys
from pathlib import Path

_SKILLS_DIR = Path(".agents/skills")
_FM_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)

# Section headers that denote routing (not dependency) references.
# Content under these headers is excluded from edge detection.
_ROUTING_HEADER_RE = re.compile(
    r"^#{2,3}\s+(Does\s+Not\s+Cover|Out\s+of\s+Scope)\s*$",
    re.IGNORECASE,
)

# Any markdown header (## or ###) — used to detect end of a routing section.
_ANY_HEADER_RE = re.compile(r"^#{1,6}\s+")

# Inline boundary contract routing pattern:
#   **Does Not Cover:** ... or **Out of Scope:** ...
_INLINE_ROUTING_RE = re.compile(
    r"\*\*(Does\s+Not\s+Cover|Out\s+of\s+Scope)\s*:\*\*.*$",
    re.IGNORECASE,
)


def discover_skills() -> set[str]:
    """Return set of known skill names from directory listing."""
    return {
        d.name
        for d in _SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    }


def _build_skill_patterns(
    known_skills: set[str],
) -> dict[str, re.Pattern[str]]:
    """Build regex patterns for each skill name.

    Uses negative lookbehind/lookahead for alphanumeric and hyphen characters
    to avoid matching substrings (e.g. 'python-script' inside
    'python-script-numbering').
    """
    patterns: dict[str, re.Pattern[str]] = {}
    for skill in known_skills:
        escaped = re.escape(skill)
        patterns[skill] = re.compile(rf"(?<![a-zA-Z0-9\-]){escaped}(?![a-zA-Z0-9\-])")
    return patterns


def _strip_routing_sections(content: str) -> str:
    """Remove routing sections from content, keeping only dependency-relevant text.

    Routing sections ("Does Not Cover", "Out of Scope") contain references
    that tell agents *where else to go* — not dependencies.  These are
    excluded so that skill names in routing sections don't create DAG edges.
    """
    lines = content.splitlines()
    result: list[str] = []
    in_routing = False

    for line in lines:
        # Check for inline routing (single-line boundary contract format)
        if _INLINE_ROUTING_RE.search(line):
            continue

        # Check if this line starts a routing section
        if _ROUTING_HEADER_RE.match(line):
            in_routing = True
            continue

        # Check if this line starts a NEW section (exits routing)
        if in_routing and _ANY_HEADER_RE.match(line):
            in_routing = False

        if not in_routing:
            result.append(line)

    return "\n".join(result)


def build_edges(known_skills: set[str]) -> dict[str, set[str]]:
    """Parse SKILL.md files and return adjacency dict of skill -> {referenced skills}.

    Detects both backtick-wrapped and plain-text skill name mentions.
    YAML frontmatter and routing sections are excluded.
    """
    adjacency: dict[str, set[str]] = {s: set() for s in known_skills}
    patterns = _build_skill_patterns(known_skills)

    for skill_id in sorted(known_skills):
        skill_md = _SKILLS_DIR / skill_id / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")

        # Strip YAML frontmatter to avoid self-match on name: field
        content = _FM_RE.sub("", content)

        # Strip routing sections — references there are navigation hints,
        # not dependency declarations
        content = _strip_routing_sections(content)

        for target, pattern in patterns.items():
            if target == skill_id:
                continue
            if pattern.search(content):
                adjacency[skill_id].add(target)

    return adjacency


def find_mutual_references(
    adjacency: dict[str, set[str]],
) -> list[tuple[str, str]]:
    """Find all mutual reference pairs (A->B and B->A both exist).

    Returns sorted list of (A, B) tuples where A < B alphabetically,
    so each pair appears exactly once.
    """
    pairs: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for src, targets in adjacency.items():
        for dst in targets:
            if src in adjacency.get(dst, set()):
                pair = (min(src, dst), max(src, dst))
                if pair not in seen:
                    seen.add(pair)
                    pairs.append(pair)

    return sorted(pairs)


def find_cycle_nodes(adjacency: dict[str, set[str]]) -> list[str]:
    """Find nodes involved in cycles via Kahn's topological sort + reachability filter.

    Returns sorted list of node names that are genuinely in directed cycles
    (can reach themselves through other nodes).
    """
    # Phase 1: Kahn's algorithm to find candidate cycle nodes
    in_degree: dict[str, int] = dict.fromkeys(adjacency, 0)
    for targets in adjacency.values():
        for t in targets:
            if t in in_degree:
                in_degree[t] += 1

    queue: list[str] = [n for n, d in in_degree.items() if d == 0]
    removed: set[str] = set()

    while queue:
        node = queue.pop()
        removed.add(node)
        for neighbor in adjacency.get(node, set()):
            if neighbor in in_degree:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    candidates = set(adjacency) - removed
    if not candidates:
        return []

    # Phase 2: filter to nodes that can actually reach themselves
    # (excludes downstream nodes that just depend on cycle nodes)
    cycle_nodes: list[str] = []
    for node in sorted(candidates):
        if _can_reach_self(node, adjacency, candidates):
            cycle_nodes.append(node)

    return cycle_nodes


def _can_reach_self(
    node: str, adjacency: dict[str, set[str]], candidates: set[str]
) -> bool:
    """Return True if *node* can reach itself through *candidates*."""
    visited: set[str] = set()
    stack = [t for t in adjacency.get(node, set()) if t in candidates]
    while stack:
        current = stack.pop()
        if current == node:
            return True
        if current in visited:
            continue
        visited.add(current)
        for neighbor in adjacency.get(current, set()):
            if neighbor in candidates and neighbor not in visited:
                stack.append(neighbor)
    return False


def main() -> int:
    """Check skill-to-skill DAG and report violations."""
    if not _SKILLS_DIR.is_dir():
        print("SKIP: .agents/skills/ directory not found.", file=sys.stderr)
        return 0

    known_skills = discover_skills()
    if not known_skills:
        return 0

    adjacency = build_edges(known_skills)
    mutual_pairs = find_mutual_references(adjacency)
    cycle_nodes = find_cycle_nodes(adjacency)

    has_violations = False

    if mutual_pairs:
        has_violations = True
        total_edges = sum(len(v) for v in adjacency.values())
        print(
            f"ERROR: {len(mutual_pairs)} mutual reference(s) detected in skill "
            f"dependency graph ({len(known_skills)} skills, {total_edges} edges).\n"
            f"Each mutual reference creates a cycle. Remove one direction to fix.\n",
            file=sys.stderr,
        )
        for a, b in mutual_pairs:
            file_a = _SKILLS_DIR / a / "SKILL.md"
            file_b = _SKILLS_DIR / b / "SKILL.md"
            print(f"  {a} <-> {b}", file=sys.stderr)
            print(f"    {file_a}: references `{b}`", file=sys.stderr)
            print(f"    {file_b}: references `{a}`", file=sys.stderr)

    # Check for non-mutual cycles (longer rings like A->B->C->A)
    # Exclude nodes already covered by mutual pairs
    mutual_nodes = set()
    for a, b in mutual_pairs:
        mutual_nodes.add(a)
        mutual_nodes.add(b)
    remaining_cycle_nodes = [n for n in cycle_nodes if n not in mutual_nodes]

    if remaining_cycle_nodes:
        has_violations = True
        # Show the edges between cycle nodes for actionability
        print(
            f"\nERROR: {len(remaining_cycle_nodes)} skill(s) involved in "
            f"non-mutual cycles (longer rings):\n",
            file=sys.stderr,
        )
        for node in remaining_cycle_nodes:
            targets_in_cycle = sorted(t for t in adjacency[node] if t in cycle_nodes)
            for t in targets_in_cycle:
                src_file = _SKILLS_DIR / node / "SKILL.md"
                print(
                    f"  {node} -> {t}  ({src_file})",
                    file=sys.stderr,
                )
        print(
            "\nFix: remove one edge per ring to break the cycle.",
            file=sys.stderr,
        )

    if not has_violations:
        return 0

    if mutual_pairs:
        print(
            "\nFix: remove one direction of each mutual cross-reference in the "
            "SKILL.md files listed above. Keep the higher-level -> lower-level "
            "direction.",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    sys.exit(main())
