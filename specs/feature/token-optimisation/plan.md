# Implementation Plan: Token Optimisation via Code Context Engine

**Date**: 2026-05-26 | **Spec**: [spec.md](../../005-token-optimisation/spec.md)
**Status**: Draft

## Summary

We are installing and validating Code Context Engine (CCE) as a local MCP server for the
Redline VS Code Copilot workflow. CCE indexes the repo and exposes a `context_search` tool
that the Copilot agent calls instead of issuing full-file `read_file` calls. No Python
code is written. The work is entirely tooling configuration, recall validation, and
instruction-file review. A blocking recall gate (Recall@5 ≥ 0.70) prevents merging if
CCE's Markdown retrieval quality is insufficient.

## Technical Context

**Tool**: `code-context-engine[local]` v0.4.x (PyPI)
**Package manager**: uv (`uv tool install`)
**Embedding backend**: fastembed + ONNX Runtime (`BAAI/bge-small-en-v1.5`, ~60 MB, CPU-only)
**Index storage**: `.context-engine/` (local, gitignored)
**MCP config**: `.vscode/mcp.json` (currently empty, to be populated by CCE)
**Instruction injection**: `.github/copilot-instructions.md` (new file, created by CCE)
**Dev OS**: Windows (requires Visual Studio Build Tools C++ workload + CMake)
**Key risk**: Recall@5 on Markdown files is unvalidated. Gate blocks merge if < 0.70.
**No Python packages added. No import-linter changes. No pyproject.toml changes.**

## Design Decisions

| # | Decision | Choice | Rationale |
| -- | --- | --- | --- |
| D1 | Embedding backend | `fastembed` (`[local]` extra) | Self-contained, no daemon required, works offline after first model download. Ollama is a valid fallback if build tools are absent. |
| D2 | Init scope | `cce init --agent copilot` (not `--agent all`) | Only VS Code Copilot is in use. `--agent all` would create config files for Claude Code, Cursor, Gemini CLI — none of which are used and would add noise to the repo. |
| D3 | `.github/copilot-instructions.md` ownership | Review and keep if convention-compliant; remove CCE block if conflicting | This file does not currently exist. CCE creates it with a `<!-- CCE:BEGIN -->` / `<!-- CCE:END -->` block. Content must not duplicate or contradict `AGENTS.md` directives. |
| D4 | Git hook for auto-reindex | Accept CCE's default (installed by `cce init`) | The hook is a post-commit hook that re-indexes changed files. Consistent with existing pre-commit hook conventions. Remove with `cce uninstall` if it proves noisy. |
| D5 | `.context-engine/` index storage | Gitignore | The index is machine-local and regenerable. Committing it would pollute history and cause merge conflicts. |
| D6 | Recall gate threshold | Recall@5 ≥ 0.70 across 10 deterministic probe queries | Conservative given Markdown-only content. Fail-fast before any sessions use CCE if retrieval quality is insufficient. |

## Domain Impact

**New packages**: None  
**Bounded context changes**: None  
**Import-linter contract updates**: None  
**Subdomain classification**: Generic (off-the-shelf tooling, no custom domain model)  
**New domain terms**: None

## Architecture

CCE sits between the Copilot agent and the codebase. On each turn, instead of the model
issuing `read_file` calls to retrieve full files, the Copilot agent calls `context_search`
via MCP. CCE returns ranked chunks with confidence scores. The model receives only the
relevant chunk, not the full file.

```
Copilot Agent (VS Code)
       |
       | MCP call: context_search("TDD red green refactor")
       v
  CCE MCP Server (cce serve)
       |
       | Hybrid retrieval: BM25 + vector (BAAI/bge-small-en-v1.5)
       v
  .context-engine/ (SQLite, sqlite-vec)
       |
       | Returns: top-k chunks with confidence scores
       v
  Copilot Agent — receives compressed chunk, not full file
```

