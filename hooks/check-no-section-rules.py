"""Git hook: forbid section-rule comment separator lines in Python code.

AGENTS.md (General Style) explicitly forbids section separator comment lines
such as:

    # ---------------------------------------------------------------------------

These decorative horizontal rules add visual noise without conveying
information, make diffs noisier, and are inconsistent with clean,
minimal Python style.

Scans .py files under the configured source directories for comment lines
consisting of four or more consecutive dashes.

Suppression: append `# hook: allow` to a line to exempt it.

AGENTS.md rule: "NEVER introduce section rules, e.g.
# ---------------------------------------------------------------------------"
"""
# no-adr: AGENTS.md style rule; no governing ADR

import argparse
import re
import sys
from pathlib import Path

_SECTION_RULE_PATTERN = re.compile(r"^\s*#\s*-{4,}")
_SUPPRESS = "# hook: allow"


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where section rules are detected."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for py_file in sorted(directory.rglob("*.py")):
            lines = py_file.read_text(encoding="utf-8").splitlines()
            for lineno, line in enumerate(lines, start=1):
                if _SUPPRESS in line:
                    continue
                if _SECTION_RULE_PATTERN.search(line):
                    violations.append((py_file, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for section-rule comment separators and report violations."""
    parser = argparse.ArgumentParser(
        description="Forbid section-rule comment separator lines in Python files.",
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
        "ERROR: section-rule comment separator lines found.\n"
        "AGENTS.md: do not introduce decorative section separator comments\n"
        "(e.g. # ---...). Remove or replace with a blank line.\n"
        "To suppress: append `# hook: allow` to the line.\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
