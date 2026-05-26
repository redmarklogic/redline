# Research: Hook-First Enforcement Gaps

**Feature**: 006-hook-enforcement-gaps  
**Date**: 2026-05-26  
**Status**: Complete — no NEEDS CLARIFICATION items remain

---

## D1 — Canonical hook structure

**Decision**: All Python hooks follow `find_violations(dirs) → list[tuple[Path, int, str]]` + `main() → int`.  
**Rationale**: Separating scan logic from CLI invocation enables direct unit testing without subprocess calls. The `tuple[Path, int, str]` return type (file, 1-based lineno, stripped line text) is consistent across all nine Python hooks and already in use in `check-no-argparse.py` and `check-hook-adr-reference.py`.  
**Alternatives considered**: Subprocess-based tests (rejected — slow, environment-sensitive); returning `list[str]` formatted messages (rejected — harder to assert in tests).

---

## D2 — Suppression token

**Decision**: `# hook: allow` on any offending line suppresses Python hook violations; `<!-- hook: allow -->` suppresses Markdown violations.  
**Rationale**: Already used in `check-banned-words.py`; consistent inline mechanism. No separate allowlist file required for the majority of hooks.  
**Alternatives considered**: Per-file `.hookignore` files (rejected — too coarse-grained); structured comments with reasons (rejected — too verbose for suppressions).

---

## D3 — Test structure

**Decision**: pytest with `tmp_path`, three to seven scenarios per hook: (a) violation present, (b) violation suppressed with `# hook: allow`, (c) clean directory.  
**Rationale**: `tmp_path` is hermetic and fast. Direct import of `find_violations()` via `importlib.util.spec_from_file_location` avoids subprocess overhead. Hook filenames use hyphens (e.g. `check-no-argparse.py`) so standard `import` is invalid; `importlib` is required.  
**Test import pattern**:
```python
import importlib.util
from pathlib import Path

def _load_hook(name: str):
    hook_path = Path(__file__).parents[2] / "hooks" / name
    spec = importlib.util.spec_from_file_location("hook", hook_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```
A shared `conftest.py` at `tests/hooks/conftest.py` will expose a `load_hook(name)` fixture.

---

## D4 — Phase 4 (ipynb) and Phase 10 (detect-secrets) test strategy

**Decision**: For `language: fail` config entries and third-party hooks, pytest reads `.pre-commit-config.yaml` (parsed with stdlib `tomllib` / PyYAML — YAML so use `pathlib` + string matching) and asserts the presence and correctness of the hook entry. No Python script to unit test.  
**Rationale**: The gap is in the config, not in a script. A config-assertion test is the minimal, correct verification.  
**Implementation note**: Parse `.pre-commit-config.yaml` using `import yaml` — wait, `yaml` is not stdlib. Use manual string matching or `import tomllib`. Actually `.pre-commit-config.yaml` is YAML. `PyYAML` (`import yaml`) is in the dev dependencies (used by pre-commit). Alternatively, use `re.search` on the raw file text. Safest stdlib-only approach: `Path(".pre-commit-config.yaml").read_text()` + `assert "forbidden-ipynb-files" in content`.

---

## D5 — detect-secrets baseline management

**Decision**: Generate `.secrets.baseline` with `uv run detect-secrets scan > .secrets.baseline` on the clean repository before wiring the hook; commit the baseline alongside the config change.  
**Rationale**: Pre-populating the baseline prevents existing content from failing the hook on first run. The baseline is the source of truth for allowlisted secrets and test fixtures.  
**Alternatives considered**: Running with `--exclude-files` patterns (rejected — harder to maintain than a committed baseline).

---

## D6 — Hook scripts exempt from check-no-argparse

**Decision**: `check-no-argparse.py` scans `--dirs=src --dirs=scripts` only; `hooks/` is excluded.  
**Rationale**: Hook scripts are infrastructure tooling that legitimately use `argparse` to parse their own CLI arguments (ADR-011 P4). This is already reflected in `.pre-commit-config.yaml`.

---

## D7 — check-no-env-defaults: `None` as a default

**Decision**: `os.getenv("KEY", None)` is treated as a violation.  
**Rationale**: The AGENTS.md rule says "NEVER set default values for environment variables in scripts … unless explicitly asked." `None` is still a default that silently masks a missing variable. The correct form is `os.environ["KEY"]` (raises `KeyError`) or a required-lookup helper.  
**Confirmed by**: spec.md Edge Cases section — "The hook treats `None` as a default (matches the pattern) since the rule is to use required helpers."

---

## D8 — Phase ordering rationale (MoSCoW → Must before Should)

**Decision**: Phases 1–8 implement P1 Must items (User Stories 1–3); Phases 9–10 implement P2 Should items (User Stories 4–5).  
**Must (P1)**: Gaps 1–7 and 10 — architectural correctness, code quality, accidental file detection  
**Should (P2)**: Gaps 8 and 9 — self-documenting hook discipline, credential detection  
**Rationale**: P1 items protect the core source tree and agent architecture immediately. P2 items are important but non-blocking if delivered in the next commit.
