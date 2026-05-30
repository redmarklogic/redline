"""Git hook: forbid custom .env file loaders in project source code.

AGENTS.md (General Style) mandates that the environment is assumed to be
correctly configured by the caller (shell, orchestrator, or container).
Custom .env loaders such as load_dotenv() from python-dotenv couple scripts
to a specific deployment convention and introduce accidental complexity.

Scans .py files under the configured source directories.

Suppression: append `# hook: allow` to a line to exempt it.

AGENTS.md rule: "NEVER implement custom environment loaders (e.g., manual
.env file parsers). Assume the environment is correctly configured by the
caller."
"""
# no-adr: AGENTS.md style rule; no governing ADR

import argparse
import re
import sys
from pathlib import Path

_ENV_LOADER_PATTERN = re.compile(
    r"\b(load_dotenv\s*\(|from\s+dotenv\s+import|import\s+dotenv\b|dotenv\.load)"
)
_SUPPRESS = "# hook: allow"


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where .env loader usage is detected."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for py_file in sorted(directory.rglob("*.py")):
            lines = py_file.read_text(encoding="utf-8").splitlines()
            for lineno, line in enumerate(lines, start=1):
                if _SUPPRESS in line:
                    continue
                if _ENV_LOADER_PATTERN.search(line):
                    violations.append((py_file, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for .env loader usage in source directories and report violations."""
    parser = argparse.ArgumentParser(
        description="Forbid .env loader imports in source directories.",
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
        "ERROR: custom .env loader usage found.\n"
        "AGENTS.md: assume the environment is configured by the caller;\n"
        "do not implement custom .env loaders (load_dotenv, python-dotenv, etc.).\n"
        "To suppress: append `# hook: allow` to the line.\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
