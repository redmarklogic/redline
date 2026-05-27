# Implementation Plan: Hook-First Enforcement Gaps

**Date**: 2026-05-26 | **Spec**: [spec.md](spec.md)  
**Status**: Draft  
**Branch**: `feature/token-optimisation`

---

## Summary

Close 10 pre-commit enforcement gaps identified against `AGENTS.md` and `.agents/skills/`. Each gap represents a rule currently stated as a text instruction with no deterministic hook check. Nine gaps require a Python hook script in `hooks/`; one gap (`.ipynb` files) is enforced by a `language: fail` config entry already present in `.pre-commit-config.yaml`. All Python hooks use stdlib only, accept project-specific values as CLI args (ADR-011 P4), and follow the canonical `find_violations() + main() → int` structure. Implementation uses TDD throughout: write tests first, run to confirm RED, implement hook, confirm GREEN. CCE indexes the canonical hook pattern after Phase 1 and is recalled in Phase 8 to ensure consistency across all nine Python hooks without re-reading source files.

---

## Technical Context

| Field | Value |
|-------|-------|
| **Language** | Python 3.12 |
| **Package manager** | uv |
| **Testing** | pytest (TDD — `test-driven-development` skill) |
| **Architecture** | Standalone scripts in `hooks/` — no dependency on `src/rl/` |
| **Dev OS / Deploy OS** | Windows / Linux |
| **Key dependencies** | stdlib only: `re`, `ast`, `sys`, `pathlib`, `argparse`. Exception: Phase 10 uses `detect-secrets` managed by pre-commit, not `pyproject.toml` |
| **Hook invocation** | `uv run --frozen --offline hooks/<name>.py [args]` |
| **Config** | `.pre-commit-config.yaml` — all project-specific literals live here (ADR-011 P4) |
| **Token optimisation** | `rtk pytest` (~90% savings), `rtk ruff check` (~80% savings) per `rtk.instructions.md` |
| **Codebase indexing** | cce-mcp skill — `context_search` instead of full-file reads; `record_decision`/`session_recall` for cross-phase pattern persistence |

---

## Design Decisions

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| D1 | Hook script structure | `find_violations(dirs) → list[tuple[Path, int, str]]` + `main() → int` | Separates scan logic from CLI; enables direct unit testing without subprocess |
| D2 | Suppression token | `# hook: allow` (Python), `<!-- hook: allow -->` (Markdown) | Consistent with existing `check-banned-words.py`; inline, minimal |
| D3 | Test approach | pytest `tmp_path`, 3–7 scenarios: violation / suppression / clean | Hermetic, fast; direct `importlib` import of `find_violations()` — no subprocess |
| D4 | Gap 4 (ipynb) test | Assert `.pre-commit-config.yaml` has the entry with correct fields | No Python script to unit test; gap is config-only |
| D5 | detect-secrets baseline | `.secrets.baseline` committed before hook activation | Prevents false positives on existing content |
| D6 | hooks/ exempt from check-no-argparse | `--dirs=src --dirs=scripts` only | Hook scripts are infrastructure tooling; argparse permitted there |
| D7 | `os.getenv("KEY", None)` | Treated as a violation | Spec Edge Cases: `None` is still a default; correct form is `os.environ["KEY"]` |
| D8 | Phase ordering | Must (Phases 1–8) before Should (Phases 9–10) | P1 items protect architecture and code quality immediately |

---

## Domain Impact

**New packages**: None in `pyproject.toml`. `detect-secrets` is pre-commit-managed only.  
**Bounded context changes**: None — hook scripts live outside `src/rl/`.  
**Import-linter contract updates**: None.  
**Subdomain classification**: Generic (infrastructure tooling).  
**New domain terms**: None.

---

## Architecture

```
.pre-commit-config.yaml
  └── hook entry (project-specific args: --dirs, --md-dir, persona names)
           │
           ▼
hooks/<hook-name>.py
  ├── Module docstring  ← references ADR or carries # no-adr: <reason>
  ├── Compiled regex pattern(s)
  ├── find_violations(dirs: list[Path]) → list[tuple[Path, int, str]]
  │     for each .py (or .md) file in dirs:
  │       skip lines containing suppression token
  │       yield (path, lineno, stripped_line) on pattern match
  └── main() → int
        argparse: --dirs / --md-dir / --hooks-dir
        calls find_violations()
        prints violation list if non-empty
        returns 0 (clean) or 1 (violations found)
```

