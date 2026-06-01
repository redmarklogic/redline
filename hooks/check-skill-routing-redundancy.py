"""Git hook: detect redundant skill references across routing and dependency sections.

If a skill name appears in a routing section ("Does Not Cover", "Out of Scope")
AND also in a dependency section ("For related topics:"), that is redundant.
The routing section is the canonical home for exclusion references.  Keeping
the same skill in "For related topics:" creates unnecessary DAG edges and
duplicates information.

Exit codes:
    0 — no redundancy found
    1 — redundant references detected
"""
# no-adr: enforces single-source routing in skill boundary contracts

import re
import sys
from pathlib import Path

_SKILLS_DIR = Path(".agents/skills")
_FM_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)

# Section headers that denote routing sections.
_ROUTING_HEADER_RE = re.compile(
    r"^#{2,3}\s+(Does\s+Not\s+Cover|Out\s+of\s+Scope)\s*$",
    re.IGNORECASE,
)

# Inline boundary contract routing pattern (pipe-separated single-line format).
_INLINE_ROUTING_RE = re.compile(
    r"\*\*(Does\s+Not\s+Cover|Out\s+of\s+Scope)\s*:\*\*\s*(.+)$",
    re.IGNORECASE,
)

# "For related topics:" intro section header (not a markdown header, just text).
_RELATED_TOPICS_RE = re.compile(r"^For related topics\b", re.IGNORECASE)

# Any markdown header — used to detect section boundaries.
_ANY_HEADER_RE = re.compile(r"^#{1,6}\s+")

# Backtick-wrapped skill reference.
_BACKTICK_REF_RE = re.compile(r"`([a-z][a-z0-9\-]+)`")


def discover_skills() -> set[str]:
    """Return set of known skill names from directory listing."""
    return {
        d.name
        for d in _SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    }


def _extract_skill_refs(text: str, known_skills: set[str]) -> set[str]:
    """Extract backtick-wrapped skill names from text."""
    return {m.group(1) for m in _BACKTICK_REF_RE.finditer(text)} & known_skills


def _parse_sections(content: str, known_skills: set[str]) -> tuple[set[str], set[str]]:
    """Parse a SKILL.md and return (routing_skills, related_topics_skills).

    routing_skills: skills referenced in "Does Not Cover" / "Out of Scope"
    related_topics_skills: skills referenced in "For related topics:" section
    """
    # Strip frontmatter
    content = _FM_RE.sub("", content)

    routing_skills: set[str] = set()
    related_topics_skills: set[str] = set()

    lines = content.splitlines()
    in_routing = False
    in_related = False

    for line in lines:
        # Check for inline routing (single-line boundary contract format)
        m = _INLINE_ROUTING_RE.search(line)
        if m:
            routing_skills |= _extract_skill_refs(m.group(2), known_skills)
            continue

        # Check if this line starts a routing section
        if _ROUTING_HEADER_RE.match(line):
            in_routing = True
            in_related = False
            continue

        # Check if this line starts a "For related topics:" section
        if _RELATED_TOPICS_RE.match(line):
            in_related = True
            in_routing = False
            continue

        # Check if a new section header ends current section
        if _ANY_HEADER_RE.match(line):
            in_routing = False
            in_related = False

        # An empty line after related topics bullets ends the section
        # (related topics is not under a markdown header, just freestanding text)
        if in_related and line.strip() == "" and not in_routing:
            # Only end if we've already seen at least one bullet
            pass  # Keep going — empty lines between bullets are okay

        if in_routing:
            routing_skills |= _extract_skill_refs(line, known_skills)
        elif in_related:
            related_topics_skills |= _extract_skill_refs(line, known_skills)

    return routing_skills, related_topics_skills


def find_redundancies(
    known_skills: set[str],
) -> dict[str, set[str]]:
    """Return {skill_file: {redundant_skill_names}} for all violations."""
    violations: dict[str, set[str]] = {}

    for skill_id in sorted(known_skills):
        skill_md = _SKILLS_DIR / skill_id / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")

        routing, related = _parse_sections(content, known_skills)
        overlap = routing & related

        if overlap:
            violations[skill_id] = overlap

    return violations


def main() -> int:
    """Check for redundant skill references and report violations."""
    if not _SKILLS_DIR.is_dir():
        print("SKIP: .agents/skills/ directory not found.", file=sys.stderr)
        return 0

    known_skills = discover_skills()
    if not known_skills:
        return 0

    violations = find_redundancies(known_skills)

    if not violations:
        return 0

    total = sum(len(v) for v in violations.values())
    print(
        f"ERROR: {total} redundant skill reference(s) across "
        f"{len(violations)} file(s).\n"
        f"Skills in 'Does Not Cover'/'Out of Scope' MUST NOT also appear in\n"
        f"'For related topics:'. The routing section is the canonical home.\n"
        f"Remove the duplicate from 'For related topics:'.\n",
        file=sys.stderr,
    )

    for skill_id, dupes in sorted(violations.items()):
        path = _SKILLS_DIR / skill_id / "SKILL.md"
        for dupe in sorted(dupes):
            print(
                f"  {path}: `{dupe}` in both routing and 'For related topics:'",
                file=sys.stderr,
            )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
