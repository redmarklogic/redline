# Feature Specification: Token Optimisation via Code Context Engine

**Branch**: `feature/token-optimisation`
**Created**: 2026-05-26
**Status**: Draft

## Source Document Reconciliation

| Source | Authority | Status |
| --- | --- | --- |
| [Session analysis — chronicle:tips 2026-05-25](../../docs/meetings/) | Primary — observed patterns | Informs scope and acceptance criteria |
| [elara-labs/code-context-engine README](https://github.com/elara-labs/code-context-engine) | Primary — tool spec | Informs install steps and capabilities |
| Peter's review of token-optimisation diagnosis (2026-05-25) | Supporting — architectural advisory | Shapes priority and risk framing |

### Key Findings from Source Documents

The session analysis identified `read_file` accounting for 307 of 358 file-access events
(86%) across 50 sessions. Sessions accumulate 45–75 turns, with the majority of file reads
being full-file rather than targeted. Code Context Engine (CCE) replaces full-file reads
with indexed chunk retrieval, shifting the model's tool-selection behaviour toward
`context_search` without requiring user habit changes.

CCE's published benchmark (94% retrieval savings) is measured against full-file reads of
Python source code. This repo is primarily Markdown (skills, agent JDs, ADRs, docs).
Markdown is supported but AST-parsing advantages do not apply. Conservative estimate for
this repo: **50–70% reduction in context tokens per session**.

**Critical risk**: `cce init --agent copilot` writes output compression rules directly into
`AGENTS.md`. This file is a highly curated, binding system prompt. Any CCE-injected rules
must be reviewed against existing conventions (no emoji, no section rules, no default env
values) before the change is committed.

## Scope

This spec covers **installation, configuration, and validation** of CCE as a local MCP
server for the Redline VS Code Copilot workflow.

It does not cover:
- Python source-code chunk search (the repo has minimal Python relative to Markdown)
- `session_recall` / cross-session decision memory (separate feature, separate spec)
- Output compression tuning beyond default `standard` level
- Multi-device or cloud sync

## Scenarios (mandatory)

### Scenario 1 — CCE installs and registers as an MCP server in VS Code

A developer runs `cce init --agent copilot` in the repo root. After restarting VS Code,
the Copilot agent has access to `context_search` and related CCE tools. The `.vscode/mcp.json`
is populated with the CCE server entry. No existing MCP servers are removed or overwritten.
The embedding model downloads and the initial index completes without error.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 2              | 85             | 1                    | 8.5        |

**Independent test**: Open VS Code, open Copilot Chat in agent mode, ask "cce: what tools
are available?" and verify `context_search` is listed.

**Acceptance criteria**:

1. **Given** a clean repo with an empty `.vscode/mcp.json`,
   **when** `cce init --agent copilot` runs to completion,
   **then** `.vscode/mcp.json` contains a valid CCE server entry pointing at the installed
   `cce` executable.

2. **Given** CCE is installed,
   **when** `cce status` is run,
   **then** it reports the index as current, the embedding backend as active (fastembed
   local or Ollama), and shows the file count for the repo.

3. **Given** CCE has indexed the repo,
   **when** `cce index` is run a second time without file changes,
   **then** it completes in under 5 seconds (cache hit rate ≥ 90%).

4. **Given** the repo uses `uv`,
   **when** CCE is installed,
   **then** it is installed via `uv tool install "code-context-engine[local]"` so it
   remains consistent with the repo's package management conventions.

---

### Scenario 2 — Semantic search retrieves the correct skill files from natural-language queries

A developer queries CCE with natural-language prompts that match known content in the
`.agents/skills/` tree. The retrieval returns the correct files in the top-5 results for
a defined set of probe queries, establishing a Recall@5 baseline before any sessions run
with CCE active.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 2              | 60             | 1                    | 6.0        |

Confidence is 60% (not higher) because CCE's published benchmarks are for Python source
code. Markdown file recall has not been independently validated by the team.

**Independent test**: Run each probe query via `cce search "<query>"` and record the
top-5 results. Pass threshold is Recall@5 ≥ 0.70 (correct file in top 5 for ≥ 70% of
probes).

**Probe query set** (10 queries, deterministic):

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

**Acceptance criteria**:

1. **Given** CCE has indexed the full repo,
   **when** each probe query is run via `cce search`,
   **then** the expected file appears in the top-5 results for ≥ 7 of 10 queries
   (Recall@5 ≥ 0.70).

2. **Given** the Recall@5 result is recorded,
   **when** this spec is reviewed,
   **then** the actual score is committed alongside the spec as
   `specs/005-token-optimisation/recall-baseline.md`.

3. **Given** Recall@5 < 0.70,
   **when** the result is reviewed,
   **then** the feature is considered blocked: do not merge CCE MCP config, and open
   a follow-on investigation into re-indexing strategy or alternative tools.

---

### Scenario 3 — AGENTS.md injection is safe and convention-compliant

`cce init` writes output compression rules into `AGENTS.md`. Before any commit that
includes CCE-modified content in `AGENTS.md`, a reviewer verifies the injected rules
do not conflict with existing repo conventions.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 1              | 95             | 0.5                  | 9.5        |

This scenario is a quality gate, not a feature. Its RICE score reflects the cost of
ignoring it (corrupted system prompt, agent misbehaviour).

**Independent test**: Diff `AGENTS.md` before and after `cce init`. Manually review each
injected line against the conventions checklist below.

**Acceptance criteria**:

1. **Given** `cce init --agent copilot` has run,
   **when** `AGENTS.md` is diffed against the pre-init version,
   **then** no injected line contains emoji, unicode symbols, or section separator rules
   (e.g., `# ---`).

2. **Given** the diff is reviewed,
   **when** CCE injects output compression rules,
   **then** the injected block is contained within a clearly delimited section
   (e.g., `<!-- cce:start -->` / `<!-- cce:end -->`) so it can be removed cleanly.

3. **Given** the injected block sets output compression level,
   **when** the compression level is `standard` or lower,
   **then** it is accepted; if CCE defaults to `max`, it must be overridden to `standard`
   before committing.

4. **Given** any injected rule conflicts with an existing AGENTS.md directive,
   **when** the conflict is identified during review,
   **then** the conflicting CCE rule is removed and the existing directive takes
   precedence.

5. **Given** `cce uninstall` is run,
   **when** `AGENTS.md` is inspected,
   **then** all CCE-injected content has been cleanly removed with no residual lines.

---

### Scenario 4 — Token savings are measurable after two working sessions

After CCE is active and two normal working sessions have completed, `cce savings` reports
a reduction in context tokens relative to the pre-CCE baseline established in the session
analysis (307 `read_file` calls / 50 sessions ≈ 6 per session average).

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 2              | 55             | 0.5                  | 11.0       |

Confidence is 55% because CCE's savings metric is measured relative to a full-file
baseline, not against Copilot's actual prior behaviour.

**Independent test**: Run `cce savings` after two sessions and record output. Compare
`read_file` call count in session store against pre-CCE baseline from chronicle data.

**Acceptance criteria**:

1. **Given** two sessions have run with CCE active,
   **when** `cce savings` is run,
   **then** it reports at least 1 session with measurable token savings (non-zero).

2. **Given** the session store is queried post-CCE,
   **when** `read_file` call counts are compared to the pre-CCE baseline (6/session),
   **then** the mean `read_file` calls per session is ≤ 4 (≥ 33% reduction).

3. **Given** `cce savings` output is captured,
   **when** this spec is closed,
   **then** the savings report is committed to `specs/005-token-optimisation/savings-baseline.md`.

---

## Out of Scope

| Item | Reason |
| --- | --- |
| `session_recall` / `record_decision` tools | Cross-session memory is a separate capability. Address in a follow-on spec after CCE baseline is validated. |
| Python source-code AST search | Minimal Python relative to Markdown in this repo. CCE's AST advantage does not apply to the primary content type. |
| Output compression level tuning | Default `standard` is sufficient for initial rollout. Tuning requires session data. |
| Multi-device or cloud sync | Single developer, single device. No cloud sync needed. |
| Replacing `grep_search` / `semantic_search` built-in tools | CCE supplements, does not replace, VS Code's built-in tools. |
| CI/CD integration or git hook for auto-reindex | Post-validation concern. Add only if index staleness becomes a problem in practice. |

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Recall@5 < 0.70 on Markdown files | Medium | High — feature delivers no value | Scenario 2 is a blocking gate. If recall is poor, do not proceed. |
| CCE corrupts or conflicts with `AGENTS.md` | Low | High — breaks all agent sessions | Scenario 3 acceptance criteria + `cce uninstall` rollback plan. |
| Embedding model download fails on Windows | Low | Low — install blocked temporarily | Use `[local]` extra which bundles fastembed; fallback to Ollama if needed. |
| CCE MCP server conflicts with future MCP servers in `.vscode/mcp.json` | Low | Low — easy to resolve manually | `.vscode/mcp.json` is currently empty; document CCE's entry format. |
| Savings are unmeasurable because CCE targets code, not skills | Medium | Medium — investment with no payoff | Scenario 4 acceptance criteria establish a post-hoc exit condition. |
