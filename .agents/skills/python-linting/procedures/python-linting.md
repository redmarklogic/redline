# Python Linting — Detailed Reference

## Context & Guidelines

### Scope

Apply these rules whenever you add or refactor Python code in `src/` or `tests/`.

### Core Rules

- Prefer fixing root causes over suppressing lint rules.
- Only suppress a rule when there is a clear, justified reason.

### Ruff Suppressions

- File-level suppressions: use `# ruff: noqa: RULE1, RULE2` (not `# ruff noqa:`).
- Line-level suppressions: use `# noqa: RULE1, RULE2`.
- Do not use `# ruff: noqa: I001` as a convenience workaround; fix import ordering.

### Common Repo Rules (Non-Exhaustive)

- Use `pathlib.Path` for filesystem operations (avoid `os.path`).
- Exception messages must not use string literals directly; assign the message to a variable first.
- Remove trailing whitespace from blank lines (`W293`).
- Use keyword arguments for boolean parameters (`FBT003`) instead of positional arguments.
- Make boolean default arguments keyword-only using `*` to prevent positional passing (`FBT002`).
- Avoid variable names that shadow Python builtins (`A001`).
- Use `snake_case` for variables in global scope (`N816`).
- Docstring requirements and formatting are enforced by Ruff; use the `python-documentation` skill.
- Sort `__all__` lists alphabetically (`RUF022`).
- Column aliases in domain models (e.g., `pa.Field(alias="...")`) should be kept as string literals directly in the field definition for clarity, even if repeated. Ignore duplicate literal lint errors for these.
- Wrap long string literals (e.g., field descriptions) using parentheses to avoid exceeding line length limits (100 chars).
- Prefer absolute imports over relative imports across packages (`TID252`), unless an existing file uses
  an explicitly allowed pattern via Ruff configuration.
- Suppress broad exception catching in scripts with `# noqa: BLE001` when necessary.
- Always specify an encoding when using `open()` (e.g., `encoding="utf-8"`).

## Procedure

1. Run lint locally (or use CI output) and fix issues directly.
2. If a suppression is truly necessary:
   - Prefer the narrowest scope (line-level over file-level).
   - Add the exact rule codes.
   - Document intent in surrounding code when it is non-obvious.
3. If you see a repeated lint failure pattern, add a one-line reminder to this file under
   "Repo Reminders" (only if it is not already covered).
