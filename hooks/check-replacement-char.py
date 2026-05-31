"""Git hook: forbid the Unicode replacement character (U+FFFD) in committed files.

U+FFFD (?) appears when text is read with the wrong encoding and the
original bytes cannot be decoded.  Committing files that contain it
silently embeds garbled content — the intended character is lost and
readers see ?.

Scans .py, .md, .toml, .yml, and .yaml files under the configured
directories for the literal U+FFFD code point.

Suppression: append `# hook: allow` (Python/TOML) or `<!-- hook: allow -->`
(Markdown/YAML) to a line to exempt it.

No governing ADR — straightforward encoding hygiene.
"""
# no-adr: encoding hygiene; no governing ADR

import argparse
import sys
from pathlib import Path

_REPLACEMENT_CHAR = "\ufffd"
_PY_SUPPRESS = "# hook: allow"
_MD_SUPPRESS = "<!-- hook: allow -->"

_EXT_TO_SUPPRESS: dict[str, str] = {
    ".py": _PY_SUPPRESS,
    ".toml": _PY_SUPPRESS,
    ".yml": _MD_SUPPRESS,
    ".yaml": _MD_SUPPRESS,
    ".md": _MD_SUPPRESS,
}


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where U+FFFD is detected."""
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
                if _REPLACEMENT_CHAR not in line:
                    continue
                if suppress in line:
                    continue
                violations.append((path, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for the Unicode replacement character and report violations."""
    parser = argparse.ArgumentParser(
        description=(
            "Forbid the Unicode replacement character (U+FFFD) in committed files."
        ),
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
        "ERROR: Unicode replacement character (U+FFFD, \ufffd) found in committed files.\n"
        "This indicates a text encoding error -- the original character was lost\n"
        "when the file was read with the wrong codec.\n"
        "Fix: replace \ufffd with the intended character (often a hyphen-minus - or\n"
        "similar ASCII punctuation).\n"
        "To suppress a line: append `# hook: allow` (py/toml) or\n"
        "`<!-- hook: allow -->` (md/yml/yaml).\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
