r"""Git hook: forbid absolute user-home paths in committed files.

Absolute paths that contain a user's home directory (e.g.
``C:\\Users\\harel\\Documents\\...``) are machine-specific and must never be
committed.  They leak developer identity, break reproducibility, and prevent
team members from using the repository without manual path surgery.

Scans text files with common extensions under the configured source
directories for Windows-style user paths (``[A-Z]:\\Users\\<name>``).

Suppression: include ``hook: allow`` anywhere on a line to exempt it.

# no-adr: AGENTS.md style rule; no governing ADR
"""
# no-adr: AGENTS.md style rule; no governing ADR

import argparse
import re
import sys
from pathlib import Path

_USER_PATH_PATTERN = re.compile(r"(?i)[a-z]:[/\\]users[/\\]", re.IGNORECASE)
_SUPPRESS = "hook: allow"

_TEXT_EXTENSIONS = {
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
    ".json",
    ".rst",
    ".ps1",
    ".sh",
    ".cfg",
    ".ini",
}


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where user paths are detected."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for candidate in sorted(directory.rglob("*")):
            if not candidate.is_file():
                continue
            if candidate.suffix.lower() not in _TEXT_EXTENSIONS:
                continue
            try:
                lines = candidate.read_text(
                    encoding="utf-8", errors="replace"
                ).splitlines()
            except OSError:
                continue
            for lineno, line in enumerate(lines, start=1):
                if _SUPPRESS in line:
                    continue
                if _USER_PATH_PATTERN.search(line):
                    violations.append((candidate, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for absolute user-home paths in text files and report violations."""
    parser = argparse.ArgumentParser(
        description="Forbid absolute user-home paths in committed text files.",
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
        "ERROR: absolute user-home paths found.\n"
        "Committed files must not contain machine-specific paths such as\n"
        "C:\\Users\\<name>\\...  Replace with repo-relative or environment-\n"
        "variable-based paths.\n"
        "To suppress a specific line: add `hook: allow` anywhere on that line.\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
