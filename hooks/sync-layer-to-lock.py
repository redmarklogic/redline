"""Sync layer field in skills-lock.json from skills-taxonomy.md.

Parses the Layer Definitions section of skills-taxonomy.md to build a
skill-to-layer mapping, then writes the derived `layer` field into each
skill entry in skills-lock.json.

skills-taxonomy.md is the SOT for layer assignments (ADR-001).
skills-lock.json is the machine-readable registry; `layer` is a derived field.

Usage:
    python hooks/sync-layer-to-lock.py

Run automatically as a pre-commit hook. Exits non-zero if any skill in the
lock file has no layer assignment in the taxonomy.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TAXONOMY_PATH = REPO_ROOT / "docs" / "architecture" / "skills-taxonomy.md"
LOCK_PATH = REPO_ROOT / "skills-lock.json"


def parse_layer_map(taxonomy_text: str) -> dict[str, int]:
    """Return {skill_name: layer_number} extracted from Layer Definitions section only.

    Parsing is restricted to the ``## Layer Definitions`` section so that
    backtick-quoted skill names in examples, enforcement notes, or references
    are never mistakenly treated as layer assignments.
    Only table rows (lines starting with ``|``) are parsed within that section.
    """
    layer_map: dict[str, int] = {}
    current_layer: int | None = None
    in_layer_definitions = False

    for line in taxonomy_text.splitlines():
        # Enter the Layer Definitions section.
        if re.match(r"^##\s+Layer Definitions", line):
            in_layer_definitions = True
            continue

        # Exit on any level-2 heading (## but not ###) after entering.
        if in_layer_definitions and re.match(r"^##[^#]", line):
            break

        if not in_layer_definitions:
            continue

        # Detect layer heading: ### Layer N — ...
        heading_match = re.match(r"^###\s+Layer\s+(\d+)", line)
        if heading_match:
            current_layer = int(heading_match.group(1))
            continue

        if current_layer is None:
            continue

        # Only parse table rows to avoid extracting non-assignment backtick names.
        if not line.lstrip().startswith("|"):
            continue

        # Extract skill names from table cells: | `skill-name` | ... |
        # Handles multi-skill cells like | `a`, `b`, `c` |
        for cell in line.split("|"):
            for match in re.finditer(r"`([a-z][a-z0-9-]+)`", cell):
                skill = match.group(1)
                if skill not in layer_map:
                    layer_map[skill] = current_layer

    return layer_map


def main() -> int:
    taxonomy_text = TAXONOMY_PATH.read_text(encoding="utf-8")
    layer_map = parse_layer_map(taxonomy_text)

    lock_data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    skills = lock_data["skills"]

    missing: list[str] = []
    for skill_name, skill_data in skills.items():
        if skill_name in layer_map:
            skill_data["layer"] = layer_map[skill_name]
        else:
            missing.append(skill_name)

    if missing:
        print(
            f"ERROR: {len(missing)} skill(s) in skills-lock.json have no layer "
            f"assignment in skills-taxonomy.md:\n  " + "\n  ".join(missing),
            file=sys.stderr,
        )
        print(
            "Add each skill to the correct layer in the Layer Definitions section "
            "of docs/architecture/skills-taxonomy.md, then re-run this script.",
            file=sys.stderr,
        )
        return 1

    LOCK_PATH.write_text(json.dumps(lock_data, indent=2) + "\n", encoding="utf-8")

    print(f"Synced layer field for {len(skills)} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
