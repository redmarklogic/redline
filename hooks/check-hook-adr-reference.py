"""Git hook: verify that hook scripts reference their governing ADR.

ADR-011 P6 mandates that every hook script enforcing a principle with a
corresponding ADR must:

1. Include a module-level docstring.
2. Reference the governing ADR by number (e.g. "See ADR-011") in that
   docstring.
3. Emit the ADR reference in its error message so developers can trace
   enforcement back to the decision that justifies it.

Hooks that enforce purely technical constraints without a governing ADR are
exempt from the ADR-reference requirement but must still carry a module
docstring. To declare an exemption, include a `# no-adr: <reason>` comment
anywhere in the file.

This hook applies to all .py files in the configured hooks directory,
including itself.

See ADR-011 P6 (docs/adr/adr-011-hook-first-enforcement.md).
"""

import argparse
import ast
import re
import sys
from pathlib import Path

_ADR_PATTERN = re.compile(r"\bADR-\d+\b")
_NO_ADR_PATTERN = re.compile(r"#\s*no-adr\s*:")


def _check_file(py_file: Path) -> str | None:
    """Return an error message if the file fails the ADR-reference gate."""
    source = py_file.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return f"{py_file}: SyntaxError — {exc}"

    docstring = ast.get_docstring(tree)

    if not docstring:
        return f"{py_file}: missing module docstring (required by ADR-011 P6)"

    if _ADR_PATTERN.search(docstring):
        return None

    # No ADR reference — check for explicit exemption.
    if _NO_ADR_PATTERN.search(source):
        return None

    return (
        f"{py_file}: module docstring has no ADR reference and no "
        f"`# no-adr: <reason>` exemption (ADR-011 P6)"
    )


def main() -> int:
    """Check hook scripts for module docstrings and ADR references."""
    parser = argparse.ArgumentParser(
        description="Verify hook scripts reference their governing ADR.",
    )
    parser.add_argument(
        "--hooks-dir",
        required=True,
        help="Path to the hooks directory to scan.",
    )
    args = parser.parse_args()

    hooks_dir = Path(args.hooks_dir)
    if not hooks_dir.is_dir():
        print(f"ERROR: {hooks_dir} is not a directory.", file=sys.stderr)
        return 1

    errors: list[str] = []
    for py_file in sorted(hooks_dir.glob("*.py")):
        error = _check_file(py_file)
        if error:
            errors.append(error)

    if not errors:
        return 0

    print(
        "ERROR: hook script(s) missing ADR reference or module docstring.\n"
        "ADR-011 P6: every hook must cite its governing ADR in its module\n"
        "docstring, or carry `# no-adr: <reason>` for technical-only hooks.\n"
        "See ADR-011 (docs/adr/adr-011-hook-first-enforcement.md).\n",
        file=sys.stderr,
    )
    for error in errors:
        print(f"  {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
