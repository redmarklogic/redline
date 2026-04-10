---
name: pre-commit-hooks-create
description: How to implement, register, and test project-specific pre-commit hooks in tasks/hooks/.
---

# Bespoke Pre-commit Hooks

This skill covers how to create project-specific pre-commit hooks that live inside the
repository under `tasks/hooks/`.

## Context & Guidelines

### Scope

Apply this skill when adding a new automated check that should block commits -- e.g.
forbidden filenames, structural invariants, or convention violations that cannot be
expressed as a Ruff rule.

### When to write a bespoke hook (vs. using an existing tool)

- **Use Ruff** for linting and formatting rules expressible as AST or token checks.
- **Use an upstream pre-commit repo** when one already provides the check
  (e.g. `check-merge-conflict`, `trailing-whitespace`).
- **Write a bespoke hook** when the check is project-specific and not covered by any
  existing tool (e.g. "every script must appear in the README", "no numeric-prefixed
  filenames").

### Constraints

- Hooks are plain Python scripts -- no `argparse`, no third-party dependencies beyond what
  is already in `pyproject.toml`.
- Entry point: `uv run tasks/hooks/<hook_name>.py` (ensures the project venv is used).
- Return `0` for pass, non-zero for fail.
- Print a clear, actionable error message on failure (what is wrong, how to fix it, where
  the convention is documented).
- Keep hooks focused: one check per script.
- **Never reference `docs/lessons/` files** in hook scripts or error messages. Lesson
  files are volatile human records that may be renumbered on branch merges. Embed
  rationale directly in the hook's module docstring or error text instead.

### File Placement

- Hook script: `tasks/hooks/<descriptive_name>.py`
- Registration: `.pre-commit-config.yaml` (local repo block)

## Procedure

### 1. Create the hook script

Create a new file under `tasks/hooks/` following the established pattern:

```python
"""Pre-commit hook to <describe what it checks>.

<Optional: reference to the skill or ADR that defines the convention.>
"""

import sys
from pathlib import Path


def find_violations() -> list[Path]:
    """Return paths that violate the convention."""
    ...


def main() -> int:
    """Check for violations and report them."""
    violations = find_violations()
    if not violations:
        return 0

    print("<Clear description of the problem>")
    for v in violations:
        print(f"  {v}")
    print("\n<How to fix it>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

Key conventions:

- Module docstring explains the purpose and references the governing skill/ADR.
- `find_violations()` returns a list of offending paths (or tuples of path + detail).
- `main()` prints human-readable output and returns an exit code.
- No `argparse`; the hook is not a CLI tool.

### 2. Register in `.pre-commit-config.yaml`

Add a `- repo: local` block (or append to an existing one):

```yaml
- repo: local
  hooks:
    - id: <hook-id-kebab-case>
      name: <Short human-readable description>
      entry: uv run tasks/hooks/<hook_name>.py
      language: system
      always_run: true
      pass_filenames: false
```

- `always_run: true` + `pass_filenames: false` is the default for project-wide scans.
- Use `files:` or `types:` filters only when the hook benefits from pre-commit's
  file-selection (e.g. it processes individual files passed as arguments).

### 3. Mention in the governing skill

If a skill defines the convention being enforced, add a reference to the hook in that
skill's `SKILL.md` under a "Pre-commit hook enforcement" section.

### 4. Test the hook

```powershell
uv run pre-commit run <hook-id> --all-files
```

Verify it passes on a clean tree and fails when the violation is present.

### 5. Lint the hook

```powershell
uv run ruff check tasks/hooks/<hook_name>.py
```

## Examples

### Example: Forbid numeric-prefixed script filenames

**Hook**: `tasks/hooks/no_numeric_script_prefix.py`
**Config id**: `no-numeric-script-prefix`
**Governing skill**: `python-script-numbering`

Scans `src/scripts/` for `.py` files matching `s\d\d_*` and rejects the commit.

### Example: Require scripts in README

**Hook**: `tasks/hooks/scripts_in_readme.py`
**Config id**: `scripts-in-readme`
**Governing skill**: `python-script-numbering`

Scans for `.py` files under `src/scripts/` and fails if any filename is missing from
the corresponding `README.md`.