Exit codes: `0` = pass, `1` = violations found. pre-commit treats any non-zero exit as failure.

---

## MoSCoW

| Category | Items |
|----------|-------|
| **Must have** | Gap 1 (persona names), Gap 2 (no argparse), Gap 3 (no archive imports), Gap 4 (no ipynb), Gap 5 (no env loader), Gap 6 (no env defaults), Gap 7 (no section rules), Gap 10 (no debug statements) |
| **Should have** | Gap 8 (hook ADR reference), Gap 9 (detect-secrets) |
| **Could have** | — |
| **Won't have (this time)** | Hooks for non-Python code; automated hook test reporting dashboard |

---

## Phased Delivery

> **Prerequisite for all phases**: Create `tests/hooks/conftest.py` with the `load_hook()` importlib helper (see [data-model.md](data-model.md)) before writing Phase 1 tests.

---

### Phase 1 (Must): Gap 1 — Persona Name Boundary in Skill Files

> **CCE setup note**: At the start of this phase, call `session_recall "hook structure pattern"` to check for prior cross-session decisions. After Phase 1 verifies the canonical hook structure end-to-end, call:
> ```
> record_decision "hook structure: module docstring + ADR/no-adr + argparse + find_violations(dirs: list[Path])->list[tuple[Path,int,str]] + main()->int + suppression # hook: allow / <!-- hook: allow -->"
> ```
> This decision is recalled in Phase 8 so Phases 2–8 share the same structure without re-reading source.

**Goal**: Verify `check-banned-words.py` supports `--md-dir` for recursive Markdown scanning; the `check-skills-persona-names` hook blocks a skill file containing an agent persona name and passes on clean files.

**FRs**: FR-001, FR-002, FR-003, FR-016, FR-018

**TDD approach**: Write `tests/hooks/test_check_banned_words.py` first.

| Scenario | Input | Expected |
|----------|-------|----------|
| A | `.agents/skills/my-skill/SKILL.md` contains "Kabilan" | `find_violations` returns one entry |
| B | Same line with `<!-- hook: allow -->` | zero violations |
| C | Clean skill file, no persona names | zero violations |
| D | `hooks/check-banned-words.py` itself contains "redline" (existing regression) | zero violations (own filename excluded) |

**Deliverables**:
1. `tests/hooks/conftest.py` — `load_hook(name, repo_root)` fixture
2. `tests/hooks/test_check_banned_words.py` — scenarios A–D above
3. `hooks/check-banned-words.py` — verify/implement `--md-dir`, `_check_md_files()`, `<!-- hook: allow -->` suppression

**Verification**:
```
rtk pytest tests/hooks/test_check_banned_words.py -v
rtk ruff check hooks/check-banned-words.py
```

**Acceptance Gate** (both must pass before Phase 2 starts):
- [ ] `rtk pytest tests/hooks/test_check_banned_words.py -v` exits 0, all scenarios green
- [ ] `pre-commit run check-skills-persona-names --all-files` exits 0 on clean repository

---

### Phase 2 (Must): Gap 2 — No argparse in Source Code

**Goal**: `check-no-argparse.py` detects `import argparse` and `from argparse import` in `src/` and `scripts/`; exits non-zero; respects `# hook: allow`.

**FRs**: FR-004, FR-005, FR-015, FR-016, FR-017, FR-018

**TDD approach**: Write `tests/hooks/test_check_no_argparse.py` first.

| Scenario | Input | Expected |
|----------|-------|----------|
| A | `src/example.py` contains `import argparse` | one violation |
| B | `src/example.py` contains `from argparse import ArgumentParser` | one violation |
| C | Violating line has `# hook: allow` | zero violations |
| D | Clean `src/` directory | zero violations |

**Deliverables**:
1. `tests/hooks/test_check_no_argparse.py` — scenarios A–D
2. `hooks/check-no-argparse.py` — verify canonical structure with `# no-adr:` exemption, `_ARGPARSE_PATTERN`

**Verification**:
```
rtk pytest tests/hooks/test_check_no_argparse.py -v
rtk ruff check hooks/check-no-argparse.py
```

