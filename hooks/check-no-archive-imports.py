"""Git hook: forbid imports from the archive/ directory.

AGENTS.md states that archive/ contains archived code for reference only
and MUST NOT be imported or used in the current codebase. Any import
statement that references the archive package or its sub-modules is a
violation that must be caught at commit time.

Scans .py files under the configured source directories.

Suppression: append `# hook: allow` to a line to exempt it.

AGENTS.md rule: "archive/ code is for reference only and MUST NOT be
imported."
"""
# no-adr: AGENTS.md architectural rule; no governing ADR

import argparse
import re
import sys
from pathlib import Path

_ARCHIVE_PATTERN = re.compile(
    r"^\s*(import archive\b|from archive(\.[^\s]+)?\s+import\b)"
)
_SUPPRESS = "# hook: allow"


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where archive imports are detected."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for py_file in sorted(directory.rglob("*.py")):
            lines = py_file.read_text(encoding="utf-8").splitlines()
            for lineno, line in enumerate(lines, start=1):
                if _SUPPRESS in line:
                    continue
                if _ARCHIVE_PATTERN.search(line):
                    violations.append((py_file, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for archive imports in source directories and report violations."""
    parser = argparse.ArgumentParser(
        description="Forbid imports from archive/ in source directories.",
    )
    parser.add_argument(
        "--dirs",
        action="append",
        default=[],
        help="Directory to scan (may be repeated).",
    )
    args = parser.parse_args()

    violations = find_violations([Path(d) for d in args.dirs])
    if not violations:
        return 0

    print(
        "ERROR: imports from archive/ found.\n"
        "AGENTS.md: archive/ is for reference only and MUST NOT be imported.\n"
        "To suppress: append `# hook: allow` to the line.\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
