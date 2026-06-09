"""Git hook: forbid function definitions inside __init__.py files.

__init__.py files are namespace declarations, not implementation modules.
Placing functions there couples callers to the package root, hides real
module locations, and inflates SonarQube's analysis surface on files that
are intentionally excluded from quality scans.

Suppression: append `# hook: allow` to the def line to exempt it.
"""
# no-adr: project-style rule; no governing ADR

import ast
import sys
from pathlib import Path


def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where functions are defined in __init__.py."""
    violations: list[tuple[Path, int, str]] = []
    for directory in dirs:
        if not directory.is_dir():
            continue
        for init_file in sorted(directory.rglob("__init__.py")):
            source = init_file.read_text(encoding="utf-8")
            lines = source.splitlines()
            try:
                tree = ast.parse(source, filename=str(init_file))
            except SyntaxError:
                continue
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    lineno = node.lineno
                    line = lines[lineno - 1].strip() if lineno <= len(lines) else ""
                    if "# hook: allow" in line:
                        continue
                    violations.append((init_file, lineno, line))
    return violations


def main() -> int:
    """Check for function definitions in __init__.py files and report violations."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Forbid function definitions in __init__.py files.",
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
        "ERROR: function definitions found in __init__.py files.\n"
        "__init__.py is a namespace declaration; move functions to a proper module.\n"
        "To suppress a single line: append `# hook: allow`.\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