**Before CCE**: 307 `read_file` calls / 50 sessions = 6.1/session average  
**Target after CCE**: ≤ 4 `read_file` calls/session (≥ 33% reduction)

## MoSCoW

| Category | Items |
| --- | --- |
| **Must have** | CCE installed via `uv tool install`; `.vscode/mcp.json` populated; Recall@5 ≥ 0.70 validated; `.github/copilot-instructions.md` injection reviewed |
| **Should have** | `.context-engine/` in `.gitignore`; baseline savings recorded in `specs/005-token-optimisation/`; post-commit reindex hook active |
| **Could have** | `cce savings` dollar estimates tracked per session; `session_recall` / `record_decision` for cross-session memory (separate spec) |
| **Won't have (this time)** | Output compression level tuning; multi-device sync; Ollama backend; Python source-code AST benchmarking |

## Phased Delivery

### Phase 0: Prerequisites and Install

**Goal**: CCE is installed and runnable. Build tools are confirmed. `cce --version` exits 0.

**Deliverables**:

1. Build tool verification (cmake + C compiler present — no file change, just gate check)
2. CCE installed: `uv tool install "code-context-engine[local]"`
3. `.context-engine/` added to `.gitignore`

**Verification**:

```powershell
cmake --version                   # must exit 0
cce --version                     # must print version string
```

**Acceptance Gate** (must pass before Phase 1 starts):
- [ ] `cce --version` exits 0 and prints a version string
- [ ] If cmake is absent: document the Ollama fallback path and proceed with `uv tool install code-context-engine` (no `[local]`)

---

### Phase 1: Init, Index, and Instruction Review

**Goal**: CCE indexes the repo, registers with VS Code Copilot, and the injected instruction file is reviewed and confirmed safe.

**Deliverables**:

1. `.vscode/mcp.json` — populated with CCE server entry
2. `.github/copilot-instructions.md` — created by CCE, reviewed against checklist
3. Repo fully indexed (`.context-engine/` populated)

**Verification**:

```powershell
cce init --agent copilot          # runs index + writes config files
cce status                        # reports index current, file count, embedding backend
```

**Instruction review checklist** (manual, blocking):
- [ ] No emoji or unicode symbols in injected content
- [ ] No directives that contradict `AGENTS.md` (no emoji, no section separator rules, no default env values)
- [ ] Compression level is `standard` or lower — if `max`, override to `standard` in `.context-engine.yaml`
- [ ] `<!-- CCE:BEGIN -->` / `<!-- CCE:END -->` markers present so block is removable

**Acceptance Gate** (must pass before Phase 2 starts):
- [ ] `.vscode/mcp.json` contains `"context-engine"` server entry
- [ ] `cce status` reports index as current
- [ ] Instruction review checklist fully checked off — no blocking items
- [ ] VS Code reloaded (`Developer: Reload Window`) and `context_search` is available in Copilot Chat agent mode

---

### Phase 2: Recall Validation (Blocking Gate)

**Goal**: Establish Recall@5 baseline. Confirm CCE retrieves correct skill files for known queries. This phase is a go/no-go decision point.

**Deliverables**:

1. `specs/005-token-optimisation/recall-baseline.md` — results for all 10 probe queries

**Probe queries** (run each as `cce search "<query>"`):

| # | Query | Expected file |
| --- | --- | --- |
| Q1 | "how to write a failing test before code" | `python-testing-unit/SKILL.md` |
| Q2 | "TDD red green refactor cycle" | `test-driven-development/SKILL.md` |
| Q3 | "hiring agents PIP performance review" | `hiring-agent-management/SKILL.md` |
| Q4 | "deep research 5 whys intake notebooklm" | `notebooklm-deep-research/SKILL.md` |
| Q5 | "ruff linting suppression rules" | `python-linting/SKILL.md` |
| Q6 | "git commit conventions pre-commit hooks" | `version-control/SKILL.md` |
| Q7 | "spec kit specify CLI implementation plan" | `spec-kit/SKILL.md` |
| Q8 | "brainstorming socratic design before code" | `brainstorming/SKILL.md` |
| Q9 | "PR review comments resolution cycle" | `resolving-pr-issues/SKILL.md` |
| Q10 | "ADR architecture decision record" | `engineering-architecture/SKILL.md` |

