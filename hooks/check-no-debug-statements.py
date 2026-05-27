"""Pre-commit hook: forbid debug instrumentation in committed code.

The version-control skill mandates that debug instrumentation must be
removed before committing. Committing breakpoint(), pdb, or ipdb calls
is a workflow violation — these are ephemeral development aids, not
production-ready code.

Scans .py files under the configured source directories for:
  - breakpoint()       (built-in soft debugger hook)
  - import pdb         (stdlib debugger import)
  - pdb.set_trace()    (stdlib debugger invocation)
  - import ipdb        (IPython debugger import)
  - ipdb.set_trace()   (IPython debugger invocation)

Suppression: append `# hook: allow` to a line to exempt it.

version-control skill rule: "Remove debug statements before committing."
"""
# no-adr: version-control skill rule; no governing ADR

import argparse
import re
import sys
from pathlib import Path

_DEBUG_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bbreakpoint\s*\("),
    re.compile(r"^\s*import pdb\b"),
    re.compile(r"\bpdb\.set_trace\s*\("),
    re.compile(r"^\s*import ipdb\b"),
    re.compile(r"\bipdb\.set_trace\s*\("),
]
_SUPPRESS = "# hook: allow"


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where debug statements are detected."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for py_file in sorted(directory.rglob("*.py")):
            lines = py_file.read_text(encoding="utf-8").splitlines()
            for lineno, line in enumerate(lines, start=1):
                if _SUPPRESS in line:
                    continue
                for pattern in _DEBUG_PATTERNS:
                    if pattern.search(line):
                        violations.append((py_file, lineno, line.strip()))
                        break
    return violations


def main() -> int:
    """Check for debug statements in source directories and report violations."""
    parser = argparse.ArgumentParser(
        description="Forbid debug instrumentation in committed source files.",
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
        "ERROR: debug statements found.\n"
        "version-control skill: remove breakpoint(), pdb, and ipdb calls\n"
        "before committing.\n"
        "To suppress: append `# hook: allow` to the line.\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
