# ADR-021 — Process Environment as Sole Config Source

**Status:** Accepted  
**Date:** 2026-06-10

## Summary

The application process assumes its environment is correctly configured by the
caller (shell, orchestrator, or container runtime). No Python source file in
`src/` or `scripts/` may load a `.env` file, import `python-dotenv`, or supply
a default value to `os.getenv()` / `os.environ.get()`. Environment variables
are read with `os.environ["VAR"]` (raises `KeyError` on misconfiguration) or via
`pydantic-settings` with `env_file=None`. `.env` files are a local developer
ergonomic tool only — they are excluded from the Docker build context and never
present at runtime.

## Context

Redline deploys as a Docker image built in GitHub Actions. The build context
contains no `.env` file. Locally, developers may use a `.env` file for
convenience. Two failure modes arise when source code loads `.env` directly:

1. **Silent local/CI divergence.** `load_dotenv()` finds no file in CI, returns
   without error, and `os.getenv("VAR")` returns `None`. The service starts,
   passes the `/health` liveness check, and CI goes green. The failure surfaces
   only at runtime in the deployed container — after "CI passes."

2. **Silent misconfiguration.** `os.getenv("SECRET_KEY", "dev-secret")` in
   source code means a container with an unset `SECRET_KEY` silently runs with
   a predictable hard-coded value. No startup error; no log line.

Both failure modes share the same root: the code masks a misconfigured
environment instead of surfacing it loudly at startup.

## Decision

1. **`load_dotenv()` and all `python-dotenv` imports are banned from `src/` and
   `scripts/`.** `python-dotenv` is not a declared dependency and must not
   become one without amending this ADR.

2. **`os.getenv("VAR", default)` and `os.environ.get("VAR", default)` with a
   second positional argument are banned from `src/` and `scripts/`.** Use
   `os.environ["VAR"]` (raises `KeyError` on missing — fail-fast, not silent)
   or `pydantic-settings` for structured config with validation at startup.

3. **`.env` files are excluded from the Docker build context.** The root
   `.dockerignore` excludes `.env` and `.env.*`. The Docker image is
   config-agnostic; environment variables enter at container start time via the
   orchestrator (Compose `environment:` locally, GitHub Actions secrets in CI).

4. **Escape hatch.** A line may append `# hook: allow` to exempt a specific
   case. This is intended for test fixtures that exercise env-loading behaviour
   — not for production code.

## Enforcement

Two pre-commit hooks are the primary enforcement layer (ADR-011):

- `hooks/check-no-env-loader.py` — bans `load_dotenv()`, `import dotenv`, etc.
- `hooks/check-no-env-defaults.py` — bans `os.getenv("VAR", default)` etc.

Both are wired in `prek.toml` at priority 10 (fast, blocking, pre-commit) and
scan `src/` and `scripts/`.

## Consequences

- Misconfigured environments fail loudly at startup, not silently at runtime.
- The Docker image is configuration-agnostic; the same image runs in every
  environment without modification.
- Local `.env` files remain a supported developer ergonomic — loaded by the
  shell or Compose before the process starts, never by the process itself.
- `pydantic-settings` is the recommended structured config alternative; it
  validates required vars at process startup and raises `ValidationError`
  immediately on misconfiguration.

## Alternatives Considered

- **Allow `load_dotenv()` in entrypoints only.** Rejected: the failure mode
  is silent regardless of call site. A container with no `.env` starts
  successfully; the failure surfaces only when the missing var is first used.

- **Allow `python-dotenv` as a dev dependency.** Rejected: a dev dep still
  permits `load_dotenv()` in source; the import pattern is indistinguishable
  from a prod dep at the hook level, and the audit cost outweighs the benefit.

## References

- ADR-011 — Hook-First Enforcement  
- ADR-014 — Raise on Failure (no silent sentinel returns)  
- 12-Factor App, Factor III: Config  
- Peter's analysis, 2026-06-10 (via `DEV Community: load_dotenv() Anti-Pattern`)
