---
name: python-linting
description: Standards for Ruff/lint compliance and safe lint suppressions in this repo.
---

# Python Linting (Ruff)

This skill defines how to keep Python code compliant with the repo's linting rules.

## Boundary Contract

### Applies To
- All Python files under `src/` and `tests/`

### Produces
- Ruff-compliant code with justified, narrowly-scoped suppressions

### Does Not Cover
- General style conventions and formatting (`python-style`)
- Type hint standards (`python-typing`)
- Docstring content and format (`python-documentation`)
- Import ordering across packages (`python-module-structure`)

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

## Repo Reminders

Add one-line reminders here when you fix new, recurring lint failures.

- Ensure all module-level imports are placed at the top of the file before any other code (`E402`)
- Do not pass the exception object to `logger.exception()` as it is redundant (`TRY401`).
- When a domain sub-package name intentionally shadows a stdlib module (e.g. `ghgmod.domain.statistics`), suppress `A005` file-wide with `# ruff: noqa: A005` in `__init__.py` and document the reason inline.
- Suppress `RUF059` for loop-unpacked variables not used downstream by prefixing with `_` (e.g. `_p_value`).
- For test stub/mock functions that must match a keyword-only call interface but don't use the arguments, use `**_kwargs` instead of naming unused keyword-only params (`ARG001`).
- Remove unused imports using the automated refactoring tool or manual deletion (`F401`).
- Use proper Markdown headers (e.g., `##`) instead of bolded text for section titles in documentation (`MD036`).
- Use `Self` return type from `typing` in context manager `__enter__` methods instead of string literals (`PYI034`).
- Avoid chained boolean assertions; use `all(...)` or separate checks to satisfy `PT018`.
- When adding a new subpackage under an `exhaustive = true` container, add it to the `layers` list in the corresponding `[[tool.importlinter.contracts]]` block in `pyproject.toml`. See `.agents/skills/spec-kit/references/import-linter.md` for details.
- Side-effect-only fixtures (injected but value unused) must use `@pytest.mark.usefixtures("fixture_name")` on the class or method instead of parameter injection — **do not** use an underscore prefix to suppress `ARG002`; that only trades it for `PT019`.
