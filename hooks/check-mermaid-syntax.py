"""Git hook: check Mermaid diagram blocks for syntax that breaks v8.8.0.

Scans .md and .qmd files for Mermaid fenced code blocks and flags:

1. Em-dash (\u2014, U+2014) or en-dash (\u2013, U+2013) anywhere inside the block.
   These break the 8.8.0 tokeniser even inside quoted strings.

2. Wildcard (*) inside node label brackets [...].
   Glob-style abbreviations (e.g. eda-*) are not valid Mermaid label characters
   and cause a syntax error.

Suppression: append `<!-- mermaid: allow -->` to a line to exempt it.

See .agents/skills/mermaid-diagrams/procedures/syntax.md for the full rules.
"""

# no-adr: Mermaid diagram syntax conventions are governed by
# .agents/skills/mermaid-diagrams/SKILL.md, not a project ADR.

import argparse
import sys
from pathlib import Path

_SUPPRESS = "<!-- mermaid: allow -->"
_MERMAID_OPEN = "```mermaid"
_MERMAID_CLOSE = "```"
_EM_DASH = "\u2014"
_EN_DASH = "\u2013"


def _read_text(path: Path) -> str | None:
    """Return file contents, or None if the file cannot be read."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _has_wildcard_in_brackets(line: str) -> bool:
    """Return True if line contains a glob wildcard (*) inside [...] brackets.

    Exception: ``[*]`` is a valid stateDiagram start/end state token and is
    not flagged.
    """
    in_bracket = False
    bracket_content: list[str] = []
    for ch in line:
        if ch == "[":
            in_bracket = True
            bracket_content = []
        elif ch == "]":
            if in_bracket and "*" in bracket_content and bracket_content != ["*"]:
                return True
            in_bracket = False
            bracket_content = []
        elif in_bracket:
            bracket_content.append(ch)
    return False


def _check_file(path: Path) -> list[tuple[int, str, str, str]]:
    """Return (lineno, line, violation_type, reason) for each violation.

    violation_type is one of:
      "dash"     — em/en-dash; auto-fixable with --fix
      "wildcard" — * inside brackets; requires manual rename
    """
    violations: list[tuple[int, str, str, str]] = []
    in_mermaid = False

    text = _read_text(path)
    if text is None:
        return violations

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()

        if not in_mermaid:
            if stripped == _MERMAID_OPEN:
                in_mermaid = True
            continue

        if stripped == _MERMAID_CLOSE:
            in_mermaid = False
            continue

        if _SUPPRESS in line:
            continue

        # Check 1: em-dash or en-dash (never valid anywhere in a Mermaid block).
        if _EM_DASH in line:
            violations.append(
                (
                    lineno,
                    stripped,
                    "dash",
                    "em-dash (\u2014) breaks the 8.8.0 tokeniser",
                )
            )
            continue
        if _EN_DASH in line:
            violations.append(
                (
                    lineno,
                    stripped,
                    "dash",
                    "en-dash (\u2013) breaks the 8.8.0 tokeniser",
                )
            )
            continue

        # Check 2: wildcard (*) inside node label brackets [...].
        if _has_wildcard_in_brackets(line):
            violations.append(
                (
                    lineno,
                    stripped,
                    "wildcard",
                    "wildcard (*) inside node label brackets is not valid Mermaid syntax",
                )
            )

    return violations


def fix_file(path: Path) -> bool:
    """Replace em/en-dashes with hyphens inside Mermaid blocks in-place.

    Returns True if any changes were made, False otherwise.
    Wildcards are not auto-fixable and are left untouched.
    """
    raw = _read_text(path)
    if raw is None:
        return False
    lines = raw.splitlines(keepends=True)
    in_mermaid = False
    changed = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not in_mermaid:
            if stripped == _MERMAID_OPEN:
                in_mermaid = True
            continue
        if stripped == _MERMAID_CLOSE:
            in_mermaid = False
            continue
        if _SUPPRESS in line:
            continue
        if _EM_DASH in line or _EN_DASH in line:
            lines[i] = line.replace(_EM_DASH, "-").replace(_EN_DASH, "-")
            changed = True

    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str, str, str]]:
    """Return (file, lineno, line, violation_type, reason) for every violation."""
    violations: list[tuple[Path, int, str, str, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for pattern in ("*.md", "*.qmd"):
            for md_file in sorted(directory.rglob(pattern)):
                for lineno, line, vtype, reason in _check_file(md_file):
                    violations.append((md_file, lineno, line, vtype, reason))
    return violations


def main() -> int:  # noqa: PLR0912
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Check Mermaid blocks for syntax patterns that break v8.8.0.",
    )
    parser.add_argument(
        "--dirs",
        action="append",
        default=[],
        help="Directory to scan (may be repeated).",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-replace em/en-dashes with plain hyphens inside Mermaid blocks.",
    )
    args = parser.parse_args()

    dirs = [Path(d) for d in args.dirs]

    if args.fix:
        fixed_files: list[Path] = []
        for directory in dirs:
            if not directory.is_dir():
                continue
            for pattern in ("*.md", "*.qmd"):
                for md_file in sorted(directory.rglob(pattern)):
                    if fix_file(md_file):
                        fixed_files.append(md_file)
        if fixed_files:
            print(
                f"check-mermaid-syntax --fix: repaired em/en-dashes in {len(fixed_files)} file(s)"
            )
            for f in fixed_files:
                print(f"  {f}")

    violations = find_violations(dirs)
    if not violations:
        return 0

    n = len(violations)
    dash_count = sum(1 for *_, vtype, _ in violations if vtype == "dash")
    wildcard_count = n - dash_count

    print(
        f"check-mermaid-syntax: {n} violation(s) found ({dash_count} auto-fixable, {wildcard_count} manual)\n"
    )

    # Group by file for readability.
    current_file: Path | None = None
    for file, lineno, line, vtype, reason in violations:
        if file != current_file:
            print(f"  {file}")
            current_file = file
        if vtype == "dash":
            fixed_line = line.replace(_EM_DASH, "-").replace(_EN_DASH, "-")
            print(f"    line {lineno}  [dash - auto-fixable]")
            print(f"      PROBLEM : {reason}")
            print(f"      BEFORE  : {line}")
            print(f"      AFTER   : {fixed_line}")
        else:
            print(f"    line {lineno}  [wildcard - manual fix required]")
            print(f"      PROBLEM : {reason}")
            print(f"      FOUND   : {line}")
            print(
                "      ACTION  : Replace * with explicit skill names, e.g. [eda-codebook / eda-qa] not [eda-*]"
            )
        print()

    print("─" * 60)
    if dash_count:
        dir_args = " ".join(f"--dirs={d}" for d in args.dirs)
        print(
            f"Auto-fix dashes : uv run hooks/check-mermaid-syntax.py --fix {dir_args}"
        )
    if wildcard_count:
        print("Manual wildcards: spell out each skill name inside [...] brackets")
    print("Suppress a line : append <!-- mermaid: allow --> to it")
    print("Skill reference : .agents/skills/mermaid-diagrams/procedures/syntax.md")
    return 1


if __name__ == "__main__":
    sys.exit(main())
