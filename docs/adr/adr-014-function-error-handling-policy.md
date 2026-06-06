# ADR-014: Function Error Handling Policy — Raise, Don't Return Sentinels

## Summary

All functions in this codebase signal failure by raising exceptions, never by returning
sentinel values (`None`, `False`, `-1`, empty collections). On success, a function returns
its meaningful output or `None` when there is nothing to return. This is the binding
convention across all packages (`rl`, `marker`, and any future sibling). The single most
important constraint it imposes: callers must handle failures via `try/except`; they cannot
silently ignore a failed call by discarding a return value.

## Decision

Functions raise typed exceptions on failure. Return type is the success value only — never
a union with a sentinel. Standard Python exception types are preferred where they fit
naturally. A thin `RedlineError` base class is available for domain-specific failures that
do not map to a standard type.

## Status

Accepted — 2026-06-05

## Context

At project inception, no consistent error handling convention existed. Two patterns were
under consideration: returning sentinel values (`None`/`False`) to signal failure, or
raising exceptions. Without a binding decision, different functions would adopt different
patterns, forcing callers to mix `if result is None` checks with `try/except` blocks —
increasing cognitive load and the risk of silently swallowed failures.

The project is developer-facing (no end-user API at this stage). All callers are engineers
or agents working within the codebase, not consumers of a public SDK where silent failure
might be preferred for resilience.

## Options Considered

- **Forgiving (return sentinels):** Return `None`, `False`, or an empty value on failure.
  Caller decides whether to act.
- **Punitive (raise exceptions):** Raise a typed exception on failure. Caller must handle
  or let it propagate.
- **Mixed:** Raise for programming errors (wrong types, invalid arguments); return sentinels
  for recoverable runtime failures (file not found, network timeout).

## Decision Rationale

**Raise exceptions** was selected for the following reasons:

1. **Pythonic.** Python's EAFP (Easier to Ask Forgiveness than Permission) idiom favours
   exceptions. The standard library and all major Python packages (python-docx, pydantic,
   pathlib) raise on failure. Consistency with the ecosystem reduces surprise.

2. **Sentinel returns are easy to ignore.** `result = build_skeleton(...)` followed by no
   check is valid Python. A swallowed failure is invisible until something downstream breaks
   in a harder-to-diagnose way. An unhandled exception surfaces immediately with a full
   stack trace.

3. **Clean return types.** `-> None` or `-> Path` is unambiguous. `-> Path | None` forces
   every caller to handle the `None` branch or ignore it at their own risk.

4. **Debugging.** Exceptions carry message, type, and stack trace. A `None` return carries
   nothing.

5. **Mixed approach rejected.** Distinguishing "programming errors" from "recoverable
   runtime failures" requires consistent judgement across all contributors. In a small team
   with AI agents as contributors, that distinction is a source of drift. A single rule is
   simpler and safer.

## Consequences

**Positive:**

- Failures are never silently swallowed.
- Return types are honest — the return value is always the success value.
- Consistent with the standard library and major dependencies.
- Easier to test: assert that a specific exception is raised rather than checking return
  value equality against a sentinel.

**Negative:**

- Callers that want to continue on failure must explicitly wrap calls in `try/except`.
- A poorly typed exception hierarchy makes it hard for callers to catch specific failure
  modes. Mitigated by the exception taxonomy below.

## Exception Taxonomy

Use standard Python exceptions where they map naturally. Introduce domain exceptions only
when no standard type fits.

| Failure mode | Exception to raise |
| --- | --- |
| Missing or wrong-type argument | `TypeError` |
| Argument value is structurally invalid (empty list, negative count) | `ValueError` |
| File or directory not found, unwritable path | `OSError` / `FileNotFoundError` |
| Pydantic model validation failure | `pydantic.ValidationError` |
| Domain failure with no standard equivalent | `RedlineError` (see below) |

`RedlineError` is a thin base class in `rl.domain.errors` (or equivalent domain layer).
Subclass it only when the failure mode is genuinely domain-specific and callers need to
catch it distinctly. Do not create subclasses speculatively.

## References

- Python docs: EAFP coding style — <https://docs.python.org/3/glossary.html#term-EAFP>
- python-docx error model (raises on invalid operations)
- Pydantic `ValidationError` (raises on model construction failure)