**Verification**:

```powershell
cce search "how to write a failing test before code"   # check top-5 for python-testing-unit/SKILL.md
# ... repeat for each query
```

**Acceptance Gate**:
- [ ] Expected file in top-5 results for ≥ 7 of 10 queries (Recall@5 ≥ 0.70)
- [ ] Results recorded in `specs/005-token-optimisation/recall-baseline.md`
- [ ] **If Recall@5 < 0.70**: STOP. Do not commit `.vscode/mcp.json`. Run `cce uninstall` to clean up. Open follow-on investigation.

---

### Phase 3: Baseline Measurement

**Goal**: Confirm CCE reduces `read_file` calls in live sessions. Run two normal working sessions with CCE active and record savings.

**Deliverables**:

1. `specs/005-token-optimisation/savings-baseline.md` — `cce savings` output + session store comparison

**Verification**:

```powershell
cce savings                       # run after 2 sessions; capture output
```

Then query the session store:

```sql
SELECT COUNT(*) as read_file_calls, COUNT(DISTINCT session_id) as sessions
FROM session_files
WHERE tool_name = 'read_file'
  AND first_seen_at >= datetime('now', '-3 days')
```

**Acceptance Gate**:
- [ ] `cce savings` reports non-zero savings for at least 1 session
- [ ] Mean `read_file` calls/session ≤ 4 (vs pre-CCE baseline of 6.1)
- [ ] Savings output committed to `specs/005-token-optimisation/savings-baseline.md`

## File Inventory

| Phase | Files Changed / Created | Notes |
| --- | --- | --- |
| 0 | `.gitignore` | Add `.context-engine/` |
| 1 | `.vscode/mcp.json` | Populated by CCE |
| 1 | `.github/copilot-instructions.md` | Created by CCE, reviewed before commit |
| 1 | `.context-engine/` | Index directory — gitignored, not committed |
| 2 | `specs/005-token-optimisation/recall-baseline.md` | Manual results recording |
| 3 | `specs/005-token-optimisation/savings-baseline.md` | Manual savings recording |

**Total new committed files**: ~3 | **Total deleted**: 0

## CCE CLI Reference (confirmed from docs)

### `code-context-engine[local]`

- **Install**: `uv tool install "code-context-engine[local]"`
- **Init**: `cce init --agent copilot`
- **Status**: `cce status`
- **Search**: `cce search "<query>"`
- **Savings**: `cce savings`
- **Uninstall**: `cce uninstall` (removes MCP config, instruction block, git hook; does NOT delete index)
- **Index refresh**: `cce reindex` (force full re-index)
- **Config file**: `.context-engine.yaml` in repo root (override compression level, embedding model)
- **Windows note**: Requires Visual Studio Build Tools (C++ workload) + CMake for `[local]` extra. If absent, use `uv tool install code-context-engine` with Ollama running.

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Recall@5 < 0.70 on Markdown files | Medium | High | Phase 2 is a blocking gate. `cce uninstall` if fail. |
| `.github/copilot-instructions.md` content conflicts with `AGENTS.md` | Low | High | Phase 1 checklist review before any commit. |
| Visual Studio Build Tools absent on Windows | Low | Low | Ollama fallback documented in Phase 0. |
| CCE git hook fires on every commit and slows workflow | Low | Low | Remove hook via `cce uninstall --hooks` if disruptive. |
| `cce savings` reports 0 (CCE not being called) | Low | Medium | Verify `context_search` appears in session_files after Phase 3 sessions. |