**Acceptance Gate**:
- [ ] `rtk pytest tests/hooks/test_check_no_argparse.py -v` exits 0, all scenarios green
- [ ] `pre-commit run check-no-argparse --all-files` exits 0 on clean repository

---

### Phase 3 (Must): Gap 3 — No archive/ Imports

**Goal**: `check-no-archive-imports.py` detects `import archive` and `from archive[.submodule] import` in `src/`.

**FRs**: FR-006, FR-015, FR-016, FR-017, FR-018

**TDD approach**: Write `tests/hooks/test_check_no_archive_imports.py` first.

| Scenario | Input | Expected |
|----------|-------|----------|
| A | `from archive.old_module import helper` | one violation |
| B | `import archive` | one violation |
| C | `from archive import something` | one violation |
| D | Violating line has `# hook: allow` | zero violations |
| E | Clean directory | zero violations |

**Deliverables**:
1. `tests/hooks/test_check_no_archive_imports.py` — scenarios A–E
2. `hooks/check-no-archive-imports.py` — verify `_ARCHIVE_PATTERN` covers `import archive`, `from archive import`, and `from archive.sub import`

**Verification**:
```
rtk pytest tests/hooks/test_check_no_archive_imports.py -v
rtk ruff check hooks/check-no-archive-imports.py
```

**Acceptance Gate**:
- [ ] All scenarios green
- [ ] `pre-commit run check-no-archive-imports --all-files` exits 0 on clean repository

---

### Phase 4 (Must): Gap 4 — No .ipynb Files

**Goal**: `.pre-commit-config.yaml` has a `forbidden-ipynb-files` entry using `language: fail` that blocks any staged `.ipynb` file. No Python script required.

**FRs**: FR-007, FR-019

**TDD approach**: Write `tests/hooks/test_forbidden_ipynb_files.py` first. Assert config fields using `Path.read_text()` + string matching (stdlib only).

| Scenario | Assertion | Expected |
|----------|-----------|----------|
| A | `forbidden-ipynb-files` entry exists in config text | passes |
| B | Entry contains `language: fail` | passes |
| C | Entry contains `\.ipynb$` file pattern | passes |
| D | Entry contains `priority: 0` | passes |

**Deliverables**:
1. `tests/hooks/test_forbidden_ipynb_files.py` — config assertion scenarios A–D

**Verification**:
```
rtk pytest tests/hooks/test_forbidden_ipynb_files.py -v
```

**Acceptance Gate**:
- [ ] Config assertion tests exit 0
- [ ] `pre-commit run forbidden-ipynb-files --all-files` exits 0 on clean repository (no `.ipynb` files present)

---

### Phase 5 (Must): Gap 5 — No Custom .env Loaders

**Goal**: `check-no-env-loader.py` detects `load_dotenv`, `from dotenv import`, `import dotenv`, and `dotenv.load` in `src/` and `scripts/`.

**FRs**: FR-008, FR-015, FR-016, FR-017, FR-018

**TDD approach**: Write `tests/hooks/test_check_no_env_loader.py` first.

| Scenario | Input | Expected |
|----------|-------|----------|
| A | `from dotenv import load_dotenv` | one violation |
| B | `import dotenv` | one violation |
| C | `load_dotenv()` (bare call) | one violation |
| D | Violating line has `# hook: allow` | zero violations |
| E | Clean directory | zero violations |

**Deliverables**:
1. `tests/hooks/test_check_no_env_loader.py` — scenarios A–E
2. `hooks/check-no-env-loader.py` — verify `_ENV_LOADER_PATTERN` covers all three dotenv forms

**Verification**:
```
rtk pytest tests/hooks/test_check_no_env_loader.py -v
rtk ruff check hooks/check-no-env-loader.py
```

**Acceptance Gate**:
- [ ] All scenarios green
- [ ] `pre-commit run check-no-env-loader --all-files` exits 0 on clean repository

---

### Phase 6 (Must): Gap 6 — No Environment Variable Defaults

**Goal**: `check-no-env-defaults.py` detects `os.getenv("KEY", <default>)` and `os.environ.get("KEY", <default>)` with any second argument (including `None`) in `src/` and `scripts/`.

**FRs**: FR-009, FR-015, FR-016, FR-017, FR-018

**TDD approach**: Write `tests/hooks/test_check_no_env_defaults.py` first.

