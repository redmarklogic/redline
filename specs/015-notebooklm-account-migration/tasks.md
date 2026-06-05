# Tasks: NotebookLM Account Migration

**Input**: [plan.md](plan.md)
**Prerequisites**: Phase 0 (Founder account setup) must be complete before Phase 1 begins.
No Python code, no pytest — tasks are operational steps executed by Linda via MCP tools.

---

## Phase 0: Account Setup (Founder Action)

**Purpose**: New Google account authenticated with MCP; old-account notebooks deleted.

- [ ] T001 [Phase 0] Delete only Redline notebooks from old Google account via NotebookLM web UI — those listed in `register.json`; other projects' notebooks are left untouched
- [ ] T002 [Phase 0] Run `nlm login` in terminal and authenticate to new Google account
- [ ] T003 [Phase 0] Run `nlm login --check` and confirm success; run `nlm doctor` and confirm no errors

### Acceptance Gate — Phase 0

- [ ] T004 [Phase 0] Verify `notebook_list` via MCP returns an empty list (zero notebooks in new account)
- [ ] T005 [Phase 0] Confirm to Linda verbally: "mcp-notebooklm is operational in the new account"

---

## Phase 1: Agent Consultations

**Purpose**: Every agent owner has confirmed their notebook structure; proposed manifest written.

- [ ] T006 [Phase 1] Consult Graeme — present 6 geotechnical notebooks from `register.json`; surface source counts; discuss keep/decompose/split; reach written agreement; note 100-source-limit split plan for any at-risk notebooks
- [ ] T007 [P] [Phase 1] Consult Peter — present 5 AI & software notebooks; discuss keep/decompose/split; reach written agreement
- [ ] T008 [P] [Phase 1] Consult Matt — present `product-design-ux`; confirm keep or restructure
- [ ] T009 [P] [Phase 1] Consult John — present `digital-marketing-social-selling`; confirm keep or restructure
- [ ] T010 [P] [Phase 1] Linda self-review — confirm `information-architecture-km` and `technical-communication` structure
- [ ] T011 [Phase 1] Consult Mark — present 8 process/product notebooks; surface Peter's consumer usage of `writing-specs` and `org-design-team-topologies`; resolve `professional-services-firm-management` ownership; determine disposition of `legal-ai-startup`
- [ ] T012 [Phase 1] Consult Ron — present 3 advisory-board-only notebooks; ask about `legal-ai-startup` GTM/market-signal framing (depends on T011 — Mark's ownership decision must precede this)
- [ ] T013 [Phase 1] Compile proposed notebook manifest at `docs/people/drafts/015-proposed-notebook-manifest.md` — one row per proposed notebook: ID, name, description, access, primary agent, projected source count, split rationale, status = `draft`

### Acceptance Gate — Phase 1

- [ ] T014 [Phase 1] Verify manifest row count ≥ 26; all 7 consultations marked complete; no row with status = `unresolved` without a Founder-flag note
- [ ] T015 [Phase 1] Founder reviews and approves `docs/people/drafts/015-proposed-notebook-manifest.md`

---

## Phase 2: Notebook Design Plan

**Purpose**: Complete source file list per notebook; notebook-to-agent mapping table finalised.

- [ ] T016 [Phase 2] For each notebook in the approved manifest, locate source files under `G:\My Drive\Library` using the `library-management` skill; count files per notebook
- [ ] T017 [Phase 2] Flag any notebook where file count would exceed 100 post-split; confirm revised thematic split plan with relevant domain agent (Graeme for geotechnical-domain notebooks)
- [ ] T018 [Phase 2] Compile `SourceFileRecord` list per notebook (notebook_id, file_path, content_type, upload_status = `pending`)
- [ ] T019 [Phase 2] Produce notebook-to-agent mapping table (notebook ID, primary agent, secondary agents)
- [ ] T020 [Phase 2] Write design plan to `docs/people/drafts/015-notebook-design-plan.md` — notebook creation table + source file lists + mapping table; flag any notebooks with zero located sources

### Acceptance Gate — Phase 2

- [ ] T021 [Phase 2] Verify: no notebook in design plan has source count > 100; all notebooks have ≥ 1 source or a "not found" flag with resolution path
- [ ] T022 [Phase 2] Founder reviews and approves `docs/people/drafts/015-notebook-design-plan.md`

---

## Phase 3: Notebook Creation

**Purpose**: All approved notebooks exist in the new Google account with correct names and descriptions.

- [ ] T023 [Phase 3] For each `open`-access notebook in the design plan: call `notebook_create(name=..., description=...)`; record returned URL in `docs/people/drafts/015-register-draft.json`
- [ ] T024 [Phase 3] For each `advisory-board-only` notebook in the design plan: call `notebook_create(name=..., description=...)`; record returned URL in register draft
- [ ] T025 [Phase 3] For each created notebook: call `notebook_get` and verify name and description match the approved manifest; flag any mismatches

### Acceptance Gate — Phase 3

- [ ] T026 [Phase 3] Verify `notebook_list` count matches manifest row count
- [ ] T027 [Phase 3] Verify `docs/people/drafts/015-register-draft.json` — every entry has a non-empty, new-account URL
- [ ] T028 [Phase 3] Founder reviews register draft and confirms notebook list is correct before population begins

---

## Phase 4: Source Population and Register Promotion

**Purpose**: Every notebook populated with approved sources; `register.json` updated with live URLs.

- [ ] T029 [Phase 4] For each `open`-access notebook: iterate `SourceFileRecord` list; for each file — if `upload_status = pending` call `source_add` and set status to `uploaded` or `failed`; if `upload_status = not_found` skip without upload
- [ ] T030 [Phase 4] For each `advisory-board-only` notebook: same rule — upload `pending` files, skip `not_found` files
- [ ] T031 [Phase 4] For each notebook: call `notebook_get` to confirm final source count (uploaded files only); note discrepancies between expected and actual count
- [ ] T032 [Phase 4] Call `refresh_auth` if any `source_add` calls return auth errors mid-operation
- [ ] T033 [Phase 4] Confirm per-notebook source count back to each primary owner agent
- [ ] T034 [Phase 4] Send per-notebook source-count summary to Mark confirming completion
- [ ] T035 [Phase 4] Await Founder instruction; upon instruction: copy `docs/people/drafts/015-register-draft.json` to `.agents/skills/redline-research/register.json` (URL fields only update — preserve all other fields verbatim)

### Acceptance Gate — Phase 4

- [ ] T036 [Phase 4] Verify: no notebook has source count > 100 in `notebook_get` results
- [ ] T037 [Phase 4] Verify `register.json` — all entries have live, new-account URLs; no stale URLs remain
- [ ] T038 [Phase 4] Verify no other register fields were modified (names, descriptions, topics, access levels, added dates all unchanged)

---

## Execution Notes

- `[P]` = parallelizable (no dependency on another in-progress task)
- `[Phase N]` = which plan phase the task belongs to
- **T011 must precede T012** — Mark decides `legal-ai-startup` ownership before Ron is consulted on GTM/market-signal framing
- **T006 first** — Graeme's 6 notebooks include the highest 100-source-limit risk; surface splits early
- T007, T008, T009, T010 are independent of each other and of T006; run in parallel if possible
- Phase 3 open notebooks before advisory-board-only (T023 before T024)
- Phase 4 matches Phase 3 order
- If auth expires mid-Phase 4: call `refresh_auth` (T032), resume from last confirmed upload_status = `uploaded`
- No pytest gate applies — verification is via MCP tool calls (`notebook_list`, `notebook_get`)
- Commit `docs/people/drafts/` files after each phase acceptance gate passes
