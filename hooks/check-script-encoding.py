"""Git hook: forbid scripts Windows PowerShell 5.1 cannot read safely.

Windows PowerShell 5.1 reads a script that has no UTF-8 byte-order mark (BOM)
using the ANSI code page (CP1252), not UTF-8. Any non-ASCII byte sequence is then
mis-decoded: multibyte punctuation such as an em-dash (U+2014) becomes a smart
quote (U+201D) that PowerShell treats as a string delimiter, producing a parse
error far from the offending character. scan.ps1 hit exactly this failure.

Rule:
  - .ps1 files must be pure ASCII, OR begin with a UTF-8 BOM (which makes
    PowerShell 5.1 decode them as UTF-8).
  - .sh files must be pure ASCII (bash needs no BOM; ASCII also avoids the same
    copy-paste smart-punctuation accident).

Scans .ps1/.sh files found under the configured --dirs and the explicit --files.

Suppression: append `# hook: allow` to a line to exempt it.
"""
# no-adr: PowerShell 5.1 encoding-safety convention; no governing ADR

import argparse
import sys
from pathlib import Path

_SUPPRESS = "# hook: allow"
_UTF8_BOM = b"\xef\xbb\xbf"
_MAX_ASCII = 0x7E


def _has_utf8_bom(path: Path) -> bool:
    """Return True if the file begins with a UTF-8 byte-order mark."""
    with path.open("rb") as handle:
        return handle.read(3) == _UTF8_BOM


def _scan_file(path: Path) -> list[tuple[Path, int, int, int]]:
    """Return (file, line, column, codepoint) for each disallowed character."""
    # A .ps1 with a UTF-8 BOM is decoded correctly by PowerShell 5.1 -> allowed.
    if path.suffix.lower() == ".ps1" and _has_utf8_bom(path):
        return []
    violations: list[tuple[Path, int, int, int]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), start=1):
        if _SUPPRESS in line:
            continue
        for col, char in enumerate(line, start=1):
            if ord(char) > _MAX_ASCII:
                violations.append((path, lineno, col, ord(char)))
    return violations


def find_violations(
    dirs: list[Path], files: list[Path]
) -> list[tuple[Path, int, int, int]]:
    """Return all non-ASCII violations across --dirs (recursive) and --files."""
    targets: list[Path] = []
    for directory in dirs:
        if directory.is_dir():
            targets.extend(sorted(directory.rglob("*.ps1")))
            targets.extend(sorted(directory.rglob("*.sh")))
    for file in files:
        if file.is_file() and file.suffix.lower() in (".ps1", ".sh"):
            targets.append(file)

    violations: list[tuple[Path, int, int, int]] = []
    for path in targets:
        violations.extend(_scan_file(path))
    return violations


def main() -> int:
    """Check scripts for PowerShell-5.1-unsafe encoding and report violations."""
    parser = argparse.ArgumentParser(
        description="Forbid non-ASCII (no-BOM) PowerShell/shell scripts.",
    )
    parser.add_argument(
        "--dirs",
        action="append",
        default=[],
        help="Directory to scan (may be repeated).",
    )
    parser.add_argument(
        "--files",
        action="append",
        default=[],
        help="Explicit file to scan (may be repeated).",
    )
    args = parser.parse_args()

    violations = find_violations(
        [Path(d) for d in args.dirs], [Path(f) for f in args.files]
    )
    if not violations:
        return 0

    print(
        "ERROR: non-ASCII character(s) in a script Windows PowerShell 5.1 cannot\n"
        "read without a UTF-8 BOM (the byte is mis-decoded as a smart quote and\n"
        "breaks parsing). Use ASCII (e.g. '-' not an em-dash), or save the .ps1\n"
        "with a UTF-8 BOM. To suppress a line: append `# hook: allow`.\n",
        file=sys.stderr,
    )
    for path, lineno, col, codepoint in violations:
        print(f"  {path}:{lineno}:{col}: U+{codepoint:04X}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
