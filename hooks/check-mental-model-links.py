"""Git hook: enforce Markdown links for mental-model path references.

Scans .md files for backtick code spans that contain a path into the
mental-models skill directory (e.g. `mental-models/strategic_decisions/rice.md`).
These paths must be Markdown links so that VS Code can auto-load the referenced
file into context (requires `chat.includeReferencedInstructions: true`).

WRONG  — code span, not loadable by VS Code:
  `mental-models/strategic_decisions/rice.md`

CORRECT — Markdown link, auto-loadable:
  [RICE](../mental-models/strategic_decisions/rice.md)

Suppression: append `<!-- mental-model-link: allow -->` to the line.

See docs/adr/adr-009-skill-taxonomy-and-governance-registry.md and
.agents/skills/mental-models/SKILL.md for context.
"""

# no-adr: enforces .vscode/settings.json + mental-models skill conventions;
# governed by .agents/skills/mental-models/SKILL.md.

import argparse
import os
import re
import sys
from pathlib import Path

_SUPPRESS = "<!-- mental-model-link: allow -->"

# Matches a backtick code span whose content includes a mental-models path.
# E.g. `mental-models/strategic_decisions/rice.md`
_BACKTICK_MENTAL_MODEL = re.compile(r"`([^`]*mental-models/[^`]*\.md[^`]*)`")

# Opening/closing fences (``` or ~~~, with optional language tag).
_FENCE_OPEN = re.compile(r"^(`{3,}|~{3,})")


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str, str]]:
    """Return (file, lineno, line, suggestion) tuples for each violation.

    A violation is a backtick code span containing a mental-models path that
    should instead be a Markdown link.
    """
    violations: list[tuple[Path, int, str, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for md_file in sorted(directory.rglob("*.md")):
            text = _read_text(md_file)
            if text is None:
                continue
            in_fence = False
            for lineno, line in enumerate(text.splitlines(), start=1):
                stripped = line.strip()
                # Track fenced code blocks; paths inside them are examples.
                if _FENCE_OPEN.match(stripped):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                if _SUPPRESS in line:
                    continue
                for match in _BACKTICK_MENTAL_MODEL.finditer(line):
                    raw_path = match.group(1).strip()
                    suggestion = _suggest_fix(raw_path, md_file)
                    violations.append((md_file, lineno, line.strip(), suggestion))
                    break  # one violation per line is enough
    return violations


def _suggest_fix(raw_path: str, source_file: Path) -> str:
    """Build a concrete fix suggestion from the bare path and source file location.

    Computes the correct relative path from the source file's directory to the
    actual mental-model file, so the suggestion is actionable regardless of
    where in the repo the source file lives.
    """
    # Normalise: strip leading ../ to get the repo-root-relative path
    normalised = re.sub(r"^(\.\./)*", "", raw_path)
    # Locate the actual target file from the repo root
    if normalised.startswith(".agents/"):
        target = Path(normalised)
    else:
        target = Path(".agents/skills") / normalised
    # Compute the relative path from the source file's directory
    rel = os.path.relpath(target, source_file.parent).replace("\\", "/")
    stem = Path(normalised).stem
    title = stem.replace("-", " ").title()
    return f"[{title}]({rel})"


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Enforce Markdown links for mental-model path references.",
    )
    parser.add_argument(
        "--dirs",
        action="append",
        default=[],
        help="Directory to scan recursively (may be repeated).",
    )
    args = parser.parse_args()

    violations = find_violations([Path(d) for d in args.dirs])
    if not violations:
        return 0

    print(
        "ERROR: mental-model path(s) written as backtick code spans instead of "
        "Markdown links.\n"
        "\n"
        "VS Code can only auto-load referenced files when they are Markdown links.\n"
        "Backtick code spans are inert text — the file is never added to context.\n"
        "\n"
        "HOW TO FIX: replace the backtick span with a Markdown link.\n"
        "  WRONG:   `mental-models/strategic_decisions/rice.md`\n"
        "  CORRECT: [Rice](../mental-models/strategic_decisions/rice.md)\n"
        "\n"
        "TO SUPPRESS (e.g. inside a 'do not do this' example): append\n"
        "  <!-- mental-model-link: allow -->  to the line.\n",
        file=sys.stderr,
    )
    for path, lineno, line, suggestion in violations:
        print(f"  {path}:{lineno}", file=sys.stderr)
        print(f"    Line   : {line}", file=sys.stderr)
        print(f"    Fix as : {suggestion}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
