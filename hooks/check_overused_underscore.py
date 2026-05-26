"""Git hook to detect overused underscore-prefixed helpers."""
# no-adr: code quality heuristic; no governing ADR

import ast
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def list_py_files(base: Path) -> list[Path]:
    """Recursively list Python source files under a base directory.

    Args:
        base: The base directory to search for `.py` files.

    Returns:
        A list of absolute Paths to Python source files contained in the tree.
    """
    return [p for p in base.rglob("*.py") if p.is_file()]


def analyze_file(path: Path) -> tuple[set[str], set[str]]:
    """Parse a Python module to collect private helper definitions and references.

    Parses the given file to find any function or class definitions whose names
    begin with a single underscore (indicating a private helper). It also finds
    all references to such underscored names within that module.

    Args:
        path: Path object pointing to the file being analyzed.

    Returns:
        A tuple (defs, refs):
            defs: Set of helper names defined in the file.
            refs: Set of helper names referenced in the file.
    """
    try:
        code = path.read_text(encoding="utf-8")
        tree = ast.parse(code, filename=str(path))
    except SyntaxError:
        # Skip files that don't parse
        return set(), set()

    defs, refs = set(), set()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_") and not node.name.startswith("__"):
                defs.add(node.name)
        elif (
            isinstance(node, ast.Name)
            and node.id.startswith("_")
            and not node.id.startswith("__")
        ) or (
            isinstance(node, ast.Attribute)
            and node.attr.startswith("_")
            and not node.attr.startswith("__")
        ):
            refs.add(getattr(node, "id", getattr(node, "attr", "")))

    return defs, refs


def main(max_extra_files: int = 3, base_dir: str = "src") -> int:
    """Check for underscore helpers referenced outside their defining files.

    Scans all `.py` files in the given directory, then flags any function or
    class whose name begins with a single underscore (`_`) if it is referenced
    in more files than it is defined in, exceeding a threshold of extra files.

    The overuse level is computed as:
        overuse_level = len(used_in_files) - len(definition_files)

    If `overuse_level > max_extra_files`, the hook reports a failure.

    Args:
        max_extra_files: Maximum allowed number of files beyond definition files
            where a private helper may appear.
        base_dir: Directory to use as the root for scanning.

    Returns:
        An integer exit code (0 on success, 1 on violation).
    """
    base_path = Path(base_dir)
    files = list_py_files(base_path)
    if not files:
        print(f"No Python files found under {base_path}")
        return 0

    all_defs: dict[str, set[Path]] = defaultdict(set)
    all_refs: dict[str, set[Path]] = defaultdict(set)

    with ProcessPoolExecutor() as exe:
        futures = {exe.submit(analyze_file, f): f for f in files}
        for fut in as_completed(futures):
            fpath = futures[fut]
            defs, refs = fut.result()
            for d in defs:
                all_defs[d].add(fpath)
            for r in refs:
                all_refs[r].add(fpath)

    offenders = []
    for name, def_files in all_defs.items():
        used_in = all_refs.get(name, set())
        overuse_level = len(used_in) - len(def_files)
        if overuse_level > max_extra_files:
            offenders.append((name, overuse_level, def_files, used_in))

    if offenders:
        print("FAILED: Overused private helpers found:\n")
        for name, overuse, defs, uses in sorted(offenders, key=lambda x: -x[1]):
            defs_fmt = ", ".join(str(p.relative_to(base_path)) for p in defs)
            uses_fmt = ", ".join(str(p.relative_to(base_path)) for p in sorted(uses))
            print(
                f"  {name}: referenced in {len(uses)} files, "
                f"defined in {len(defs)} files "
                f"(overuse level = {overuse})"
            )
            print(f"    defined in: {defs_fmt}")
            print(f"    used in: {uses_fmt}\n")
        print(f"Failing (> {max_extra_files} extra files beyond definitions).")
        return 1

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detect overused underscore helpers.")
    parser.add_argument(
        "--max-extra-files",
        "-t",
        type=int,
        default=1,
        help="Maximum number of extra files beyond definitions (default: 1).",
    )
    parser.add_argument(
        "--base",
        "-b",
        type=str,
        default="src",
        help="Base directory to search (default: 'src').",
    )
    args = parser.parse_args()
    sys.exit(main(args.max_extra_files, args.base))
