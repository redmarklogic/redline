"""Git hook: forbid default values in environment variable lookups.

AGENTS.md (General Style) mandates that environment variables must not have
default values set in scripts. A default silently masks a misconfigured
environment and produces behaviour that is difficult to trace.

Use os.environ["VAR"] (raises KeyError on missing) or a required-lookup
helper instead of os.getenv("VAR", "fallback") or
os.environ.get("VAR", "fallback").

Scans .py files under the configured source directories.

Suppression: append `# hook: allow` to a line to exempt it.

AGENTS.md rule: "NEVER set default values for environment variables in
scripts (e.g., use os.environ.get('VAR') or a required helper, not
os.getenv('VAR', 'default')), unless explicitly asked to do so by the user."
"""
# no-adr: AGENTS.md style rule; no governing ADR

import argparse
import re
import sys
from pathlib import Path

# Match os.getenv("KEY", ...) or os.environ.get("KEY", ...) with a second arg.
# The pattern requires a string literal key followed by a comma, which
# indicates a default positional argument is present.
_ENV_DEFAULT_PATTERN = re.compile(
    r'\b(os\.getenv|os\.environ\.get)\s*\(\s*["\'][^"\']*["\']\s*,'
)
_SUPPRESS = "# hook: allow"


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where env default values are detected."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for py_file in sorted(directory.rglob("*.py")):
            lines = py_file.read_text(encoding="utf-8").splitlines()
            for lineno, line in enumerate(lines, start=1):
                if _SUPPRESS in line:
                    continue
                if _ENV_DEFAULT_PATTERN.search(line):
                    violations.append((py_file, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for env var default values in source directories."""
    parser = argparse.ArgumentParser(
        description="Forbid default values in env var lookups.",
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
        "ERROR: environment variable default values found.\n"
        "AGENTS.md: do not set default values for environment variables.\n"
        'Use os.environ["VAR"] or a required helper instead.\n'
        "To suppress: append `# hook: allow` to the line.\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