| Scenario | Input | Expected |
|----------|-------|----------|
| A | `os.getenv("KEY", "default")` | one violation |
| B | `os.environ.get("KEY", None)` | one violation (`None` is still a default) |
| C | `os.getenv("KEY")` (no second arg) | zero violations |
| D | `os.environ["KEY"]` (direct access) | zero violations |
| E | Violating line has `# hook: allow` | zero violations |

**Deliverables**:
1. `tests/hooks/test_check_no_env_defaults.py` — scenarios A–E including the `None` boundary case
2. `hooks/check-no-env-defaults.py` — verify `_ENV_DEFAULT_PATTERN` matches both `getenv` and `environ.get` with a second argument

**Verification**:
```
rtk pytest tests/hooks/test_check_no_env_defaults.py -v
rtk ruff check hooks/check-no-env-defaults.py
```

**Acceptance Gate**:
- [ ] All scenarios green, including `None` default triggering a violation
- [ ] `pre-commit run check-no-env-defaults --all-files` exits 0 on clean repository

---

### Phase 7 (Must): Gap 7 — No Section-Rule Comments

**Goal**: `check-no-section-rules.py` detects comment lines with four or more consecutive dashes (e.g. `# ----`) in `src/`.

**FRs**: FR-010, FR-015, FR-016, FR-017, FR-018

**TDD approach**: Write `tests/hooks/test_check_no_section_rules.py` first.

| Scenario | Input | Expected |
|----------|-------|----------|
| A | `# ---------------------------------------------------------------------------` | one violation |
| B | `# ----` (exactly four dashes — minimum threshold) | one violation |
| C | `# ---` (three dashes — below threshold) | zero violations |
| D | `# ---- some text` (dashes followed by text) | one violation |
| E | Violating line has `# hook: allow` | zero violations |

**Deliverables**:
1. `tests/hooks/test_check_no_section_rules.py` — scenarios A–E including boundary cases
2. `hooks/check-no-section-rules.py` — verify `_SECTION_RULE_PATTERN = re.compile(r"^\s*#\s*-{4,}")`

**Verification**:
```
rtk pytest tests/hooks/test_check_no_section_rules.py -v
rtk ruff check hooks/check-no-section-rules.py
```

**Acceptance Gate**:
- [ ] All scenarios green; 3-dash case passes, 4-dash case fails
- [ ] `pre-commit run check-no-section-rules --all-files` exits 0 on clean repository

---

### Phase 8 (Must): Gap 10 — No Debug Statements

> **CCE recall note**: Call `session_recall "hook structure pattern"` to retrieve the canonical structure recorded at the end of Phase 1. If nothing is returned (new session), call `context_search "find_violations dirs list Path tuple"` to locate the pattern in the indexed codebase. Call `reindex hooks/check-no-debug-statements.py` immediately after the file is created or modified to keep the index current.

**Goal**: `check-no-debug-statements.py` detects `breakpoint()`, `import pdb`, `pdb.set_trace()`, `import ipdb`, and `ipdb.set_trace()` in `src/` and `tests/`.

**FRs**: FR-014, FR-015, FR-016, FR-017, FR-018

**TDD approach**: Write `tests/hooks/test_check_no_debug_statements.py` first.

| Scenario | Input | Expected |
|----------|-------|----------|
| A | `breakpoint()` | one violation |
| B | `import pdb` | one violation |
| C | `pdb.set_trace()` | one violation |
| D | `import ipdb` | one violation |
| E | `ipdb.set_trace()` | one violation |
| F | Violating line has `# hook: allow` | zero violations |
| G | Clean directory | zero violations |

**Deliverables**:
1. `tests/hooks/test_check_no_debug_statements.py` — scenarios A–G (all five debug patterns)
2. `hooks/check-no-debug-statements.py` — verify `_DEBUG_PATTERNS` list covers all five patterns, `# no-adr:` exemption present

**Verification**:
```
rtk pytest tests/hooks/test_check_no_debug_statements.py -v
rtk ruff check hooks/check-no-debug-statements.py
```

**Acceptance Gate**:
- [ ] All five debug patterns each trigger exactly one violation; all scenarios green
- [ ] `pre-commit run check-no-debug-statements --all-files` exits 0 on clean repository

---

### Phase 9 (Should): Gap 8 — Hook ADR Reference Enforcement

