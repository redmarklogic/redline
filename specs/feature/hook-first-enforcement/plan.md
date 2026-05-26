# Implementation Plan: Hook-first Enforcement Gaps

**Date**: 2026-05-26 | **Spec**: ADR-011 gap analysis (see chat session 2026-05-26)
**Status**: Draft

## Summary

ADR-011 mandates that every project rule expressible as a deterministic pattern check must
be enforced by a pre-commit hook. A gap analysis against `AGENTS.md` and `.agents/skills/`
identified 10 rules currently stated only as instructions with no hook enforcement. This
plan closes each gap as an independent phase, ordered by architectural risk (P2/P8 priority
first). Each phase adds one hook (or extends one existing hook) and wires it into
`.pre-commit-config.yaml`.

## Technical Context

**Language**: Python 3.12
**Package manager**: uv
**Testing**: pytest (TDD workflow per `test-driven-development` skill)
**Hook location**: `hooks/` (Python scripts, wired into `.pre-commit-config.yaml`)
**Key constraint**: Hook bodies must be generic per ADR-011 P4; project-specific values
pass as CLI args in `.pre-commit-config.yaml`
**Key dependencies**: stdlib only (re, ast, sys, pathlib) — no new third-party packages
**Token optimisation**: Verification commands use [RTK](https://github.com/rtk-ai/rtk) (`rtk pytest` −90%, `rtk ruff check` −80%). RTK is a CLI proxy; prefix `pytest` and `ruff` calls with `rtk` to reduce LLM context cost during development loops.
**Codebase indexing**: [Code Context Engine](https://github.com/elara-labs/code-context-engine) (CCE) — MCP server that provides semantic search over the indexed codebase (94% input-token savings vs full-file reads). Agents call `context_search` instead of reading entire hook files. Setup once with `cce init --agent copilot`. See CCE Workflow section below.

## CCE Workflow

CCE saves tokens at the **reading** phase — when the agent explores existing hooks to understand patterns before writing new ones. This happens at the start of every phase. RTK and CCE address different cost buckets: RTK compresses terminal output; CCE compresses file-reading context.

One-time setup:

```
uv tool install "code-context-engine[local]"
cce init --agent copilot
```

| CCE MCP Tool | When to use in this plan | Example call |
|---|---|---|
| `context_search` | Before writing any hook: find the existing hook pattern (argparse wiring, `main()` signature, `sys.exit` idiom) without reading full files | `context_search "hook script argparse main return int sys.exit"` |
| `record_decision` | After Phase 1: persist the canonical hook structure so every subsequent phase session starts informed without re-reading all hooks | `record_decision "hook structure: module docstring + ADR ref + argparse + find_violations() + main()->int + sys.exit(main())"` |
| `session_recall` | At the start of Phases 2–10: retrieve the hook structure decision from Phase 1 | `session_recall "hook structure pattern"` |
| `reindex` | After adding each new hook file: keep the index current so later phases can search it | `reindex hooks/check-no-argparse.py` |
| `context_search` | Phase 8 specifically: find which existing hooks already carry an `ADR-` reference in their docstring | `context_search "ADR reference docstring hooks"` |

## Design Decisions

| #  | Decision | Choice | Rationale |
|----|----------|--------|-----------|
| D1 | Hook language | Python (stdlib only) | Consistent with existing hooks; no new deps |
| D2 | One hook per rule | Yes, except Phase 1 which extends an existing hook | Keeps each hook single-responsibility and self-documenting |
| D3 | ADR reference in docstring | Required for all new hooks (ADR-011 P6) | P6 compliance; error output links developer to the governing ADR |
| D4 | Suppression mechanism | `# hook: allow` inline comment | Consistent with ADR-011 P5 (inline suppression, no central allowlists) |

## MoSCoW

| Category | Items |
|---|---|
| **Must have** | Phases 1, 2, 3, 4 (architectural invariants per ADR-011 P2/P8) |
| **Should have** | Phases 5, 6, 7 (style invariants explicitly stated in AGENTS.md) |
| **Could have** | Phases 8, 9, 10 (meta-enforcement and security) |
| **Won't have (this time)** | PR size enforcement (requires CI, not pre-commit); behavioral rules (not pattern-checkable) |

---

## Phased Delivery

### Phase 1: Extend `check-banned-words` to cover skill files

**Goal**: Skills must not reference agent persona names (ADR-010 dependency inversion).
Currently `check-banned-words.py` only scans `hooks/`; extend it to also scan
`.agents/skills/**/*.md` using a separate `--skills-dir` argument.

**ADR reference**: ADR-010, ADR-011 P8

**TDD approach**: Add test in `tests/hooks/test_check_banned_words.py` that creates a
temp SKILL.md containing a banned agent name and asserts the hook exits non-zero.

**CCE usage**: This is the only phase that modifies an existing hook rather than creating one.
Use `context_search "check banned words hooks directory argparse"` to retrieve the relevant
functions without reading the full file. After completing this phase, call
`record_decision "hook structure: module docstring + ADR ref + argparse + find_violations() + main()->int + sys.exit(main())"` so phases 2–10 begin informed via `session_recall`.

**Deliverables**:

1. `hooks/check-banned-words.py` — extended with `--skills-dir` and `--skill-banned-words`
   CLI args; scans `*.md` files in the skills directory for forbidden persona names
2. `.pre-commit-config.yaml` — updated `check-banned-words` entry with
   `args: ["--hooks-dir=hooks", "--skills-dir=.agents/skills", "--skill-banned-words=<names>", "redline"]`
3. `tests/hooks/test_check_banned_words.py` — new/updated tests covering the skills-dir path

**Verification**:

```
# Run tests (rtk filters pytest output, -90% tokens)
.venv\Scripts\activate; rtk pytest tests/hooks/test_check_banned_words.py -v

# Run static checks on the modified hook
.venv\Scripts\activate; rtk ruff check hooks/check-banned-words.py
```

**Acceptance Gate** (both must pass before Phase 2 starts):
- [ ] Tests green
- [ ] `pre-commit run check-banned-words --all-files` passes on clean repo

---

### Phase 2: `check-no-argparse` — no `argparse` in `src/` or `scripts/`

**Goal**: AGENTS.md § General Style states `NEVER import argparse`. Enforce this as a
pattern check on all Python files under `src/` and `scripts/`. The `hooks/` directory is
explicitly excluded because hooks legitimately use `argparse`.

**ADR reference**: ADR-011 P1

**TDD approach**: `tests/hooks/test_check_no_argparse.py` — fixture with a temp `.py`
file containing `import argparse`; assert exit code 1. Fixture without it; assert exit
code 0.

**Deliverables**:

1. `hooks/check-no-argparse.py` — scans `.py` files under configurable `--source-dirs`
   for `import argparse` or `from argparse import`; excludes configurable `--exclude-dirs`
2. `.pre-commit-config.yaml` — new entry with
   `args: ["--source-dirs=src,scripts", "--exclude-dirs=hooks"]`
3. `tests/hooks/test_check_no_argparse.py` — unit tests

**Verification**:

```
# Run tests (rtk filters pytest output, -90% tokens)
.venv\Scripts\activate; rtk pytest tests/hooks/test_check_no_argparse.py -v

# Run static checks on the new hook
.venv\Scripts\activate; rtk ruff check hooks/check-no-argparse.py
```

**Acceptance Gate**:
- [ ] Tests green
- [ ] `pre-commit run check-no-argparse --all-files` passes on clean repo

---

### Phase 3: `check-no-archive-imports` — no imports from `archive/`

**Goal**: AGENTS.md § Archive states archive code is for reference only and must not be
imported. Architectural erosion from silent archive imports is the hardest class to
recover from (ADR-011 P8).

**ADR reference**: ADR-011 P1, P8

**TDD approach**: `tests/hooks/test_check_no_archive_imports.py` — fixture with
`from archive.something import Foo`; assert exit 1. Clean file; assert exit 0.

**Deliverables**:

1. `hooks/check-no-archive-imports.py` — scans `.py` files under a configurable
   `--source-dirs` for `from archive` or `import archive` patterns; configurable
   `--archive-dir` name
2. `.pre-commit-config.yaml` — new entry with `args: ["--source-dirs=src,scripts,tests", "--archive-dir=archive"]`
3. `tests/hooks/test_check_no_archive_imports.py` — unit tests

**Verification**:

```
# Run tests (rtk filters pytest output, -90% tokens)
.venv\Scripts\activate; rtk pytest tests/hooks/test_check_no_archive_imports.py -v

# Run static checks on the new hook
.venv\Scripts\activate; rtk ruff check hooks/check-no-archive-imports.py
```

**Acceptance Gate**:
- [ ] Tests green
- [ ] `pre-commit run check-no-archive-imports --all-files` passes on clean repo

---

### Phase 4: Block `.ipynb` files from being committed

**Goal**: AGENTS.md § General Guidelines states never create notebooks unless explicitly
asked. A lightweight `language: fail` entry in `.pre-commit-config.yaml` blocks any
`.ipynb` file at commit time with zero custom Python code.

**ADR reference**: ADR-011 P1, P7

**TDD approach**: No unit test required for a `language: fail` entry (pre-commit itself
is the test). Manual smoke-test: create a dummy `.ipynb` file, attempt `git commit`,
confirm blocked.

**Deliverables**:

1. `.pre-commit-config.yaml` — new `language: fail` entry:
   ```yaml
   - id: forbidden-notebook-files
     name: forbidden notebook files
     entry: "Jupyter notebooks (.ipynb) must not be committed; see AGENTS.md"
     language: fail
     files: \.ipynb$
   ```

**Verification**:

```
echo {} > test.ipynb; git add test.ipynb; pre-commit run forbidden-notebook-files
```
Confirm blocked, then `git restore --staged test.ipynb; del test.ipynb`.

**Acceptance Gate**:
- [ ] Hook blocks a staged `.ipynb` file
- [ ] `pre-commit run forbidden-notebook-files --all-files` passes on clean repo

---

### Phase 5: `check-no-env-loader` — no custom `.env` file loaders

**Goal**: AGENTS.md § General Style states `NEVER implement custom environment loaders`
(e.g., manual `.env` file parsers, `load_dotenv`). Detect `load_dotenv`, `python-dotenv`
imports, and manual `open(.*\.env` patterns in `src/` and `scripts/`.

**ADR reference**: ADR-011 P1

**TDD approach**: `tests/hooks/test_check_no_env_loader.py` — fixtures for each
violation pattern; assert exit 1 per pattern. Clean file; assert exit 0.

**Deliverables**:

1. `hooks/check-no-env-loader.py` — regex scan for configurable `--patterns` list
   against `.py` files under configurable `--source-dirs`
2. `.pre-commit-config.yaml` — new entry with
   `args: ["--source-dirs=src,scripts", "--patterns=load_dotenv,from dotenv,import dotenv"]`
3. `tests/hooks/test_check_no_env_loader.py` — unit tests

**Verification**:

```
# Run tests (rtk filters pytest output, -90% tokens)
.venv\Scripts\activate; rtk pytest tests/hooks/test_check_no_env_loader.py -v

# Run static checks on the new hook
.venv\Scripts\activate; rtk ruff check hooks/check-no-env-loader.py
```

**Acceptance Gate**:
- [ ] Tests green
- [ ] `pre-commit run check-no-env-loader --all-files` passes on clean repo

---

### Phase 6: `check-no-env-defaults` — no default values in `os.getenv()`

**Goal**: AGENTS.md § General Style states `NEVER set default values for environment
variables` (e.g., `os.getenv("VAR", "default")`). Detect the two-argument `os.getenv`
call pattern in `src/` and `scripts/`.

**ADR reference**: ADR-011 P1

**TDD approach**: `tests/hooks/test_check_no_env_defaults.py` — fixture with
`os.getenv("X", "fallback")`; assert exit 1. `os.getenv("X")` or
`os.environ.get("X")`; assert exit 0.

**Deliverables**:

1. `hooks/check-no-env-defaults.py` — regex scan for `os\.getenv\s*\([^,)]+,[^)]+\)`
   in `.py` files under configurable `--source-dirs`
2. `.pre-commit-config.yaml` — new entry with `args: ["--source-dirs=src,scripts"]`
3. `tests/hooks/test_check_no_env_defaults.py` — unit tests

**Verification**:

```
# Run tests (rtk filters pytest output, -90% tokens)
.venv\Scripts\activate; rtk pytest tests/hooks/test_check_no_env_defaults.py -v

# Run static checks on the new hook
.venv\Scripts\activate; rtk ruff check hooks/check-no-env-defaults.py
```

**Acceptance Gate**:
- [ ] Tests green
- [ ] `pre-commit run check-no-env-defaults --all-files` passes on clean repo

---

### Phase 7: `check-no-section-rules` — no separator comment lines

**Goal**: AGENTS.md § General Style states `NEVER introduce section rules`
(e.g., `# -------...`). Detect long dash/underscore separator comments in `.py` files.

**ADR reference**: ADR-011 P1

**TDD approach**: `tests/hooks/test_check_no_section_rules.py` — fixture with
`# --------------------------------`; assert exit 1. Normal comment; assert exit 0.

**Deliverables**:

1. `hooks/check-no-section-rules.py` — regex scan for `#\s*[-_=]{10,}` in `.py` files
   under configurable `--source-dirs`; configurable `--min-length` (default: 10)
2. `.pre-commit-config.yaml` — new entry with `args: ["--source-dirs=src,scripts,hooks", "--min-length=10"]`
3. `tests/hooks/test_check_no_section_rules.py` — unit tests

**Verification**:

```
# Run tests (rtk filters pytest output, -90% tokens)
.venv\Scripts\activate; rtk pytest tests/hooks/test_check_no_section_rules.py -v

# Run static checks on the new hook
.venv\Scripts\activate; rtk ruff check hooks/check-no-section-rules.py
```

**Acceptance Gate**:
- [ ] Tests green
- [ ] `pre-commit run check-no-section-rules --all-files` passes on clean repo

---

### Phase 8: `check-hook-adr-reference` — hooks must cite governing ADR

**Goal**: ADR-011 P6 requires every hook that enforces an ADR-backed rule to reference
the ADR number in its module docstring and error output. Enforce this meta-rule on hooks
that govern architectural invariants (i.e., hooks whose docstring contains "ADR-" already
implies they are ADR-backed; hooks without any ADR reference are flagged if they scan
source files rather than configuration).

**ADR reference**: ADR-011 P6

**TDD approach**: `tests/hooks/test_check_hook_adr_reference.py` — fixture hook file
that scans `src/` but has no ADR reference; assert exit 1. Hook with `See ADR-011`;
assert exit 0.

**CCE usage**: Before writing the hook logic, use `context_search "ADR reference docstring
hooks"` to get a list of which existing hooks already carry an `ADR-\d+` citation and
which do not — this directly defines the test fixtures and the hook's expected violation
set, without reading every hook file individually.

**Deliverables**:

1. `hooks/check-hook-adr-reference.py` — scans `.py` files under configurable
   `--hooks-dir`; for each hook that contains source-scanning patterns (e.g., `src/rl`,
   `src/`, `\.py`) without an `ADR-\d+` reference in the module docstring, emit a
   violation
2. `.pre-commit-config.yaml` — new entry with `args: ["--hooks-dir=hooks"]`
3. `tests/hooks/test_check_hook_adr_reference.py` — unit tests

**Verification**:

```
# Run tests (rtk filters pytest output, -90% tokens)
.venv\Scripts\activate; rtk pytest tests/hooks/test_check_hook_adr_reference.py -v

# Run static checks on the new hook
.venv\Scripts\activate; rtk ruff check hooks/check-hook-adr-reference.py
```

**Acceptance Gate**:
- [ ] Tests green
- [ ] `pre-commit run check-hook-adr-reference --all-files` passes on clean repo

---

### Phase 9: Add `detect-secrets` for hardcoded credential detection

**Goal**: `security` SKILL.md states never hardcode secrets (API keys, passwords, tokens).
`detect-secrets` is the industry-standard pre-commit hook for this pattern; no custom
Python required.

**ADR reference**: ADR-011 P1, P2 (security as architectural invariant)

**TDD approach**: Generate a baseline with `detect-secrets scan > .secrets.baseline`;
add a deliberate fake API key to a temp file; confirm `detect-secrets audit` flags it.

**Deliverables**:

1. `.pre-commit-config.yaml` — add `detect-secrets` repo entry pointing to
   `https://github.com/Yelp/detect-secrets` at a pinned revision
2. `.secrets.baseline` — generated baseline file committed to repo (documents known
   false-positives and allows the hook to pass on clean state)

**Verification**:

```
pre-commit run detect-secrets --all-files
```

**Acceptance Gate**:
- [ ] Hook passes on clean repo with baseline present
- [ ] A file with a fake secret pattern (e.g., `api_key = "AKIAIOSFODNN7EXAMPLE"`) is blocked

---

### Phase 10: `check-no-debug-statements` — no `breakpoint()` or `pdb` in commits

**Goal**: `version-control` SKILL.md states do not commit debug print statements or
breakpoints. Detect `breakpoint()`, `pdb.set_trace()`, and `import pdb` in `.py` files
under `src/`, `scripts/`, and `tests/`.

**ADR reference**: ADR-011 P1, P7

**TDD approach**: `tests/hooks/test_check_no_debug_statements.py` — fixture with each
debug pattern; assert exit 1 per pattern. Clean file; assert exit 0.

**Deliverables**:

1. `hooks/check-no-debug-statements.py` — regex scan for configurable `--patterns`
   in `.py` files under configurable `--source-dirs`; inline `# hook: allow` suppression
   supported for legitimate uses in test utilities
2. `.pre-commit-config.yaml` — new entry with
   `args: ["--source-dirs=src,scripts,tests", "--patterns=breakpoint(),pdb.set_trace(),import pdb"]`
3. `tests/hooks/test_check_no_debug_statements.py` — unit tests

**Verification**:

```
# Run tests (rtk filters pytest output, -90% tokens)
.venv\Scripts\activate; rtk pytest tests/hooks/test_check_no_debug_statements.py -v

# Run static checks on the new hook
.venv\Scripts\activate; rtk ruff check hooks/check-no-debug-statements.py
```

**Acceptance Gate**:
- [ ] Tests green
- [ ] `pre-commit run check-no-debug-statements --all-files` passes on clean repo

---

## File Inventory

| Phase | New / Modified Files | Count |
|-------|----------------------|-------|
| 1 | `hooks/check-banned-words.py` (modified), `.pre-commit-config.yaml` (modified), `tests/hooks/test_check_banned_words.py` | 3 |
| 2 | `hooks/check-no-argparse.py`, `.pre-commit-config.yaml` (modified), `tests/hooks/test_check_no_argparse.py` | 3 |
| 3 | `hooks/check-no-archive-imports.py`, `.pre-commit-config.yaml` (modified), `tests/hooks/test_check_no_archive_imports.py` | 3 |
| 4 | `.pre-commit-config.yaml` (modified) | 1 |
| 5 | `hooks/check-no-env-loader.py`, `.pre-commit-config.yaml` (modified), `tests/hooks/test_check_no_env_loader.py` | 3 |
| 6 | `hooks/check-no-env-defaults.py`, `.pre-commit-config.yaml` (modified), `tests/hooks/test_check_no_env_defaults.py` | 3 |
| 7 | `hooks/check-no-section-rules.py`, `.pre-commit-config.yaml` (modified), `tests/hooks/test_check_no_section_rules.py` | 3 |
| 8 | `hooks/check-hook-adr-reference.py`, `.pre-commit-config.yaml` (modified), `tests/hooks/test_check_hook_adr_reference.py` | 3 |
| 9 | `.pre-commit-config.yaml` (modified), `.secrets.baseline` | 2 |
| 10 | `hooks/check-no-debug-statements.py`, `.pre-commit-config.yaml` (modified), `tests/hooks/test_check_no_debug_statements.py` | 3 |

**Total new hook files**: 8 | **Total modified files**: `.pre-commit-config.yaml` (10 edits)

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|-----------|
| R1 | Phase 1 banned-word list for agent names drifts from `AGENTS.md` as new agents are hired | Medium | Low | Pass names via CLI arg in `.pre-commit-config.yaml`; update alongside `AGENTS.md` when a new agent is added |
| R2 | `detect-secrets` (Phase 9) generates noisy false-positives on existing test fixtures | Medium | Medium | Generate `.secrets.baseline` before wiring into CI; review and accept known FPs |
| R3 | Phase 7 section-rule regex triggers on legitimate uses (e.g., RST/Markdown inside docstrings) | Low | Low | Scoped to `.py` only; `# hook: allow` suppression available at the line |
| R4 | Phases 2–7 pass on current codebase but existing violations exist in history | Low | Low | Hooks only check staged files; history is not re-scanned |
