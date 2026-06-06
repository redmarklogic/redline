"""Git hook: require description= and alias= on every Pydantic field in domain/schema modules.

Every annotated attribute in a Pydantic model class under src/*/domain/ and
src/*/schemas/ must declare Field(description=..., alias=...) so models are
self-documenting and serialisation aliases are explicit. Catches violations at
commit time via AST analysis; no base-class inheritance required.
"""
# no-adr: enforces python-domain-modeling skill convention; no governing ADR

import ast
import sys
from pathlib import Path

_SCAN_ROOTS = [Path("src")]
_TARGET_PARTS = frozenset({"domain", "schemas"})
_SKIP_NAMES = frozenset({"model_config", "model_fields", "__annotations__"})


def _is_target_file(path: Path) -> bool:
    return any(part in _TARGET_PARTS for part in path.parts)


def _missing_field_kwargs(call: ast.Call) -> list[str]:
    present = {kw.arg for kw in call.keywords}
    return [k for k in ("description", "alias") if k not in present]


def _is_field_call(node: ast.expr | None) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (isinstance(func, ast.Name) and func.id == "Field") or (
        isinstance(func, ast.Attribute) and func.attr == "Field"
    )


def _check_file(path: Path) -> list[tuple[int, str, list[str]]]:
    """Return (lineno, field_name, missing_kwargs) triples for each violation."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return []

    violations: list[tuple[int, str, list[str]]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if not isinstance(item, ast.AnnAssign):
                continue
            if not isinstance(item.target, ast.Name):
                continue
            name = item.target.id
            if name in _SKIP_NAMES or name.startswith("_"):
                continue
            if item.value is None:
                violations.append((item.lineno, name, ["description=", "alias="]))
            elif _is_field_call(item.value):
                missing = _missing_field_kwargs(item.value)  # type: ignore[arg-type]
                if missing:
                    violations.append((item.lineno, name, [f"{k}=" for k in missing]))
    return violations


def main() -> int:
    """Entry point."""
    all_violations: list[tuple[Path, int, str, list[str]]] = []
    for root in _SCAN_ROOTS:
        for py_file in sorted(root.rglob("*.py")):
            if not _is_target_file(py_file):
                continue
            for lineno, field_name, missing in _check_file(py_file):
                all_violations.append((py_file, lineno, field_name, missing))

    if not all_violations:
        return 0

    print(
        "ERROR: Pydantic model fields missing required metadata.\n"
        "All fields in domain/schema modules must declare "
        "Field(description=..., alias=...) "
        "(see python-domain-modeling skill).\n",
        file=sys.stderr,
    )
    for path, lineno, field_name, missing in all_violations:
        print(
            f"  {path}:{lineno}: {field_name!r} missing {', '.join(missing)}",
            file=sys.stderr,
        )
    print(
        "\nFix: add Field(description='...', alias='...') to each flagged field.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
