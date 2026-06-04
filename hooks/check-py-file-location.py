"""Git hook: forbid .py files outside src/ and tests/.

AGENTS.md convention: Python source belongs in src/ (production) or tests/
(verification). Files in hooks/ are exempt because pre-commit hooks must
live there. Any .py file elsewhere is a misplacement that should be moved
or deleted.

Scans git-tracked files to find .py files in disallowed locations.

Suppression: not supported — move the file instead.

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


def find_violations() -> list[str]:
    """Return git-tracked .py file paths outside allowed directories."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    violations: list[str] = []
    for line in result.stdout.splitlines():
        path = line.strip()
        if not path:
            continue
        posix = PurePosixPath(path)
        if posix.suffix != ".py":
            continue
        if any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            continue
        violations.append(path)
    return violations


def main() -> int:
    """Check for .py files outside allowed directories and report violations."""
    violations = find_violations()
    if not violations:
        return 0

    print(
        "ERROR: .py files found outside src/ and tests/.\n"
        "Python files must live in src/ (production) or tests/ (verification).\n"
        "hooks/ is exempt. Move or delete the offending files.\n",
        file=sys.stderr,
    )
    for path in sorted(violations):
        print(f"  {path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
