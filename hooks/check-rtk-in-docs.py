"""Git hook: check RTK prefix enforcement in Markdown documentation.

Scans .md and .qmd files for fenced code blocks with shell commands and
flags any RTK-eligible command that lacks the ``rtk`` prefix.

RTK is a CLI proxy that filters and compresses command outputs, saving
60-90% tokens. Instruction, skill, and agent files must show the
``rtk``-prefixed form so that agents learn the correct pattern.

Suppression: place ``<!-- rtk:skip -->`` on the line immediately before
a fenced code block to exempt it.

See .github/instructions/rtk.instructions.md for the full rule.
"""
# no-adr: rtk.instructions.md governs this convention; no project ADR

import argparse  # hook: allow
import re
import sys
from pathlib import Path

RTK_ELIGIBLE_COMMANDS: frozenset[str] = frozenset(
    {
        "git",
        "pytest",
        "ruff",
        "docker",
        "uv",
        "pip",
        "mypy",
        "prek",
    }
)

_FENCE_OPEN = re.compile(r"^```(bash|sh|shell|console|powershell)\s*$")
_FENCE_CLOSE = re.compile(r"^```\s*$")
_NON_SHELL_LANG = re.compile(
    r"^```(python|py|json|yaml|yml|toml|javascript|js|typescript|ts|sql|html|css|xml|mermaid|text|plaintext|ini|cfg|markdown|md|r|ruby|go|java|c|cpp|csharp|dockerfile|makefile|hcl|terraform)\s*$"
)
_SUPPRESSION = "<!-- rtk:skip -->"


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _extract_first_command(line: str) -> str | None:
    """Extract the first token from a shell command line.

    Returns None for blank lines, comments, variable assignments,
    and continuation lines.
    """
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or stripped.startswith("//"):
        return None
    # Skip variable assignments like FOO=bar
    if re.match(r"^[A-Z_]+=", stripped):
        return None
    # Skip continuation lines
    if stripped.startswith("|") or stripped.startswith("&"):
        return None
    # Handle env-var-prefixed commands: VAR=val cmd ...
    tokens = stripped.split()
    for token in tokens:
        if "=" in token and not token.startswith("-"):
            continue
        return token
    return None


def _check_file(path: Path) -> list[tuple[int, str, str]]:  # noqa: PLR0912,PLR0915
    """Return (lineno, command_line, suggestion) for each violation."""
    violations: list[tuple[int, str, str]] = []
    text = _read_text(path)
    if text is None:
        return violations

    lines = text.splitlines()
    in_shell_block = False
    in_skip_block = False
    skip_next_block = False

    for lineno_0, line in enumerate(lines):
        lineno = lineno_0 + 1
        stripped = line.strip()

        if in_skip_block:
            if _FENCE_CLOSE.match(stripped):
                in_skip_block = False
            continue

        if not in_shell_block:
            if stripped == _SUPPRESSION:
                skip_next_block = True
                continue

            if _NON_SHELL_LANG.match(stripped):
                # Explicitly non-shell block; skip entirely
                in_skip_block = True
                skip_next_block = False
                continue

            if _FENCE_OPEN.match(stripped):
                if skip_next_block:
                    in_skip_block = True
                    skip_next_block = False
                    continue
                in_shell_block = True
                skip_next_block = False
                continue

            # Untagged code block (``` with no language tag) — treat as shell-eligible
            if _FENCE_CLOSE.match(stripped):
                if skip_next_block:
                    in_skip_block = True
                    skip_next_block = False
                    continue
                in_shell_block = True
                skip_next_block = False
                continue

            # Reset skip flag if non-fence, non-suppression line encountered
            if stripped and not stripped.startswith("<!--"):
                skip_next_block = False
            continue

        # Inside a shell code block
        if _FENCE_CLOSE.match(stripped):
            in_shell_block = False
            continue

        first_cmd = _extract_first_command(line)
        if first_cmd is None:
            continue

        # Already prefixed with rtk
        if first_cmd == "rtk":
            continue

        # Check if this command is RTK-eligible
        if first_cmd in RTK_ELIGIBLE_COMMANDS:
            suggestion = f"rtk {stripped}"
            violations.append((lineno, stripped, suggestion))

    return violations


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str, str]]:
    """Return (file, lineno, command, suggestion) for every violation."""
    violations: list[tuple[Path, int, str, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for pattern in ("*.md", "*.qmd"):
            for md_file in sorted(directory.rglob(pattern)):
                for lineno, cmd, suggestion in _check_file(md_file):
                    violations.append((md_file, lineno, cmd, suggestion))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(  # hook: allow
        description="Check RTK prefix enforcement in Markdown shell code blocks.",
    )
    parser.add_argument(
        "--dirs",
        action="append",
        default=[],
        help="Directory to scan (may be repeated).",
    )
    args = parser.parse_args()

    dirs = [Path(d) for d in args.dirs]
    violations = find_violations(dirs)
    if not violations:
        return 0

    print(
        "ERROR: shell commands missing 'rtk' prefix in documentation.\n"
        "RTK is a CLI proxy that saves 60-90%% tokens. Prefix eligible\n"
        "commands with 'rtk'. To suppress: add `<!-- rtk:skip -->` on the\n"
        "line before the code block.\n",
        file=sys.stderr,
    )
    for path, lineno, cmd, suggestion in violations:
        print(f"  {path}:{lineno}: {cmd}", file=sys.stderr)
        print(f"    suggestion: {suggestion}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
