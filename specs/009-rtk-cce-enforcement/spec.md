# Feature Specification: RTK + CCE Enforcement

**Feature Branch**: `009-rtk-cce-enforcement`

**Created**: 2026-05-30

**Status**: Draft

**Input**: Build enforcement mechanisms ensuring AI agents consistently use RTK (token-optimised CLI proxy) for shell commands and CCE (Code Context Engine) for codebase discovery, rather than falling back to raw commands and `read_file` sweeps.

---

## Source Document Reconciliation

| Source | Authority | Status |
| --- | --- | --- |
| `.github/instructions/rtk.instructions.md` | Primary — agent instruction | Defines RTK prefix rule |
| `.agents/skills/cce-mcp/SKILL.md` | Primary — skill spec | Defines CCE usage patterns |
| `.github/hooks/rtk-rewrite.json` | Primary — existing hook | Copilot PreToolUse rewrite for RTK |
| `specs/005-token-optimisation/spec.md` | Supporting — prior spec | CCE installation/validation (separate scope) |
| Session analysis (chronicle data) | Supporting — observed patterns | 307 of 358 file-access events via `read_file` |

### Key Findings from Source Documents

RTK is a CLI proxy that filters and compresses terminal output, saving 60–90% of output tokens. An `rtk.instructions.md` file applies to all files (`applyTo: "**"`) and a `rtk-rewrite.json` PreToolUse hook exists to rewrite Copilot commands. However, no validation exists to confirm the rewrite hook fires, no metrics track compliance, and no pre-commit checks enforce RTK mentions in instruction files.

CCE provides semantic search over the codebase via MCP tools (`context_search`, `expand_chunk`, `session_recall`). The `cce-mcp` skill documents when to prefer `context_search` over `read_file`. However, enforcement is purely advisory — agents routinely fall back to `read_file` sweeps for discovery, consuming excessive context tokens.

The existing enforcement pattern in this repo uses `prek` pre-commit hooks (see `hooks/` directory) for static checks. RTK and CCE enforcement can follow the same pattern where applicable (instruction file checks), but agent runtime behaviour requires different mechanisms (session auditing, instruction reinforcement).

## Scope

This spec covers:
- Validation that RTK and CCE enforcement mechanisms are active and functioning
- Pre-commit hooks checking instruction/skill files reference RTK/CCE correctly
- Session audit tooling to measure RTK and CCE compliance rates
- Instruction reinforcement to reduce agent drift

Out of scope:
- CCE installation and setup (covered by spec 005)
- RTK CLI development or feature changes (upstream tool)
- Output compression tuning
- Multi-agent orchestration changes

---

## Scenarios (mandatory)

### Scenario 1 — Pre-commit hook validates RTK enforcement in instruction files (Priority: P1)

A developer creates or modifies an instruction file (`.instructions.md`, `SKILL.md`, or agent JD) that contains shell command examples. The pre-commit hook checks that shell commands in code blocks use the `rtk` prefix where applicable.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 2              | 85             | 1                    | 8.5        |

**Independent test**: Create a test instruction file with a bare `git status` in a code block. Run the hook. Verify it flags the violation.

**Acceptance criteria**:

1. **Given** an instruction file with `git status` in a fenced code block, **when** the pre-commit hook runs, **then** it reports a violation with the line number and suggests `rtk git status`.

2. **Given** an instruction file with `rtk git status` in a fenced code block, **when** the pre-commit hook runs, **then** it passes with no violations.

3. **Given** a code block with `python -m pytest` (not a known RTK-eligible command), **when** the hook runs, **then** it does not flag it (RTK-eligible commands are: `git`, `pytest`, `ruff`, `docker`, `uv`, `pip`, `mypy`).

4. **Given** a code block annotated with `<!-- rtk:skip -->` on the preceding line, **when** the hook runs, **then** it skips that code block.

5. **Given** the hook is registered in `prek.toml`, **when** `prek run` executes, **then** the hook runs as part of the standard pre-commit checks.

---

### Scenario 2 — Session audit reports RTK and CCE compliance rates (Priority: P1)

After a working session, a developer runs a compliance audit that analyses the session store for RTK and CCE usage patterns. The audit reports: (a) percentage of shell commands that used `rtk` prefix, (b) ratio of `context_search` to `read_file` calls for discovery, and (c) specific violations with turn numbers.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 3              | 60             | 2                    | 4.5        |

**Independent test**: Run a session with known RTK/CCE violations, then run the audit script and verify it correctly identifies the violations.

**Acceptance criteria**:

1. **Given** a session with 10 terminal commands where 7 used `rtk` prefix, **when** the audit runs, **then** it reports 70% RTK compliance.

2. **Given** a session with 15 `read_file` calls and 5 `context_search` calls, **when** the audit classifies discovery-vs-targeted reads, **then** it reports the CCE adoption ratio (context_search / total discovery reads).

3. **Given** the audit output, **when** violations are listed, **then** each violation includes: turn number, tool name, command/file, and suggested alternative.

4. **Given** the audit is packaged as a script in `scripts/`, **when** run via `python -m scripts.audit_rtk_cce`, **then** it completes without errors and writes output to stdout.

---

### Scenario 3 — CCE preference is reinforced in the cce-mcp skill (Priority: P2)

The `cce-mcp` skill is updated with explicit enforcement language and a decision tree that agents follow before calling `read_file`. The skill makes the preference actionable, not just advisory.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 1.5            | 90             | 0.5                  | 13.5       |

**Independent test**: Read the updated skill and verify the decision tree covers the three main `read_file` scenarios (discovery, targeted edit, full-file need).

**Acceptance criteria**:

1. **Given** the updated `cce-mcp/SKILL.md`, **when** an agent reads it, **then** it contains a decision tree: "Before calling `read_file`: (1) Am I discovering/exploring? → use `context_search`. (2) Do I know the exact file and need full content for editing? → use `read_file`. (3) Do I need a specific function/section? → use `context_search` + `expand_chunk`."

2. **Given** the skill's "Common Mistakes" table, **when** reviewed, **then** it includes a row for "Using `grep_search` for semantic queries" → "Use `context_search` which combines vector + BM25".

3. **Given** the skill update, **when** the `cce-mcp` skill description in the skills list is checked, **then** it accurately reflects the enforcement language.

---

### Scenario 4 — RTK rewrite hook is validated and monitored (Priority: P2)

The existing `.github/hooks/rtk-rewrite.json` PreToolUse hook is validated to confirm it actually fires and rewrites commands. A simple validation test exists that can be run on demand.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 1.5            | 70             | 0.5                  | 10.5       |

**Independent test**: Trigger a terminal command in Copilot Chat without `rtk` prefix and verify the rewrite hook modifies it.

**Acceptance criteria**:

1. **Given** the `rtk-rewrite.json` hook is present, **when** Copilot executes `git status` via `run_in_terminal`, **then** the actual command executed is `rtk git status`.

2. **Given** the hook validation test exists as a documented procedure in `specs/009-rtk-cce-enforcement/validation.md`, **when** a developer follows the steps, **then** they can confirm the hook is active within 2 minutes.

3. **Given** `rtk gain --history` is run after a session, **when** the output is reviewed, **then** it shows at least one rewritten command, confirming the hook fired.

---

## Non-Functional Requirements

- All hooks follow existing `hooks/` patterns: module docstring, `find_violations()`, `main() -> int`
- No new dependencies beyond stdlib for hooks
- Audit script may depend on `session_store_sql` tool (already available)
- All new files must be indexed by CCE after creation (`reindex`)
