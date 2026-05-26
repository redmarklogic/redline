# Data Model: Hook-First Enforcement Gaps

**Feature**: 006-hook-enforcement-gaps  
**Date**: 2026-05-26

---

## Canonical Hook Interface

Every Python hook script in `hooks/` implements the following interface.  
This is the binding contract across all nine Python-script gaps (Gaps 1–3, 5–10).

### `find_violations`

```python
def find_violations(dirs: list[Path]) -> list[tuple[Path, int, str]]:
    """Scan .py files under dirs; return (file, 1-based-lineno, stripped-line) triples."""
```

| Field | Type | Meaning |
|-------|------|---------|
| `file` | `Path` | Absolute or repo-relative path to the offending file |
| `lineno` | `int` | 1-based line number |
| `line` | `str` | `line.strip()` — the offending source line, without leading/trailing whitespace |

**Suppression**: any line containing `# hook: allow` (Python) or `<!-- hook: allow -->` (Markdown) is skipped before pattern matching.

### `main`

```python
def main() -> int:
    """Parse CLI args, call find_violations(), print violations, return exit code."""
```

Returns `0` if no violations; returns `1` if one or more violations found.  
pre-commit treats any non-zero exit code as a hook failure.

### CLI argument conventions

| Hook | CLI argument | Notes |
|------|-------------|-------|
| Python-file hooks | `--dirs` (repeatable) | Each value is a directory to scan recursively for `.py` files |
| Markdown scan (`check-banned-words`) | `--md-dir` | Single directory to scan recursively for `.md` files |
| Hook self-audit | `--hooks-dir` | Single directory containing hook `.py` scripts |
| Positional (banned words) | `word [word ...]` | One or more banned words (case-sensitive whole-word match) |

All project-specific values (directory names, persona names) are supplied via CLI args in `.pre-commit-config.yaml`, never hardcoded in hook bodies (ADR-011 P4).

---

## Error Output Format

```
ERROR: <human-readable description of the violation type>.
  <file>:<lineno>: <stripped line>
  <file>:<lineno>: <stripped line>
  ...
Suppression: append `# hook: allow` to a line to exempt it.
```

---

## Module Docstring Requirements (ADR-011 P6)

Every hook script must satisfy exactly one of:

1. **ADR reference**: module-level docstring contains `ADR-NNN` (matched by `\bADR-\d+\b`)
2. **No-ADR exemption**: file contains a line matching `#\s*no-adr\s*:` with a reason

Scripts without a docstring or without one of the above are flagged by `check-hook-adr-reference.py`.

---

## Hook Inventory

| Gap | Hook ID | Script | FR |
|-----|---------|--------|-----|
| 1 | `check-skills-persona-names` | `hooks/check-banned-words.py --md-dir=.agents/skills` | FR-001–003 |
| 2 | `check-no-argparse` | `hooks/check-no-argparse.py --dirs=src --dirs=scripts` | FR-004–005 |
| 3 | `check-no-archive-imports` | `hooks/check-no-archive-imports.py --dirs=src` | FR-006 |
| 4 | `forbidden-ipynb-files` | *(config-only, `language: fail`)* | FR-007 |
| 5 | `check-no-env-loader` | `hooks/check-no-env-loader.py --dirs=src --dirs=scripts` | FR-008 |
| 6 | `check-no-env-defaults` | `hooks/check-no-env-defaults.py --dirs=src --dirs=scripts` | FR-009 |
| 7 | `check-no-section-rules` | `hooks/check-no-section-rules.py --dirs=src` | FR-010 |
| 8 | `check-hook-adr-reference` | `hooks/check-hook-adr-reference.py --hooks-dir=hooks` | FR-011 |
| 9 | `detect-secrets` | *(pre-commit managed, `Yelp/detect-secrets`)* | FR-012–013 |
| 10 | `check-no-debug-statements` | `hooks/check-no-debug-statements.py --dirs=src --dirs=tests` | FR-014 |

---

## Test Module Structure

```
tests/
  hooks/
    conftest.py          # load_hook(name) fixture via importlib.util
    test_check_banned_words.py          # Gap 1
    test_check_no_argparse.py           # Gap 2
    test_check_no_archive_imports.py    # Gap 3
    test_forbidden_ipynb_files.py       # Gap 4 (config assertion)
    test_check_no_env_loader.py         # Gap 5
    test_check_no_env_defaults.py       # Gap 6
    test_check_no_section_rules.py      # Gap 7
    test_check_no_debug_statements.py   # Gap 10 (Phase 8)
    test_check_hook_adr_reference.py    # Gap 8  (Phase 9)
    test_detect_secrets.py              # Gap 9  (Phase 10, config assertion)
```

### `tests/hooks/conftest.py` — canonical test import helper

```python
import importlib.util
from pathlib import Path
import types
import pytest

@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).parents[2]

def load_hook(name: str, repo_root: Path) -> types.ModuleType:
    """Import a hook script by filename (hyphens permitted)."""
    hook_path = repo_root / "hooks" / name
    spec = importlib.util.spec_from_file_location("hook", hook_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```
