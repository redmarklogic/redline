"""Git hook: enforce .py file location and naming conventions.

Two rules:

1. Location — Python source belongs in src/ (production) or tests/
   (verification). Files in hooks/ are exempt. Any .py file elsewhere is a
   misplacement that should be moved or deleted.

2. Naming — module filenames must not start with a single underscore.
   Double-underscore names (e.g. __init__.py, __main__.py) are fine.
   Single-underscore names (e.g. _helpers.py) signal private/internal
   modules and inflate SonarQube's noise surface; use a plain name instead.

Suppression: not supported — rename or move the file instead.

AGENTS.md rule: Python files belong in src/ or tests/.
"""
# no-adr: AGENTS.md architectural rule; no governing ADR

import subprocess
import sys
from pathlib import PurePosixPath

ALLOWED_PREFIXES = (
    "src/",
    "tests/",
    "hooks/",
    ".agents/tools/",
    "scripts/",
    ".github/scripts/",
)


def _tracked_py_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip() and PurePosixPath(line.strip()).suffix == ".py"
    ]


def find_location_violations(paths: list[str]) -> list[str]:
    """Return paths outside allowed directories."""
    return [p for p in paths if not any(p.startswith(pfx) for pfx in ALLOWED_PREFIXES)]


def find_naming_violations(paths: list[str]) -> list[str]:
    """Return paths whose filename starts with exactly one underscore."""
    violations = []
    for path in paths:
        stem = PurePosixPath(path).name
        if stem.startswith("_") and not stem.startswith("__"):
            violations.append(path)
    return violations


def main() -> int:
    """Check location and naming conventions for all tracked .py files."""
    paths = _tracked_py_files()
    location_violations = find_location_violations(paths)
    naming_violations = find_naming_violations(paths)

    ok = True

    if location_violations:
        ok = False
        print(
            "ERROR: .py files found outside src/ and tests/.\n"
            "Python files must live in src/ (production) or tests/ (verification).\n"
            "hooks/ is exempt. Move or delete the offending files.\n",
            file=sys.stderr,
        )
        for path in sorted(location_violations):
            print(f"  {path}", file=sys.stderr)

    if naming_violations:
        ok = False
        print(
            "ERROR: .py files with single-underscore names found.\n"
            "Single-underscore module names (e.g. _helpers.py) are forbidden.\n"
            "Use a plain name instead. Double-underscore names (__init__.py) are fine.\n",
            file=sys.stderr,
        )
        for path in sorted(naming_violations):
            print(f"  {path}", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
