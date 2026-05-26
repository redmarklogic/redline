"""Pre-commit hook: forbid stdlib dataclass usage in src/rl/.

The python-domain-modeling skill mandates Pydantic BaseModel for all domain
value objects and entities. stdlib @dataclass / dataclasses.field are
deprecated for domain modeling in this repo.

Scan every .py file under src/rl/ and fail if any line imports from the
dataclasses stdlib module, so the mistake is caught at commit time rather
than in review.
"""
# no-adr: enforces python-domain-modeling skill convention; no governing ADR

import re
import sys
from pathlib import Path

_DATACLASS_PATTERN = re.compile(r"\bfrom\s+dataclasses\s+import\b|^\s*@dataclass\b")
_SOURCE_ROOT = Path("src/rl")


def find_violations() -> list[tuple[Path, int, str]]:
    """Return (file, lineno, line) triples where dataclasses usage is detected."""
    violations: list[tuple[Path, int, str]] = []
    for py_file in sorted(_SOURCE_ROOT.rglob("*.py")):
        for lineno, line in enumerate(
            py_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if _DATACLASS_PATTERN.search(line):
                violations.append((py_file, lineno, line.strip()))
    return violations


def main() -> int:
    """Check for dataclass usage in src/rl/ and report violations."""
    violations = find_violations()
    if not violations:
        return 0

    print(
        "ERROR: stdlib dataclasses usage found in src/rl/.\n"
        "Use Pydantic BaseModel instead (see python-domain-modeling skill).\n",
        file=sys.stderr,
    )
    for path, lineno, line in violations:
        print(f"  {path}:{lineno}: {line}", file=sys.stderr)
    print(
        "\nFix: replace @dataclass / dataclasses.field with "
        "pydantic.BaseModel / pydantic.Field.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
