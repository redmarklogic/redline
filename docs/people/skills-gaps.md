# Skills Gaps & Lifecycle Ledger

**Owner (steward):** Harriet
**Last updated:** 2026-06-13

> **SOT for skill coverage gaps and pending lifecycle actions.** This is the capability
> governor's working ledger — consulted at hires, audits, topology syncs, and sprint
> planning. It deliberately holds the volatile state that must **not** appear in the
> catalog ([skills-taxonomy.md](skills-taxonomy.md)) or the placement rulebook
> ([skills-architecture.md](../architecture/skills-architecture.md)).
>
> Log a gap here when identified during a hire, audit, or sync — with proposed
> remediation and status. Close rows by marking **Live** or **Resolved** with a date;
> prune resolved rows at the following quarterly Topology Sync (history survives in git
> and in the dated sync reports under `docs/people/drafts/reports/`).

---

## Pending skills (identified, not yet created)

| Gap | Identified by | Proposed remediation | Status |
|---|---|---|---|
| `ux-professional-software` (information-dense UI, document-centric interaction, form design) | Harriet (2026-04-20, Matt hire) | Query `Product Design & UX` and `Information Architecture and Knowledge Management` notebooks; draft skill using `writing-skills` TDD cycle | Pending notebook grounding |
| `ux-conversion-design` (co-development partner conversion UX, 10→100→1000 phasing) | Harriet (2026-04-20, Matt hire; rescoped 2026-05-09) | Route through John for `Monetizing & Scaling Innovation` and `Digital Marketing & Social Selling` notebooks; combine with `Product Design & UX`; draft skill using `writing-skills` TDD cycle | Pending notebook grounding + John consultation |
| `ux-document-design` (document-as-product design for generated DOCX output) | Harriet (2026-05-09, Matt scope expansion) | Query `Product Design & UX` notebook for document design principles; consider Word/OOXML formatting constraints; draft skill using `writing-skills` TDD cycle | Pending — Sprint 1 priority |
| `ux-taskpane-design` (Word taskpane add-in interaction patterns) | Harriet (2026-05-09, Matt scope expansion) | Deferred until P-024 unfreezes. Query `Product Design & UX` notebook when ready | Deferred (P-024) |
| `ux-email-as-interface` (email template design for co-development and impact communication) | Harriet (2026-05-09, Matt scope expansion) | Collaborate with John on email copy patterns; draft skill using `writing-skills` TDD cycle | Deferred — Phase 2 |
| `knowledge-infrastructure` (library curation, notebook maintenance, register upkeep, standards monitoring) | Harriet (2026-04-25, Linda hire) | Query `Information Architecture and Knowledge Management` notebook; draft skill using `writing-skills` TDD cycle | Pending notebook grounding |
| 13 GCP/DevOps skills: Cloud Run deploy, CI/CD pipeline, IAM least-privilege, Cloud SQL, IAP/OAuth wiring, observability, cost controls, container tuning, WIF, multi-tenancy, Secret Manager, infra-boundary-contract, `terraform-iac` (added 2026-06-10 per ADR-020) | Harriet (2026-06-06, Brent topology screen; +1 at 2026-06-10 sync) | Ground from "DevOps & GCP Infrastructure" and "GCP DevOps Tactical Playbook"; `terraform-iac` additionally from HashiCorp documentation. Author with `writing-skills` TDD cycle. Until written, Brent uses WebFetch + Context7. Brent's validated Delta (2026-06-10): `terraform-iac` gains state surgery (`import`/`mv`/`rm`), provider-pinning maintenance, 6.x→7.x upgrade checklist; IAP/OAuth wiring skill must be updated **before issue #73 work begins** — direct IAP-on-Cloud-Run is GA, staling the JD template's audience format | Deferred — next sprint (GitHub issue) |
| `office-js-word-addin` (Office.js find/mark/replace; content-control marking; reader-visible highlight pairing; per-occurrence tagging; human-in-the-loop snippet verification; WordApi 1.1 floor) | Harriet (2026-06-13, #185 Office.js spike capability-gap assessment; founder-approved) | **Draft authored** at `docs/people/drafts/skills/office-js-word-addin/SKILL.md`, grounded in #185 v2 spike evidence + Microsoft Learn API reference (Context7/WebFetch, 2026-05 docs). RED→GREEN verified via `writing-skills` TDD: 2 baseline probes failed (missed paired highlight, missed per-occurrence tag, over-reached for raw-XML proof); same 2 probes pass with skill present. **Owner = Kabilan** (vendored-JS implementation scope, per his JD patch 2026-06-13). **BLOCKING: Peter or Kabilan must validate the engineering substance** (API calls, requirement-set claims, gotcha framing) before promotion to `.agents/skills/` and registration in `skills-lock.json` + taxonomy | Draft — pending engineering sign-off |

## Grounding & extension work on live skills

| Item | Identified by | Proposed remediation | Status |
|---|---|---|---|
| `engineering-architecture` grounding + salvage port from deleted `arch-engineering` (Common Mistakes table; Decision Persistence / `record_decision` section; grounding-sources list) plus two stale-pointer fixes ("Does Not Cover" cites pre-split `evaluation-architecture`; cited notebook ID `cdb5e862-…` NOT_FOUND — correct register ID `91568710-98b3-4448-b038-04f9b48b7111`) | Harriet (2026-05-16, Peter hire); Peter Delta (2026-06-10) | One commit with sync item A-5. **2026-06-12: `arch-engineering/` folder verified absent from disk** — deletion executed; confirm the salvage port landed before closing this row | Salvage + pointer fixes pending verification |
| `design-eval-rubric` + `design-eval-pipeline` notebook grounding (formerly `evaluation-architecture`; split 2026-05-31) | Harriet (2026-05-16, Peter hire) | Query `Software Development Methodology & Engineering Organisation` and `AI System Engineering` notebooks | Stubs live — grounding pending |
| `shaping` notebook grounding | Harriet (2026-05-16, Peter hire) | Query `Software Development Methodology & Engineering Organisation` notebook for Shape Up content | Stub promoted — grounding pending |
| `define-ai-policy` + `enforce-ai-batch-discipline` grounding (formerly `ai-acceptable-use-policy`; split 2026-05-31) | Harriet (2026-05-16, Peter hire) | Query methodology notebook for DORA content; incorporate external DORA 2024-2026 research | Stubs live — grounding + external research pending |
| `create-adr` extension: reciprocal status convention + partial-supersession pattern (status-line-only update on the partially superseded ADR; body immutable) | Peter Delta (2026-06-10) | Peter supplies content; founder approves; ADR-023 is the first exercise. Sync items S-6/A-24 | Pending founder approval |
| `marketing-product-led-seo` AI-citation-visibility annex (+ Big 5 note) and `linkedin-social-selling` saves/dwell metric update | John Delta (2026-06-10) — directional, secondary sources only | Corroboration-gated: Linda sources one primary reference each; then John drafts annexes; founder approves. Sync items S-9/A-26 | Blocked on primary sourcing |
| `linkedin-social-selling` metric-currency annex | John (2026-06-10) | Pending corroboration (see row above) | Blocked |
| `notebooklm-cli` re-verification at `notebooklm-mcp-cli` 0.7.2 (running 0.7.0) | Linda Delta (2026-06-10, PyPI evidence) | Founder approves upgrade; Linda re-verifies command table. Sync items S-10/A-22 | Pending founder approval |
| `hr-sync-agent-topology` protocol amendment: R2 question 1 unanswerable by static corpora (null = valid output); add dispatched-session prerequisites (NotebookLM path via `nlm`, record CCE/ToolSearch availability) | Linda + Mark Deltas (2026-06-10); 4 of 8 sessions had no NotebookLM path | Harriet supplies amendment text; founder applies. Sync items S-5/A-23 | Pending founder approval |
| Standards-monitoring procedure mechanics (Linda): amendment-level tracking, withdrawal flagging, overseas-standards tracking, update-service subscription; feed-tooling question (only `snz_scraper.py` exists) | Linda Delta (2026-06-10) | Bundled with founder decision A-18 (extend tooling vs narrow Outcome 4); Harriet drafts Linda JD patch only if narrowed. Sync item S-11 | Pending founder decision |

## Lifecycle & registry hygiene

| Item | Identified by | Action | Status |
|---|---|---|---|
| SRP new-violations: `prek-find-and-fix`, `test-find-and-fix` (structural "and" in names) | Harriet (2026-06-10, SRP Compliance Pass) | Both mirror the approved `sonarqube-find-and-fix` `justified-orchestrator` pattern. Founder to approve adding both (plus the `sync-agent-topology` → `hr-sync-agent-topology` rename) to the Known Exception Skip-List in `hr-sync-agent-topology/procedures/srp-scan-procedure.md` before next sync | Pending founder approval |
| `receiving-code-review` status `deprecated` in `skills-lock.json` | — | Excluded from catalog; remains at L0 in the rulebook while the folder exists. Delete folder + lock entry, or re-activate, at next sync | Deprecated |
| **2026-06-12 registry surgery (this refactor):** 5 ghost entries removed from `skills-lock.json` — `ai-acceptable-use-policy`, `evaluation-architecture`, `hiring-agent-management` (all split, successors live), `marketing-social-selling-linkedin` (renamed `linkedin-social-selling`), `branching-strategy` (no successor recorded — **orphan**, folder absent, content fate unknown) | Founder session (2026-06-12) | `branching-strategy`: confirm whether content was absorbed (e.g. into `git-version-control`) or lost; restore or formally retire at next sync. Others: no action — successors registered | `branching-strategy` open; rest closed |
| **2026-06-12 registry back-fill:** 21 live local skills added to `skills-lock.json` (previously unregistered — ADR-009 orphan detection was blind to them): `adr-constitution-sync`, `create-adr`, `customization-mechanism-triage`, `define-ai-policy`, `design-eval-pipeline`, `design-eval-rubric`, `enforce-ai-batch-discipline`, `engineering-architecture`, `hr-audit-agent`, `hr-hire-agent`, `hr-maintain-agent-registry`, `linkedin-social-selling`, `mental-models`, `prek-find-and-fix`, `python-fastapi`, `session-handover`, `sonarqube-find-and-fix`, `sonarqube-review`, `sonarqube-scan`, `test-find-and-fix`, `tool-selection`. `tier` and `owner_agent` derived from the pre-refactor taxonomy "Used by" column and sibling precedent | Founder session (2026-06-12) | **Harriet ratifies tier/owner; Peter ratifies the 7 new layer assignments** (`adr-constitution-sync` L8, `customization-mechanism-triage` L8, `engineering-architecture` L8, `prek-find-and-fix` L8, `test-find-and-fix` L8, `sonarqube-scan` L5, `sonarqube-review` L5; `task-defer` L8 legitimised — was lock-only). Next sync | Pending ratification |
| Agent–skill topology mermaid diagrams deleted from `skills-architecture.md` (contained three live errors: `python-style`/`doc-updater` mislayered, stale `sync-agent-topology` name) | Founder session (2026-06-12) | Topology visuals are henceforth generated from `skills-lock.json` per sync and embedded dated in sync reports — never hand-maintained | Closed (policy) |

## Historical notes (closed; retained one cycle)

- `agile-sprint-planning` / `agile-daily-standup` lock entries — verified present 2026-06-11 (tier `planning`, owner `mark`, layer 9). **Resolved.**
- `tool-selection` promoted to `.agents/skills/tool-selection/` (ADR-016, 2026-06-06); stale draft duplicate deleted, `docs/people/drafts/skills/` verified empty 2026-06-10. **Live.**
- `ddd-strategic` promoted with 3 procedures (May 2026). **Live.**
- `dev-environment` dependency-management extension; `python-domain-modeling` layer-architecture extension; `version-control` PR-discipline extension — all **Live** (2026-05-23).
- Phantom rows corrected at the 2026-06-10 sync: `marketing-social-selling-linkedin` (real folder `linkedin-social-selling`), `skills-create` (absorbed into `writing-skills`, founder ruling 2026-06-12), `hiring-agent-management` (split into `hr-*` family).
- ADR-001 layer-SSOT filename mismatch (audit Q4, 2026-06-11) — **fixed 2026-06-12** in ADR-001 and `hooks/sync-layer-to-lock.py`.
