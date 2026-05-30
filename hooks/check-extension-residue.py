"""Git hook: detect orphaned spec-kit extension integration files.

When 'specify extension add' installs an extension it writes to three
locations simultaneously:

  .specify/extensions/<id>/        — extension manifest and commands
  .github/agents/speckit.*         — Copilot agent integration file
  .agents/skills/speckit-*/        — Copilot skill integration file

Each file in the last two locations carries an ownership tag of the form
'<!-- Extension: <id> -->'. If the extension directory is deleted manually
(instead of via 'specify extension remove'), these integration files become
orphaned: the extension is gone but its agent/skill files remain, polluting
the VS Code customisation layer with stale commands.

This hook scans .github/agents/ and .agents/skills/ for Extension ownership
tags and verifies each referenced extension ID is present in
.specify/extensions/.registry. Any file whose ID is absent from the registry
is flagged as orphaned.

Fix: run 'specify extension remove <id>', or — if the extension directory
no longer exists — manually delete the flagged files in a single commit.

See ADR-013 (docs/adr/adr-013-speckit-lifecycle-hook-enforcement.md),
Consequences section: "A developer who deletes .specify/extensions/<id>/
without running 'specify extension remove' will leave orphaned files in
.github/agents/ and .agents/skills/."
See ADR-011 P1 (docs/adr/adr-011-hook-first-enforcement.md).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / ".specify" / "extensions" / ".registry"
AGENT_DIR = ROOT / ".github" / "agents"
SKILLS_DIR = ROOT / ".agents" / "skills"

_EXTENSION_TAG = re.compile(r"<!--\s*Extension:\s*([a-z0-9-]+)\s*-->")


def _installed_ids() -> set[str]:
    if not REGISTRY_PATH.exists():
        return set()
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        registry = json.load(f)
    return set(registry.get("extensions", {}).keys())


def _tagged_files() -> list[tuple[Path, str]]:
    results: list[tuple[Path, str]] = []
    for directory in (AGENT_DIR, SKILLS_DIR):
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.md")):
            content = path.read_text(encoding="utf-8", errors="replace")
            match = _EXTENSION_TAG.search(content)
            if match:
                results.append((path, match.group(1)))
    return results


def main() -> None:
    installed = _installed_ids()
    orphans = [
        (path, ext_id) for path, ext_id in _tagged_files() if ext_id not in installed
    ]

    if not orphans:
        sys.exit(0)

    print("Orphaned spec-kit extension integration files detected.")
    print(
        "These files were written by 'specify extension add' but their "
        "extension is no longer registered."
    )
    print()
    for path, ext_id in orphans:
        print(f"  {path.relative_to(ROOT)}  (extension: {ext_id})")
    print()
    print("Fix: run 'specify extension remove <id>' for each orphaned extension.")
    print(
        "If the extension directory was already deleted manually, remove the "
        "flagged files by scanning for '<!-- Extension: <id> -->' tags and "
        "deleting all three locations in a single commit."
    )
    print("See ADR-013 (docs/adr/adr-013-speckit-lifecycle-hook-enforcement.md).")
    sys.exit(1)


if __name__ == "__main__":
    main()
