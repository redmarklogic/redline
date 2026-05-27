"""Check that specified file sets do not contain banned words.

Scans Python hook scripts (--hooks-dir) and/or Markdown skill files
(--md-dir) for occurrences of words that should not appear.

For hook scripts: enforces ADR-011 P4 — hook bodies must be generic;
project-specific values live in configuration.

For skill Markdown files: enforces ADR-010 — skills must not reference
agent names (dependency-direction invariant; outer agents depend on inner
skills, never the reverse).

Suppression:
  Python files:   append `# hook: allow` to the line
  Markdown files: append `<!-- hook: allow -->` to the line

See ADR-010 and ADR-011 P4 (docs/adr/).
"""

import argparse
import re
import sys
from pathlib import Path

_PY_SUPPRESS = "# hook: allow"
_MD_SUPPRESS = "<!-- hook: allow -->"


def _check_py_files(
    hooks_dir: Path,
    patterns: list[re.Pattern[str]],
    own_name: str,
) -> list[str]:
    violations: list[str] = []
    for py_file in sorted(hooks_dir.glob("*.py")):
        if py_file.name == own_name:
            continue
        lines = py_file.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            if _PY_SUPPRESS in line:
                continue
            for pattern in patterns:
                if pattern.search(line):
                    violations.append(f"  {py_file}:{lineno}: {line.strip()}")
                    break
    return violations


def _check_md_files(
    md_dir: Path,
    patterns: list[re.Pattern[str]],
) -> list[str]:
    violations: list[str] = []
    for md_file in sorted(md_dir.rglob("*.md")):
        lines = md_file.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            if _MD_SUPPRESS in line:
                continue
            for pattern in patterns:
                if pattern.search(line):
                    violations.append(f"  {md_file}:{lineno}: {line.strip()}")
                    break
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that file sets do not contain banned words.",
    )
    parser.add_argument(
        "--hooks-dir",
        default=None,
        help="Path to the hooks directory to scan for banned words in .py files.",
    )
    parser.add_argument(
        "--md-dir",
        action="append",
        default=[],
        dest="md_dirs",
        help="Directory to scan recursively for banned words in .md files (repeatable).",
    )
    parser.add_argument(
        "words",
        nargs="+",
        help="Words to ban.",
    )
    args = parser.parse_args()

    if not args.hooks_dir and not args.md_dirs:
        print("ERROR: supply --hooks-dir and/or --md-dir.", file=sys.stderr)
        return 1

    banned: list[str] = args.words
    patterns = [
        re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE) for word in banned
    ]

    violations: list[str] = []

    if args.hooks_dir:
        hooks_dir = Path(args.hooks_dir)
        if not hooks_dir.is_dir():
            print(f"ERROR: {hooks_dir} is not a directory.", file=sys.stderr)
            return 1
        violations += _check_py_files(hooks_dir, patterns, Path(__file__).name)

    for md_dir_str in args.md_dirs:
        md_dir = Path(md_dir_str)
        if not md_dir.is_dir():
            print(f"ERROR: {md_dir} is not a directory.", file=sys.stderr)
            return 1
        violations += _check_md_files(md_dir, patterns)

    if violations:
        print(
            "ERROR: Banned word(s) found. See ADR-010 and ADR-011 P4.",
            file=sys.stderr,
        )
        for v in violations:
            print(v, file=sys.stderr)
        return 1

    print("No banned words found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
