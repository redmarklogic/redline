"""Git hook: forbid emoji and emoji-like Unicode in committed files.

Scans .py, .md, .toml, .yml, and .yaml files for emoji characters and
Unicode symbols that emulate emoji (checkmarks, crosses, stars, etc.).

This replaces the prose instruction in AGENTS.md with an automated check.
Exception: tests for multibyte characters can suppress with the standard
marker.

Suppression: append `# hook: allow` (Python/TOML) or `<!-- hook: allow -->`
(Markdown/YAML) to a line to exempt it.

No governing ADR -- style convention enforcement.
"""
# no-adr: style convention; no governing ADR

import argparse
import re
import sys
from pathlib import Path

_PY_SUPPRESS = "# hook: allow"
_MD_SUPPRESS = "<!-- hook: allow -->"

_EXT_TO_SUPPRESS: dict[str, str] = {
    ".py": _PY_SUPPRESS,
    ".toml": _PY_SUPPRESS,
    ".yml": _MD_SUPPRESS,
    ".yaml": _MD_SUPPRESS,
    ".md": _MD_SUPPRESS,
}

# --- Emoji and emoji-like character patterns ---
# True emoji: Emoticons, Misc Symbols & Pictographs, Transport & Map,
# Supplemental Symbols, Flags, Dingbats subset
_EMOJI_RANGES = (
    "\U0001f600-\U0001f64f"  # Emoticons
    "\U0001f300-\U0001f5ff"  # Misc Symbols and Pictographs
    "\U0001f680-\U0001f6ff"  # Transport and Map
    "\U0001f900-\U0001f9ff"  # Supplemental Symbols and Pictographs
    "\U0001fa00-\U0001fa6f"  # Chess Symbols
    "\U0001fa70-\U0001faff"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027b0"  # Dingbats
)

# Emoji-like Unicode: checkmarks, crosses, stars, bullets that emulate emoji
_EMOJI_LIKE = (
    "\u2713"  # CHECK MARK  # hook: allow
    "\u2714"  # HEAVY CHECK MARK  # hook: allow
    "\u2715"  # MULTIPLICATION X  # hook: allow
    "\u2716"  # HEAVY MULTIPLICATION X  # hook: allow
    "\u2717"  # BALLOT X  # hook: allow
    "\u2718"  # HEAVY BALLOT X  # hook: allow
    "\u2705"  # (emoji check)  # hook: allow
    "\u274c"  # (emoji cross)  # hook: allow
    "\u274e"  # (emoji cross variant)  # hook: allow
    "\u2728"  # SPARKLES  # hook: allow
    "\u2b50"  # WHITE MEDIUM STAR  # hook: allow
    "\u2b55"  # HEAVY LARGE CIRCLE  # hook: allow
    "\u26a0"  # WARNING SIGN  # hook: allow
    "\u26d4"  # NO ENTRY  # hook: allow
    "\u2757"  # HEAVY EXCLAMATION MARK  # hook: allow
    "\u2753"  # QUESTION MARK ORNAMENT  # hook: allow
    "\u2755"  # LIGHT EXCLAMATION MARK  # hook: allow
    "\u203c"  # DOUBLE EXCLAMATION MARK  # hook: allow
    "\u2049"  # EXCLAMATION QUESTION MARK  # hook: allow
)

_PATTERN = re.compile(f"[{_EMOJI_RANGES}{re.escape(_EMOJI_LIKE)}]")

# Global character exceptions — allowed everywhere without per-line suppression
_ALLOWED_CHARS: frozenset[str] = frozenset(
    {
        "\u2705",  # ✅ WHITE HEAVY CHECK MARK  # hook: allow
        "\u274c",  # ❌ CROSS MARK  # hook: allow
        "\u2713",  # ✓ CHECK MARK  # hook: allow
        "\u26a0",  # ⚠️ WARNING SIGN  # hook: allow
    }
)


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where emoji is detected."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file():
                continue
            suppress = _EXT_TO_SUPPRESS.get(path.suffix)
            if suppress is None:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if not _PATTERN.search(line):
                    continue
                if suppress in line:
                    continue
                if all(ch in _ALLOWED_CHARS for ch in _PATTERN.findall(line)):
                    continue
                violations.append((path, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for emoji and report violations."""
    parser = argparse.ArgumentParser(
        description="Forbid emoji and emoji-like Unicode in committed files.",
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
        "ERROR: Emoji or emoji-like Unicode found in committed files.\n"
        "Use plain ASCII alternatives instead (e.g. [x] not checkmark,\n"
        "PASS/FAIL not checkmark/cross).\n"
        "To suppress a line: append `# hook: allow` (py/toml) or\n"
        "`<!-- hook: allow -->` (md/yml/yaml).\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