**Goal**: `check-hook-adr-reference.py` fails when a hook script has no module docstring or no ADR reference, passes when "ADR-NNN" appears in the docstring or `# no-adr: <reason>` is present anywhere in the file.

**FRs**: FR-011, FR-015, FR-017

**TDD approach**: Write `tests/hooks/test_check_hook_adr_reference.py` first.

| Scenario | Input | Expected |
|----------|-------|----------|
| A | Hook file with no docstring at all | one violation |
| B | Hook file with plain docstring, no ADR reference, no `# no-adr:` | one violation |
| C | Hook file with docstring containing "See ADR-011" | zero violations |
| D | Hook file with no ADR reference but `# no-adr: purely technical constraint` | zero violations |
| E | `check-hook-adr-reference.py` itself (references ADR-011 in its own docstring) | zero violations |

**Deliverables**:
1. `tests/hooks/test_check_hook_adr_reference.py` — scenarios A–E
2. `hooks/check-hook-adr-reference.py` — verify AST-based docstring extraction, `_ADR_PATTERN`, `_NO_ADR_PATTERN`; verify the hook passes its own gate (scenario E)

**Verification**:
```
rtk pytest tests/hooks/test_check_hook_adr_reference.py -v
rtk ruff check hooks/check-hook-adr-reference.py
```

**Acceptance Gate**:
- [ ] All five scenarios green
- [ ] `pre-commit run check-hook-adr-reference --all-files` exits 0 on the full `hooks/` directory

---

### Phase 10 (Should): Gap 9 — No Hardcoded Credentials

**Goal**: The `detect-secrets` hook from `https://github.com/Yelp/detect-secrets` is wired into `.pre-commit-config.yaml` and a `.secrets.baseline` file exists, enabling credential detection at commit time.

**FRs**: FR-012, FR-013

**Setup step** (before writing tests — run once on clean repository):
```
uv run detect-secrets scan > .secrets.baseline
git add .secrets.baseline
```

**TDD approach**: Write `tests/hooks/test_detect_secrets.py` first.

| Scenario | Assertion | Expected |
|----------|-----------|----------|
| A | `.pre-commit-config.yaml` text contains `detect-secrets` | passes |
| B | Config text contains `Yelp/detect-secrets` | passes |
| C | Config text contains `--baseline` | passes |
| D | `.secrets.baseline` file exists in repository root | passes |

**Deliverables**:
1. `tests/hooks/test_detect_secrets.py` — config and file existence assertions
2. `.secrets.baseline` — generated and committed

**Verification**:
```
rtk pytest tests/hooks/test_detect_secrets.py -v
pre-commit run detect-secrets --all-files
```

**Acceptance Gate**:
- [ ] Config and file existence tests exit 0
- [ ] `pre-commit run detect-secrets --all-files` exits 0 on clean repository with baseline

---

### Final Gate: Full Suite

After all 10 phases are complete, run the full verification:

```
rtk pytest tests/hooks/ -v
pre-commit run --all-files
```

**Success Criteria** (from spec.md):
- **SC-001**: All 10 gaps produce non-zero exit code when forbidden pattern introduced
- **SC-002**: `pre-commit run --all-files` passes on clean repository
- **SC-003**: Every new hook script passes `check-hook-adr-reference` gate
- **SC-004**: `check-banned-words` passes (no project-specific literals in hook bodies)
- **SC-005**: Inline suppression verified for at least one hook

---

## Supporting Artifacts

| Artifact | Path |
|----------|------|
| Research decisions | [research.md](research.md) |
| Hook interface contract | [data-model.md](data-model.md) |
| Hook CLI contracts | [contracts/hook-cli-contracts.md](contracts/hook-cli-contracts.md) |
| Quickstart guide | [quickstart.md](quickstart.md) |

## File Inventory

| Phase | New Files | Count |
| ----- | --------- | ----- |
| 0     | [...]     | N     |
| 1     | [...]     | N     |

**Total new**: ~N | **Total deleted**: ~N

## Library Best Practices

<!-- Populated after Context7 MCP review of each key dependency -->

### [package-name]

- **Import path**: [confirmed import]
- **API gotchas**: [removed/renamed kwargs, changed defaults]
- **Confirmed pattern**: [minimal code pattern for this plan's usage]

## Risk Register

| Risk       | Mitigation  |
| ---------- | ----------- |
| [...]      | [...]       |
