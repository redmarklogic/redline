# Implementation Plan: RTK + CCE Enforcement

**Date**: 2026-05-30 | **Spec**: `specs/009-rtk-cce-enforcement/spec.md`
**Status**: Draft

## Summary

Build enforcement mechanisms for RTK (token-optimised CLI proxy) and CCE (Code Context Engine) usage across the agent system. Deliverables: (1) a pre-commit hook that checks instruction/skill files for bare shell commands missing the `rtk` prefix, (2) a session audit script that measures RTK and CCE compliance from session store data, (3) CCE skill reinforcement with an actionable decision tree, (4) RTK rewrite hook validation documentation.

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (TDD workflow per `test-driven-development` skill)
**Architecture**: Hooks follow `hooks/` directory pattern — `find_violations()` + `main() -> int`
**Dev OS**: Windows | **Deploy OS**: N/A (tooling only)
**Key dependencies**: stdlib only (re, pathlib, sys, argparse) for hooks; `session_store_sql` MCP tool for audit

## Constitution Check

Constitution template not populated — no gates to evaluate.

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | --- | --- | --- |
| D1 | RTK-eligible command list | Explicit allowlist: `git`, `pytest`, `ruff`, `docker`, `uv`, `pip`, `mypy`, `prek` | Avoids false positives on commands RTK doesn't support; matches rtk.instructions.md examples |
| D2 | Hook scope for RTK check | Scan `.md` files under `.agents/skills/`, `.github/instructions/`, `.github/agents/`, `docs/`, `specs/` | These are the files agents read; Python source and tests are excluded (developers, not agents, run those commands) |
| D3 | Code block detection strategy | Regex for fenced code blocks (``` ```bash`, ``` ```sh`, ``` ``` with shell-like content) | Matches existing hook patterns (check-mermaid-syntax.py uses same approach) |
| D4 | Suppression mechanism | `<!-- rtk:skip -->` on line preceding code block | Consistent with existing suppression patterns (`<!-- mermaid: allow -->`, `# hook: allow`) |
| D5 | Session audit location | `scripts/audit_rtk_cce.py` | Runs on-demand, not pre-commit; follows `scripts/` convention |
| D6 | Audit data source | `session_store_sql` MCP tool (SQLite) | Already available; stores tool call history per session |
| D7 | CCE decision tree format | Flowchart in `cce-mcp/SKILL.md` "When to Use" section | Single source of truth for agent behaviour; no new files needed |

## Domain Impact

**New packages**: None
**Bounded context changes**: None
**Import-linter contract updates**: None
**Subdomain classification**: Generic (developer tooling)
**New domain terms**: None

## Architecture

```
Pre-commit (prek)                    On-demand audit
─────────────────                    ─────────────────
hooks/check-rtk-in-docs.py          scripts/audit_rtk_cce.py
  │                                    │
  ├─ Scans .md files for              ├─ Queries session_store_sql
  │  fenced code blocks               │  for tool_call events
  │                                    │
  ├─ Checks each shell command        ├─ Classifies run_in_terminal
  │  against RTK-eligible list        │  calls as rtk/non-rtk
  │                                    │
  └─ Reports violations with          ├─ Classifies read_file vs
     line numbers + suggestions       │  context_search for discovery
                                       │
                                       └─ Outputs compliance report
                                          to stdout
```

## Domain Models

No domain models. This is pure tooling — hooks and scripts only.

## MoSCoW

| Category | Items |
| --- | --- |
| **Must have** | Pre-commit hook for RTK enforcement in docs (Scenario 1); CCE skill reinforcement with decision tree (Scenario 3) |
| **Should have** | Session audit script (Scenario 2); RTK rewrite hook validation doc (Scenario 4) |
| **Could have** | Aggregate compliance dashboard via `rtk gain` integration |
| **Won't have (this time)** | Automated CCE preference enforcement at runtime (would require MCP middleware); RTK CLI changes |

## Phased Delivery

### Phase 0: RTK Pre-commit Hook

**Goal**: A working pre-commit hook that detects bare shell commands (without `rtk` prefix) inside fenced code blocks in instruction/skill/agent Markdown files.

**TDD approach**: Write tests first in `tests/hooks/test_check_rtk_in_docs.py` covering: violation detection, suppression via `<!-- rtk:skip -->`, pass on already-prefixed commands, skip non-eligible commands, skip non-shell code blocks.

**Deliverables**:

1. `hooks/check-rtk-in-docs.py` — hook following `find_violations()` + `main() -> int` pattern
2. `tests/hooks/test_check_rtk_in_docs.py` — unit tests
3. `prek.toml` entry — register hook with `files = '\.(md|qmd)$'` and appropriate `--dirs` args

