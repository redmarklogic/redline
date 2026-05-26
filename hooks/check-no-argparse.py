"""Pre-commit hook: forbid argparse usage in project source code.

AGENTS.md (General Style) mandates that project scripts are configured via
environment variables or constants, not CLI argument parsers. argparse is a
CLI tool abstraction that introduces accidental complexity into library and
data pipeline code.

Scans .py files under the configured source directories and fails if any
line imports the argparse module.

Suppression: append `# hook: allow` to a line to exempt it.

AGENTS.md rule: "NEVER import argparse."
"""
# no-adr: AGENTS.md style rule; no governing ADR

import argparse
import re
import sys
from pathlib import Path

_ARGPARSE_PATTERN = re.compile(r"^\s*(import argparse\b|from argparse import\b)")
_SUPPRESS = "# hook: allow"


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where argparse usage is detected."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for py_file in sorted(directory.rglob("*.py")):
            lines = py_file.read_text(encoding="utf-8").splitlines()
            for lineno, line in enumerate(lines, start=1):
                if _SUPPRESS in line:
                    continue
                if _ARGPARSE_PATTERN.search(line):
                    violations.append((py_file, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for argparse usage in source directories and report violations."""
    parser = argparse.ArgumentParser(
        description="Forbid argparse imports in source directories.",
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
        "ERROR: argparse imports found.\n"
        "AGENTS.md: configure scripts via environment variables or constants;\n"
        "do not use argparse.\n"
        "To suppress: append `# hook: allow` to the line.\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
