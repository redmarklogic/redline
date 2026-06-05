# Spec 015: NotebookLM Account Migration — Notebook Redesign and Repopulation

**Issue**: [#39](https://github.com/redmarklogic/redline/issues/39)
**Owner**: Linda (Knowledge Infrastructure)
**Created**: 2026-06-05
**Status**: Draft
**Supersedes**: `docs/product/operations/work-orders/2026-06-04-linda-notebooklm-google-account-migration.md`

---

## Summary

Redline has migrated to a new Google account. The NotebookLM MCP CLI must be
re-authenticated, and all notebooks must be recreated in the new account. Rather than a
direct 1:1 recreation of the 26 notebooks currently in `register.json`, this spec takes a
redesign-first approach: Linda consults each agent owner before creating anything, opens
the notebook structure for review, and incorporates any requested decompositions,
consolidations, or restructuring into a reviewed manifest. Only after the manifest is
approved does creation begin.

---

## Constraints

### 100-Source Limit per Notebook

NotebookLM caps each notebook at 100 sources. Most notebooks are well within this limit.
The exceptions are standards-heavy notebooks, where the library may contain hundreds of
individual PDFs:

- `engineering-standards` — NZ infrastructure design standards (IDS), NZS 4431, and
  related regulatory documents; likely candidates for thematic splitting.
- `ground-engineering-magazine` — approximately 12 years of Ground Engineering issues
  (2014–2026); if individual issues are separate PDFs, this may exceed 100 sources.

Any notebook whose projected source count exceeds 100 MUST be split thematically (e.g.,
by jurisdiction, time period, or sub-domain) before creation. Each split notebook counts
as a separate register entry. Graeme decides the thematic boundaries for all
geotechnical-domain notebooks; Linda proposes the split and Graeme approves it during
Phase 1 consultation.

### MCP Prerequisite

Linda cannot create or populate notebooks without the NotebookLM MCP CLI authenticated
against the new Google account. Phase 0 is a blocking prerequisite for all subsequent
phases.

### Draft-First (Linda's Maturity Level)

All register.json changes go to `docs/people/drafts/` first. Founder promotes to
`register.json` directly at each review gate.

---

## Phases

---

### Phase 0 — Account Setup (Founder Action, Blocking)

**Goal**: New Google account has an authenticated, operational NotebookLM MCP CLI and no
stale notebooks from any prior migration attempt.

**Actions (Founder)**:

1. Delete all notebooks from the current (old) Google account via the NotebookLM UI.
2. Install and authenticate the NotebookLM MCP CLI against the **new** Google account.
3. Confirm to Linda that `mcp-notebooklm` is operational.

**Review gate — Phase 0 Exit**:

- [ ] Founder confirms: old account notebooks deleted
- [ ] Founder confirms: `mcp-notebooklm` authenticated to new account and operational

_Linda does not begin Phase 1 until both confirmations are received._

---

### Phase 1 — Agent Consultations

**Goal**: Every notebook owner has been consulted and has agreed on the notebook structure
they want in the new account. Linda produces a proposed notebook manifest that reflects
those agreements.

**Process**:

For each agent in the consultation schedule (see below), Linda:

1. Presents the agent's current notebooks (names, descriptions, source counts where known)
   from `register.json`.
2. Asks whether the agent wants to keep, decompose, consolidate, rename, or restructure
   any of their notebooks.
3. Answers "what resources do we have?" queries by checking the digital library
   (`G:\My Drive\Library`) and reporting what files are available in each topic area.
4. Continues the dialogue until the agent has confirmed the notebook structure they want.
5. Notes any notebooks whose projected source count exceeds 100 and flags required splits.

Linda does not make domain decisions. Thematic boundaries for splits are decided by the
domain agent, not by Linda.

**Consultation Schedule**:

| Agent  | Current notebooks (from register.json)                                                                                                                                                                       | Domain                         |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Graeme | engineering-standards, ground-engineering-magazine, geotechnical-baseline-reports, geotechnical-report-workflows, risk-assessment-engineering, geotechnical-checklists                                       | Geotechnical domain            |
| Peter  | ai-system-engineering, software-architecture-ddd, software-dev-methodology-eng-org, llm-token-optimisation-agentic-workflows, claude-max-20x-developer-workflow-research                                     | AI & software architecture     |
| Mark   | business-process-management, product-roadmapping, writing-specs, org-design-team-topologies, professional-services-firm-management, govcon-systems-engineering, legal-ai-startup, strategy-competitive-advantage | Process & product / strategy  |
| Matt   | product-design-ux                                                                                                                                                                                            | UX & design                    |
| Ron    | founder-memos (advisory-board-only), monetizing-scaling-innovation (advisory-board-only), entrepreneurship-startup-strategy (advisory-board-only), legal-ai-startup (consulted on GTM/market-signal framing) | Founder strategy               |
| John   | digital-marketing-social-selling (advisory-board-only)                                                                                                                                                       | Marketing                      |
| Linda  | information-architecture-km, technical-communication                                                                                                                                                         | Knowledge infrastructure (own) |

**Shared-notebook resolution**: `writing-specs` and `org-design-team-topologies` are owned
by Mark; Peter is a consumer, not an owner. Linda does not need to consult Peter on
ownership decisions for these notebooks, but Peter's usage needs should be surfaced during
Mark's consultation so Mark can make an informed decision. `professional-services-firm-management`
may be relevant to both Mark and Graeme; Linda flags this during both consultations and
notes any ownership disagreements for Founder resolution at the Phase 1 review gate.

**Output**: A proposed notebook manifest document at
`docs/people/drafts/015-proposed-notebook-manifest.md` containing:
- Each proposed notebook: ID, name, description, topic area, access level
- Owner agent(s) per notebook
- Projected source count and any required split rationale
- Any open disagreements flagged for Founder resolution

**Review gate — Phase 1 Exit**:

- [ ] Linda has consulted every agent in the schedule
- [ ] Each agent has confirmed their notebook structure
- [ ] All source-limit splits are proposed and approved by the relevant domain agent
- [ ] Shared-notebook ownership is resolved (or flagged for Founder)
- [ ] Proposed manifest is at `docs/people/drafts/015-proposed-notebook-manifest.md`
- [ ] **Founder reviews and approves the manifest** before Phase 2 begins

---

### Phase 2 — Notebook Design Plan

**Goal**: A complete, Founder-approved creation plan specifying every notebook, its
sources, and the notebook-to-agent mapping table.

**Actions (Linda)**:

1. For each notebook in the approved manifest, locate the corresponding source files in
   `G:\My Drive\Library` using the `library-management` skill.
2. Record the source file list per notebook.
3. Flag any notebooks where the located source count would exceed 100 and confirm the
   thematic split plan with the domain agent before proceeding.
4. Produce the design plan document at
   `docs/people/drafts/015-notebook-design-plan.md` containing:
   - Notebook creation table (one row per notebook with ID, name, access, source count,
     source file list, owner agent(s))
   - Notebook-to-agent mapping table (see schema below)
   - Any sources that cannot be located in the library (flagged for Founder)

**Notebook-to-Agent Mapping Table (schema)**:

| Notebook ID | Notebook Name | Access | Primary Agent | Secondary Agents |
|-------------|--------------|--------|---------------|-----------------|
| ...         | ...          | ...    | ...           | ...             |

**Review gate — Phase 2 Exit**:

- [ ] All notebooks have a confirmed source file list
- [ ] No notebook's source list exceeds 100 files (splits applied where needed)
- [ ] Missing sources are flagged with resolution path
- [ ] Notebook-to-agent mapping table is complete
- [ ] Design plan is at `docs/people/drafts/015-notebook-design-plan.md`
- [ ] **Founder approves the design plan** before notebook creation begins

---

### Phase 3 — Notebook Creation

**Goal**: All approved notebooks exist in the new Google account with correct names and
descriptions. No sources populated yet.

**Actions (Linda)**:

For each notebook in the approved design plan (open notebooks first, advisory-board-only
second):

1. Create the notebook in the new account via `mcp-notebooklm` with the canonical `name`
   and `description` from the approved manifest.
2. Record the new notebook URL.
3. Update the register draft at `docs/people/drafts/015-register-draft.json` with the new
   URL for each entry as it is created.

**Review gate — Phase 3 Exit**:

- [ ] All notebooks from the design plan are created in the new account
- [ ] Linda confirms: correct names and descriptions for all notebooks
- [ ] `docs/people/drafts/015-register-draft.json` has a new URL for every created notebook
- [ ] **Founder reviews the notebook list and register draft**

---

### Phase 4 — Source Population and Register Promotion

**Goal**: Every notebook is populated with its approved source list. `register.json` is
updated with live URLs and promoted from draft.

**Actions (Linda)**:

For each notebook in the design plan:

1. Upload each source file from `G:\My Drive\Library` to the notebook via `mcp-notebooklm`
   `source_add`.
2. Track the running source count per notebook.
3. After all sources are added, confirm the source count back to the primary owner agent.

After all notebooks are populated:

4. Confirm that no notebook has been populated with more than 100 sources.
5. Promote `docs/people/drafts/015-register-draft.json` to `.agents/skills/redline-research/register.json`
   (with Founder instruction; Linda drafts, Founder approves the write to the canonical
   path given Linda's Draft-First maturity level).
6. Confirm completion to Mark with a per-notebook source-count summary.

**Review gate — Phase 4 Exit**:

- [ ] Every notebook has been populated with its approved source list
- [ ] No notebook exceeds 100 sources
- [ ] Linda has confirmed source counts to each primary owner agent
- [ ] `register.json` updated — all entries have live URLs pointing to the new account
- [ ] No other register fields modified (names, descriptions, topics, access levels preserved)
- [ ] Founder confirms: register.json promoted to canonical path
- [ ] Linda confirms completion to Mark with per-notebook source-count summary

---

## Success Criteria

- **SC-001**: Every agent owner confirms (during Phase 1) that the notebook structure
  reflects their needs — no notebook was recreated without consultation.
- **SC-002**: No notebook in the new account has more than 100 sources.
- **SC-003**: All 26+ notebooks (including any new split notebooks) exist in the new
  Google account with correct names, descriptions, and access levels.
- **SC-004**: Every notebook is populated with sources traceable to `G:\My Drive\Library`.
- **SC-005**: `register.json` has a live URL for every notebook; no stale URLs remain.
- **SC-006**: The notebook-to-agent mapping table is complete and agreed upon.
- **SC-007**: Each phase has a Founder-reviewed artifact before the next phase begins.

---

## Open Questions (for Phase 1 Consultation)

These are flagged now so agents can come prepared:

1. **engineering-standards**: How many individual standard PDFs are in the library for
   this notebook? If over 100, should we split by jurisdiction (NZ vs international),
   by standard type (earthworks, foundations, site investigation), or by body (NZS, IDS,
   NZGS)?
2. **ground-engineering-magazine**: Are individual magazine issues separate PDFs? If 2014–
   2026 yields more than 100 issues, should we split by year range or by thematic focus
   (editorial vs technical papers)?
3. **writing-specs / org-design-team-topologies**: Mark is the owner. During Mark's
   consultation, Linda surfaces that Peter also uses these notebooks so Mark can factor
   that into any restructuring decisions.
4. **professional-services-firm-management**: Primary owner Mark or Graeme? The content
   spans A/E/C firm management (Graeme-adjacent) and general PSF management (Mark's
   domain). Linda raises this in both consultations.
5. **legal-ai-startup**: Only two sources — a YC interview and a website. During Mark's
   consultation, Mark decides whether it warrants its own notebook or should be merged.
   Linda also asks Ron whether it belongs in a founder-strategy notebook given its GTM
   and market-signal relevance.

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| An agent requests a large structural change that requires resolving cross-agent dependencies | Phase 1 stalls or yields conflicting manifests | Founder resolves at the Phase 1 review gate before Phase 2 begins |
| Standards notebooks exceed 100 sources even after initial thematic splits | Notebook creation blocked | Flag during Phase 2 source location; refine split with domain agent before creation |
| Library files cannot be located for a source referenced in the old register | Notebook is populated with fewer sources than the old account | Flag missing files at Phase 2; Founder decides whether to defer, skip, or re-source |
| MCP authentication fails mid-operation (session timeout or token expiry) | Partially created or populated notebooks | Resume from last confirmed state; record progress per notebook in the register draft |
| Agent is unavailable during consultation | Phase 1 blocked | Notify Founder; proceed with available agents and hold a slot for the unavailable agent |
