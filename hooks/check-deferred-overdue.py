"""Git hook: warn when deferred items in docs/deferred/ have passed their revisit_by date.

Scans all markdown files under the configured deferred directory (default:
docs/deferred/) and surfaces any open items whose optional `revisit_by`
frontmatter field has passed today's date.

This is a WARNING hook — it exits 0 regardless of findings so it never blocks
a push. The goal is visibility, not enforcement.

# no-adr: warning-only reminder hook; no architectural invariant.
# Deferred item governance is defined in docs/deferred/_index.md and
# the task-defer skill.
"""

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

_FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_KV_PATTERN = re.compile(r"^(\w+):\s+(.+)$", re.MULTILINE)


def parse_frontmatter(content: str) -> dict[str, str]:
    """Return simple key: value pairs from YAML frontmatter.

    Skips block-scalar continuation lines (lines starting with whitespace)
    and only reads single-line key: value entries.
    """
    match = _FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}
    fm_block = match.group(1)
    result: dict[str, str] = {}
    for m in _KV_PATTERN.finditer(fm_block):
        key = m.group(1)
        value = m.group(2).strip().strip('"')
        result[key] = value
    return result


def find_overdue_items(
    deferred_dir: Path,
    today: date,
) -> list[tuple[str, str]]:
    """Return (filename, revisit_by) pairs for open items past their revisit_by date.

    Items without a revisit_by field are skipped — they are condition-gated,
    not date-gated.
    """
    overdue: list[tuple[str, str]] = []
    for md_file in sorted(deferred_dir.glob("*.md")):
        if md_file.name == "_index.md":
            continue
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if fm.get("status") in ("done", "cancelled"):
            continue
        revisit_by_str = fm.get("revisit_by")
        if not revisit_by_str:
            continue
        try:
            revisit_by = datetime.strptime(revisit_by_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        if revisit_by < today:
            overdue.append((md_file.name, revisit_by_str))
    return overdue


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deferred-dir",
        default="docs/deferred",
        help="Path to the deferred items directory (default: docs/deferred)",
    )
    parser.add_argument(
        "--today",
        default=None,
        help="Override today's date (YYYY-MM-DD) — for testing only",
    )
    args = parser.parse_args()

    today = (
        datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    )
    deferred_dir = Path(args.deferred_dir)

    if not deferred_dir.is_dir():
        return 0

    overdue = find_overdue_items(deferred_dir, today)
    if not overdue:
        return 0

    print(f"\n[WARNING] {len(overdue)} deferred item(s) past their revisit_by date:\n")
    for filename, revisit_by in overdue:
        print(f"  {filename}  (revisit_by: {revisit_by})")
    print(
        "\nRun the quarterly-deferred-review or open docs/deferred/_index.md to triage.\n"
        "Push proceeds — this is a reminder only.\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
