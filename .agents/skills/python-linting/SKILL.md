---
name: python-linting
description: Use when resolving Ruff lint violations or deciding whether a suppression is safe in this repo
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

## Repo Reminders

Add one-line reminders here when you fix new, recurring lint failures.
When fixing lint errors, add a concise one-line reminder to this section if not already covered.

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
- Side-effect-only fixtures (injected but value unused) must use `@pytest.mark.usefixtures("fixture_name")` on the class or method instead of parameter injection — **do not** use an underscore prefix to suppress `ARG002`; that only trades it for `PT019`. <!-- hook: allow -->


See `procedures/python-linting.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Adding # noqa without a rule code | Always specify the rule: # noqa: E501 — bare # noqa suppresses everything silently |
| Suppressing a lint rule instead of fixing the code | Suppressions are for unavoidable violations only; fix the code first |
| Running 
uff check --fix on generated files | Exclude generated files in pyproject.toml [tool.ruff] exclude; never auto-fix code you don't own |