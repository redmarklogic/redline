# Implementation Plan: NotebookLM Account Migration

**Date**: 2026-06-05 | **Spec**: [spec.md](spec.md)
**Status**: Draft

---

## Summary

Recreate all Redline NotebookLM notebooks in a new Google account following a migration.
Rather than a direct 1:1 recreation, the plan opens a consultation window with each agent
owner before creation begins, allowing restructuring and thematic splits (required where
source counts would exceed NotebookLM's 100-source limit). Linda executes the plan via the
`mcp-notebooklm` MCP tool; the Founder reviews the output of each phase before the next
begins.

---

## Technical Context

**Infrastructure**: NotebookLM MCP CLI (`notebooklm-mcp-cli`); `nlm` CLI for auth
**MCP tools used**: `notebook_create`, `notebook_list`, `notebook_get`, `source_add`, `refresh_auth`, `server_info`
**Data store**: `.agents/skills/redline-research/register.json` (SSOT for notebook metadata)
**Library**: `G:\My Drive\Library` (source files for notebook population)
**Staging path**: `docs/people/drafts/` (all draft outputs before Founder promotion)
**No Python code, no pytest, no uv** — this is an operational process executed by Linda via MCP.

---

## Design Decisions

| # | Decision | Choice | Rationale |
| --- | --- | --- | --- |
| D1 | Approach | Consult-before-create | Agents get a say in restructuring; prevents recreating a suboptimal structure 1:1 |
| D2 | Register updates | Draft-first to `docs/people/drafts/` | Linda's Draft-First maturity level; Founder promotes to canonical path |
| D3 | Creation order | `open` notebooks first, `advisory-board-only` second | Reduces risk of access/permission issues early; open notebooks are lower-stakes to debug |
| D4 | `notebook_create` permission | Knowledge Operator exception added | Required for migration; exception scoped narrowly to migration and provisioning workflows |
| D5 | Source-limit splits | Structural options from Linda; thematic boundaries from domain agent | Linda counts files and proposes structural options (e.g., split by year, by jurisdiction); the domain agent decides which sources belong in which split — that is a domain decision Linda does not make |

---

## Domain Impact

**New packages**: None
**Bounded context changes**: None
**Import-linter contract updates**: None
**Subdomain classification**: Generic (operational process, no domain model)
**New domain terms**:

- `NotebookManifestEntry` — unit of agreement from Phase 1 consultation; captures the
  agreed notebook structure before creation begins (see [data-model.md](data-model.md))

---

## MoSCoW

| Category | Items |
| --- | --- |
| **Must have** | Phase 0 (account setup), Phase 1 (agent consultations), Phase 3 (notebook creation), Phase 4 (source population + register promotion) |
| **Should have** | Phase 2 design plan as a formal written artifact with source file lists |
| **Could have** | Automated source-count reconciliation between old and new account |
| **Won't have (this time)** | Automated re-ingestion pipeline; automated notebook creation from register.json without consultation; multi-account support |

---

## Phased Delivery

### Phase 0: Account Setup (Founder Action)

**Goal**: New Google account has an authenticated, operational `mcp-notebooklm` and zero
notebooks. Old account notebooks are deleted.

**Deliverables (Founder)**:

1. Redline notebooks deleted from old account via NotebookLM web UI (`register.json` entries only — other projects' notebooks left untouched)
2. `nlm login` completed against new Google account
3. `nlm login --check` returns success
4. Verbal confirmation to Linda that MCP is operational

**Verification**:

```text
nlm login --check   → success
nlm doctor          → no errors
notebook_list       → returns empty list
```

**Acceptance Gate** (Founder confirms before Phase 1 starts):

- [ ] Redline notebooks deleted from old account (`register.json` entries only; other projects untouched)
- [ ] `nlm login --check` success in new account
- [ ] `notebook_list` returns empty list

---

### Phase 1: Agent Consultations

**Goal**: Every agent owner has confirmed their notebook structure. Linda produces the
proposed notebook manifest at `docs/people/drafts/015-proposed-notebook-manifest.md`.

**Consultation order**: Graeme → Peter → Mark → Matt → Ron → John → Linda (self-review)

**Per-consultation steps**:

1. Present current notebooks from `register.json` (name, description, projected source count)
2. Ask: keep, decompose, consolidate, rename, or restructure?
3. Answer "what do we have?" queries from library inspection
4. Flag any notebooks where projected source count exceeds 100; surface split options
5. Record agreement; note unresolved items for Founder

**Deliverables**:

1. `docs/people/drafts/015-proposed-notebook-manifest.md` — one row per proposed notebook
   with: ID, name, description, access, primary agent, projected source count, split
   rationale (where applicable), and status = `draft`

**Verification**:

```text
Count rows in manifest == count of confirmed notebooks (≥26, may be more if splits added)
All agents in consultation schedule appear in the "consulted" column
No row has status = "unresolved" without a Founder-flag note
```

**Acceptance Gate** (Founder reviews before Phase 2 starts):

- [ ] All 7 consultations completed
- [ ] Manifest at `docs/people/drafts/015-proposed-notebook-manifest.md`
- [ ] All source-limit splits proposed and approved by domain agent
- [ ] Founder approves manifest

---

### Phase 2: Notebook Design Plan

**Goal**: Complete source file list per notebook. Notebook-to-agent mapping table
finalised. Design plan at `docs/people/drafts/015-notebook-design-plan.md`.

**Steps**:

1. For each notebook in the approved manifest, locate source files in `G:\My Drive\Library`
   using the `library-management` skill
2. Count sources per notebook; flag any that would exceed 100 post-split
3. Record `SourceFileRecord` list per notebook
4. Produce design plan document including notebook-to-agent mapping table

**Deliverables**:

1. `docs/people/drafts/015-notebook-design-plan.md` — notebook creation table + source
   file lists + notebook-to-agent mapping table

**Verification**:

```text
No notebook in the plan has a source file count > 100
All notebooks have at least 1 source file located (or "no sources found" flagged)
Mapping table covers all notebooks in the manifest
```

**Acceptance Gate** (Founder reviews before Phase 3 starts):

- [ ] All notebooks have confirmed source file lists
- [ ] No notebook exceeds 100 sources
- [ ] Missing sources flagged with resolution path
- [ ] Founder approves design plan

---

### Phase 3: Notebook Creation

**Goal**: All approved notebooks exist in the new Google account with correct names and
descriptions. No sources yet.

**Steps**:

For each notebook in the design plan (open first, advisory-board-only second):

1. Call `notebook_create(name=..., description=...)`
2. Record returned URL in `docs/people/drafts/015-register-draft.json`
3. Call `notebook_get` to verify name and description match manifest

**Deliverables**:

1. All notebooks created in new account
2. `docs/people/drafts/015-register-draft.json` — full register array with new URLs

**Verification**:

```text
notebook_list   → count matches manifest row count
notebook_get(each)   → name and description match manifest
015-register-draft.json   → all entries have a non-empty, new-account URL
```

**Acceptance Gate** (Founder reviews before Phase 4 starts):

- [ ] All notebooks from design plan created in new account
- [ ] Names and descriptions verified against manifest
- [ ] Register draft has new URL for every notebook

---

### Phase 4: Source Population and Register Promotion

**Goal**: Every notebook populated with its approved source list. `register.json` updated
with live URLs and promoted from draft.

**Steps**:

For each notebook:

1. Iterate `SourceFileRecord` list from design plan:
   - `upload_status = pending` → call `source_add`; update status to `uploaded` or `failed`
   - `upload_status = not_found` (flagged in Phase 2) → skip; do not attempt upload
2. Track running source count (uploaded files only) per notebook
3. After all files processed: call `notebook_get` to confirm final count
4. Confirm uploaded count and skipped (`not_found`) count back to primary owner agent;
   agent decides whether to re-source skipped files or accept partial population

After all notebooks:

1. Verify no notebook exceeds 100 sources
2. Confirm completion to Mark with per-notebook source-count summary
3. Await Founder instruction to promote `docs/people/drafts/015-register-draft.json`
   to `.agents/skills/redline-research/register.json`

**Deliverables**:

1. All notebooks populated with approved sources
2. Per-notebook source-count confirmation sent to each primary owner agent
3. Per-notebook source-count summary sent to Mark
4. `register.json` promoted to canonical path (Founder action)

**Verification**:

```text
notebook_get(each)   → source count matches design plan expected count
register.json   → all 26+ entries have live URLs; no stale old-account URLs remain
```

**Acceptance Gate** (final):

- [ ] All notebooks populated; no notebook exceeds 100 sources
- [ ] Source counts confirmed to each primary owner agent
- [ ] register.json promoted; all entries have live URLs
- [ ] No other register fields modified (names, descriptions, topics, access preserved)

---

## File Inventory

| Phase | Artifact | Type |
| --- | --- | --- |
| 1 | `docs/people/drafts/015-proposed-notebook-manifest.md` | New |
| 2 | `docs/people/drafts/015-notebook-design-plan.md` | New |
| 3 | `docs/people/drafts/015-register-draft.json` | New |
| 4 | `.agents/skills/redline-research/register.json` | Updated (URLs only) |

**Total new**: 3 draft files | **Total updated**: 1 canonical file

---

## Risk Register

| Risk | Mitigation |
| --- | --- |
| Agent consultation yields conflicting manifest decisions | Founder resolves at Phase 1 review gate before Phase 2 begins |
| Standards notebook exceeds 100 sources even after split | Flag during Phase 2; refine split with Graeme before creation |
| Library files cannot be located for a register-listed source | Flag in Phase 2 design plan; Founder decides defer, skip, or re-source |
| MCP auth expires mid-operation | Call `refresh_auth`; fallback to `nlm login`; resume from last confirmed state in register draft |
| Agent unavailable for consultation | Notify Founder; hold a consultation slot open; proceed with available agents |
| `notebook_create` rate-limited (bulk creation of 26+ notebooks) | Space creation calls; use `server_info` to check server state; batch in groups of 5–10 |