**Verification**:

<!-- rtk:skip -->
```bash
.venv\Scripts\activate; python -m pytest tests/hooks/test_check_rtk_in_docs.py -v
uv run --frozen --offline hooks/check-rtk-in-docs.py --dirs=.agents/skills --dirs=.github/instructions --dirs=.github/agents --dirs=docs --dirs=specs
```

**Acceptance Gate** (both must pass before Phase 1 starts):
- [ ] Working code: hook runs against repo and reports violations (or clean pass) without errors
- [ ] Tests green: `python -m pytest tests/hooks/test_check_rtk_in_docs.py -v` all pass

---

### Phase 1: CCE Skill Reinforcement

**Goal**: Update `cce-mcp/SKILL.md` with an actionable decision tree replacing advisory "When to Use" language. Add missing "Common Mistakes" entry for `grep_search` vs `context_search`.

**TDD approach**: No code tests. Manual review against Scenario 3 acceptance criteria.

**Deliverables**:

1. `.agents/skills/cce-mcp/SKILL.md` — updated "When to Use" section with decision tree; updated "Common Mistakes" table

**Verification**:

```
Read updated SKILL.md and verify:
1. Decision tree has 3 branches: discovery → context_search, targeted edit → read_file, specific section → context_search + expand_chunk
2. Common Mistakes table includes grep_search row
3. Skill description unchanged in AGENTS.md
```

**Acceptance Gate**:
- [ ] Decision tree present and covers all three branches
- [ ] Common Mistakes table includes grep_search entry

---

### Phase 2: Session Audit Script

**Goal**: A script that queries session store for RTK and CCE compliance metrics, outputting a report with compliance percentages and per-violation details.

**TDD approach**: Write tests first in `tests/scripts/test_audit_rtk_cce.py` for the classification functions (is_rtk_command, is_discovery_read, compliance calculation).

**Deliverables**:

1. `scripts/audit_rtk_cce.py` — audit script with classification + reporting
2. `tests/scripts/test_audit_rtk_cce.py` — unit tests for classification logic

**Verification**:

```bash
.venv\Scripts\activate; python -m pytest tests/scripts/test_audit_rtk_cce.py -v
```

**Acceptance Gate**:
- [ ] Tests green
- [ ] Script runs without errors against current session store (may report 0 sessions if store is empty)

---

### Phase 3: RTK Hook Validation Doc

**Goal**: Document validation procedure for the existing `rtk-rewrite.json` PreToolUse hook. Confirm hook fires.

**TDD approach**: No code tests. Documentation deliverable.

**Deliverables**:

1. `specs/009-rtk-cce-enforcement/validation.md` — step-by-step validation procedure for RTK rewrite hook
2. Verified `rtk gain --history` output showing at least one rewritten command

**Verification**:

```
Follow validation.md steps. Confirm rtk gain --history shows entries.
```

**Acceptance Gate**:
- [ ] Validation doc exists and is followable
- [ ] `rtk gain --history` confirms hook activity

## File Inventory

| Phase | New Files | Count |
| --- | --- | --- |
| 0 | `hooks/check-rtk-in-docs.py`, `tests/hooks/test_check_rtk_in_docs.py` | 2 |
| 1 | (modify existing) `.agents/skills/cce-mcp/SKILL.md` | 0 |
| 2 | `scripts/audit_rtk_cce.py`, `tests/scripts/test_audit_rtk_cce.py` | 2 |
| 3 | `specs/009-rtk-cce-enforcement/validation.md` | 1 |

**Total new**: ~5 | **Total modified**: ~2 (`cce-mcp/SKILL.md`, `prek.toml`)

## Library Best Practices

No external libraries. stdlib only (`re`, `pathlib`, `sys`, `argparse` for hooks).

Session audit uses `session_store_sql` MCP tool — not a Python library import.

## Risk Register

| Risk | Mitigation |
| --- | --- |
| RTK-eligible command list becomes stale | Keep list in a constant at top of hook; update when RTK adds new command support |
| False positives on non-shell code blocks (e.g., Python, JSON) | Only flag blocks with `bash`, `sh`, `shell`, `console` language hints, or untagged blocks containing shell-like commands |
| Session store schema changes break audit script | Audit queries `session_store_sql` via MCP, not direct SQLite — schema coupling is minimal |
| RTK rewrite hook silently stops firing after VS Code update | Phase 3 validation doc provides manual check procedure; Scenario 4 acceptance criteria require periodic verification |
| `check-rtk-in-docs` conflicts with existing instruction files | Run hook against full repo during Phase 0 verification; fix or suppress existing violations before merging |
