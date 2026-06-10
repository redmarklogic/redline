# Agent Topology Sync Report

**Date:** 2026-06-10
**Previous sync:** 2026-06-07
**Facilitating agent:** Harriet (Head of People & Agent Development, Draft-first)
**Branch:** `master`. Invoked directly by the founder.
**Skill executed:** `.agents/skills/hr-sync-agent-topology/SKILL.md` (Reflection Protocol R1–R4 restored from git history 2026-06-10; current file treated as authoritative).

---

## 1. Trigger Validation

| Trigger criterion | Met? | Evidence |
|---|---|---|
| Quarterly cadence (90 days) | No | 3 days since 2026-06-07 |
| New agent hired **and onboarded** | **Yes** | Brent promoted to `.claude/agents/brent.md` 2026-06-07 (commit `bd39b32`) — *after* the 06-07 sync report recorded the hire as pending; reciprocal handoffs landed in Kabilan/Peter/Linda JDs; ADR-001 SSOT pass 2026-06-08 (`415c43a`) |
| Major strategy pivot / new bet | No | `strategic-bets.md` unchanged in window |
| Significant product milestone shipped | **Yes** | Deploy chain shipped 2026-06-09/10: specs 004 (health endpoint), 005 (GCP baseline + Docker), 006 (infra ADR), 70 (Cloud Run staging+prod with Secret Manager); ADR-019 (revised), ADR-020, ADR-021, ADR-022 accepted; PR #97 merged (`2185f9b`) |
| Client feedback batch | No | None processed in window |

**Verdict: VALID** — two independent triggers (new hire onboarded; milestone shipped).

## 2. Environment Disclosure — Reflection Protocol Deferred (honestly recorded)

- **No Agent tool exists in this session's toolset** (platform 1-hop circuit breaker — Harriet is herself running as a dispatched agent). Despite explicit founder authorization to dispatch reflecting agents, no dispatch mechanism was available. Per the founder's standing instruction, **no Delta Statement was authored on any agent's behalf** (unlike the in-absentia synthesis of 2026-06-06/07).
- Consequence per procedure step 8: **all reflecting agents are flagged as "no Delta Statement"; their self-reported JD changes are deferred.** Facilitator-drafted patches were produced only where drift is unambiguous from repository evidence — the same path the founder mandated for Kabilan.
- Reflection Protocol Steps R2 (NotebookLM queries) and R3 (online currency checks) were **not executed** — they belong to the reflecting agents, who could not run.
- **CCE MCP (`session_recall` / `context_search`) unavailable this session** (per founder note; no ToolSearch available to load deferred MCP tools). All discovery was done on repo evidence (git log, file reads, grep).
- Session-start staleness check (per `hr-hire-agent/procedures/session-start-staleness-check.md`): all nine pre-existing JDs last updated 2026-06-08 (`415c43a`; Mark again 2026-06-10, `c6eed1d`); decision-bearing changes postdating them: ADR-019 revision, ADR-020/021/022, specs 005/006/70, PR #97. **All agents flagged stale; this ceremony is the response.**
- **Postscript — A-8 executed the same day; this section is retained as honest history of the morning run.** The founder dispatched all eight reflecting agents from the main-thread session; verbatim Delta Statements are on disk at `docs/people/drafts/reports/delta-statements-2026-06-10/` (`_index.md` = collection record, per-agent R1–R3 completion, session IDs). Two environment findings from the live collection, logged here once centrally (per Mark's recommendation): (1) **no NotebookLM access path existed in four of the eight dispatched sessions** — Ron, Mark, John, and Brent could not run R2 (no NotebookLM MCP server in the session toolset); Graeme, Matt, Linda, and Peter reached their notebooks via the `nlm` CLI. (2) **CCE `session_recall` was unavailable to all eight** (no ToolSearch in subagent toolsets); discovery fell back to direct repo reads, honestly recorded by each agent. Linda's protocol observation: R2 question 1 ("what has been updated since [date]") is **structurally unanswerable by static book corpora** — both her notebooks returned explicit nulls; null answers are valid protocol output, not protocol failure (skill amendment proposed, trigger S-5). Sections 3–5, 7, 10, and 12 below are updated from the Delta evidence; §6 (SRP pass) stands unchanged — `violations-list.md` is unaffected by the statements.

## 3. Participation — UPDATED post-A-8 (live Delta collection, 2026-06-10)

All eight reflecting agents participated with verbatim Delta Statements, collected via founder-authorized main-thread dispatch. Evidence: `docs/people/drafts/reports/delta-statements-2026-06-10/` (`_index.md` carries the collection record).

| Status | Agents | Notes |
|---|---|---|
| Participated with live Delta Statement (R1 + R3 complete) | Ron, Mark, John, Graeme, Matt, Linda, Peter, Brent | R2 run live: Graeme (3 of 7 owned notebooks — proportionality), Matt (owned + 2 consumer notebooks), Linda (both assigned), Peter (2 of 6 — declared narrowing). R2 **not run** (no NotebookLM access path in the dispatched session): Ron, Mark, John, Brent — re-run owed when notebook access exists (see §2 postscript, F-5) |
| No-dispatch by standing hard rule (facilitator-drafted path) | Kabilan | Unchanged |
| Deferred | **None** | The morning run's blanket deferral is resolved; every reflecting agent's self-reported JD position is now on the record |

## 4. Drift Summary — UPDATED: morning assessment → live Delta verdict

| Agent | Morning assessment (repo evidence) | Live Delta verdict (2026-06-10) |
|---|---|---|
| **Brent** | **High — 3 contradictions with accepted ADRs** (Terraform prohibition vs ADR-020; stale `infra/` File Authority after `09d6d8f`; IAP-gated Outcome 2 vs ADR-022) | **Confirmed HIGH by Brent — "all three flagged contradictions are real and evidence-backed."** All six facilitator patches validated; two wording amendments requested and applied (Patch 1 "current" → "maintained" per ADR-020; Patch 4 Infra-Ready template IAP fields made conditional, audience format noted stale vs direct IAP-on-Cloud-Run GA). New from his R3: google provider 7.x GA → 6.x→7.x upgrade evaluation on his backlog (no JD change); direct-IAP finding feeds issue #73 (Peter's successor auth ADR) |
| **Harriet** | One stale routing row (`sync-agent-topology` → `hr-sync-agent-topology`) | Unchanged — facilitator, no self-statement. Patch stands at `drafts/agents/harriet.agent.md` (A-2) |
| Peter | None in JD; owns the F-3 follow-up | **Confirmed — no JD patch required** (his words; routing verified current incl. Brent rows). F-3 verdict: **author ADR-023, partial supersession** — supersedes this report's original "amend/annotate" wording (A-6 rewritten). V-1 **confirmed: deprecate `arch-engineering`**, with a one-commit salvage condition + 2 stale-pointer fixes in `engineering-architecture` (S-7). Proposes: `create-adr` partial-supersession pattern + reciprocal status convention (S-6); a Touch-2 checklist line ("does the spec treat any ADR Out-of-Scope item as in-scope?") — swiss-cheese fix for the F-3 process gap; one-page platform synthesis in `docs/architecture/` (Larson: synthesize after ~5 design docs; we have a fresh 4-ADR cluster) |
| Kabilan | None requiring JD change | No statement (standing no-dispatch hard rule) — facilitator assessment stands unchanged |
| Mark | Low; `/standup` routing row left as an open nit | **Confirmed low — no JD change. Declines the `/standup` routing row** with structural reasoning: the command is founder-invoked and mechanical; its "do not ask for clarification" mandate conflicts with his sharpening-question hard constraint; a second invocation path violates SSOT spirit (ADR-001). Conditional fallback — a one-line Crisp Boundaries addition — pends his sharpening question to the founder (A-15). New flags: duplicate `specs/005-*` numbering (F-4 / A-14); PRD-amendment provenance nit (312-line product amendment landed in commit `45f6904` titled "docs(skills): add python-fastapi skill") |
| Linda | None repo-evidenced | **Confirmed — no material JD drift.** Structural finding: Outcome 4 claims monitoring of four standards feeds (ISO, BSI, Standards NZ, Standards AU) but the only permanent tooling is `snz_scraper.py` — extend-or-narrow decision routed to founder (A-18). Her owned notebook `technical-communication` is currency-stale by its own admission (sources 2000–2014) — currency review routed to consumers + founder (A-17). Protocol observation → S-5. `nlm` CLI two patch releases behind → S-10 |
| Ron | None repo-evidenced | **Confirmed — no JD change required** (Team API correctly has no Brent interface; infra evidence routes via Peter as designed). Bet-artifact drift, Ron-owned: **Bet 1 kill-criterion anchor ambiguity** (fixed-date 2026-09-01 vs "from launch" — founder decision, A-13); Bet 7 evidence base lags the DORA ROI 2026.01 report (Peter independently surfaced the same report — converging evidence); Bet 6 Beca/BEYON watch-item annotation. Minor: weekly-KPI discipline should anchor to `docs/product/tasks/this-week.md` — noted for his next REFRESH; no patch (declared no JD change) |
| John | None repo-evidenced | **Self-reported two JD defects — patch drafted** (`drafts/agents/john.agent.md`, A-20): (1) campaign gate cites nonexistent `docs/product/personas/` (verified on disk; artifact is `docs/product/strategy/personas.md`) — gate unsatisfiable as written; (2) signal-report constraint lacks a pre-launch mode — the missed June report (due 06-01, self-identified) was a structural breach (no instrumentation exists). Also: publication-status confirmation requested for the Craig Lewis email vs the empty AI-review log (A-11); reduced-scope June retro-file proposed (A-12); two skill-currency candidates held pending primary corroboration (S-9). Verified independently that no published claim is invalidated by ADR-022 |
| Graeme | None repo-evidenced | **Confirmed — no JD patch required.** Domain moved within remit (2 GE Magazine notebooks added, report-workflows populated 06-09, 4 knowledge entries; zero domain terms in the window's merged specs — no gate bypassed). Self-owned follow-ups: second-generation Eurocode 7 transition document (defer via `task-defer` or write on first domain question); CPEng/PEngGeol sign-off coverage check (feeds Peter's rubric). Watch item routed to Linda: NZGS/MBIE module revisions tied to the NSHM review. Fixed the knowledge-index date header directly (his own file) |
| Matt | None repo-evidenced | **Four JD patch items self-proposed, all evidence-grounded — patch drafted** (`drafts/agents/matt.agent.md`, A-21): (1) JD's inline notebook inventory is factually false (claims 7 books; live `nlm source list` shows 4) → replace with SSOT pointer (ADR-001); (2) zero accessibility requirements → WCAG 2.2 AA baseline (AHRC-affirmed DDA minimum, covers SaaS); (3) Website Review Protocol hardcodes non-resolving `mcp_microsoft_pla_browser_*` identifiers → canonical Playwright MCP names; (4) Self-Review gains worst-case-data stress check + partner-feedback reconcile hook. Critical-path ask: **Peter's Touch 1 memo for the Skeleton Generator — `specs/shaped/` is empty 20 days from the 06-30 ship target** (F-6 / A-19). Sourcing request to Linda (A-16) |

## 5. Gap & Overlap Analysis

### 5.1 Orphan responsibilities

| # | Orphan | Evidence | Proposed owner / resolution |
|---|---|---|---|
| O-1 | **Terraform HCL authoring + `terraform state` operations** | ADR-020 mandates Terraform for all GCP infra and assigns state ops to Brent; Brent's live JD excludes Terraform authoring; Kabilan's scope excludes cloud infra. Terraform files in repo were authored through founder/spec-kit flow with no accountable agent | **Brent** — patch drafted AND **validated by Brent 2026-06-10** (Delta §4; his §1 already claims the ownership: "per ADR-020, newly — the Terraform HCL under `deploy/infra/terraform/` plus `terraform state` operations"). Absorption confirmed; promotion pends A-1 |
| O-2 | **Brent absent from `AGENTS.md`** (roster + Agent Dispatch Policy table) | AGENTS.md lists no Brent entry; dispatch table has no Brent rows, yet his JD defines blocking Peter escalation and Linda routes cloud-source triage to him. Under "any dispatch not in this table is not permitted", Brent's escalations are formally unauthorized | Founder applies proposed text (§8) — AGENTS.md is outside Harriet's write authority |
| O-3 | **`arch-engineering` skill unrouted** | No JD routes to it; frozen since `acba676` (2026-05-31) | Deprecate/delete (founder approval; `.agents/skills/` outside Harriet's authority) |
| O-4 | `skills-lock.json` entries for `agile-sprint-planning` / `agile-daily-standup` | Skills live on disk, absent from the lock file (authoritative per ADR-001/ADR-009) | Engineering/founder adds entries (carried from taxonomy gap table) |

### 5.2 Overlap conflicts

| # | Overlap | Resolution proposal |
|---|---|---|
| V-1 | `arch-engineering` ↔ `engineering-architecture` — near-identical trigger descriptions (dispatch-routing hazard); `arch-engineering` additionally claims "writing ADRs", overlapping `create-adr`'s declared SSOT | **CONFIRMED by Peter at live reflection: deprecate/delete, with a one-commit salvage condition.** Salvage into `engineering-architecture` before deletion: (a) the 7-row Common Mistakes table, (b) the Decision Persistence section (`record_decision` discipline — AGENTS.md-mandated, absent from the successor), (c) the grounding-sources list (Team Topologies, Accelerate, Farley, Larson, Beck — feeds S-4); discard its weaker ADR Conventions (subset of `create-adr`, violates ADR-001 at skills layer). Same commit fixes 2 stale pointers Peter found live in `engineering-architecture`: "Does Not Cover" routes to pre-split `evaluation-architecture` (should be `design-eval-rubric`/`design-eval-pipeline`); cited notebook ID `cdb5e862-…` returns NOT_FOUND (correct register ID: `91568710-98b3-4448-b038-04f9b48b7111`). Founder executes (A-5); deletion is git-reversible — low-stakes, decide fast |
| **V-2** | **Persona artifact: claimed authority vs actual location.** Mark's JD declares **direct write authority** over `docs/product/personas/` (co-owned with Ron) — a directory that does not exist; John's JD gated campaigns on the same nonexistent path (now patched, A-20); the real artifact is `docs/product/strategy/personas.md`, inside **Ron's** write domain. Three agents' maps disagree with one territory | Founder + Ron + Mark decide the canonical location (A-25): materialise `docs/product/personas/` and move the artifact (matches Mark's declared co-ownership), or keep personas in the strategy file and patch Mark's JD path. John's patched gate follows the artifact either way. Surfaced by John's Delta §3.1; Mark's JD claim verified by facilitator |
| — | Agent File Authority: **no other overlaps detected.** Brent (`deploy/infra/`, `deploy/docker/`, `.github/workflows/`, `.env.example`, `docs/infrastructure/`) vs Kabilan (`src/rl/`, `tests/`, `scripts/`, `hooks/`) vs Peter (`docs/adr/`, `docs/architecture/`, `docs/evaluation/`, `specs/shaped/`) remain disjoint after the path relocation. The eight Delta Statements' "what I own today" sections were cross-mapped against the agent register: no two agents claim the same responsibility (Brent's Terraform claim is the O-1 absorption, by design) | n/a |

### 5.3 Team API friction

- **F-1 (= O-2):** Brent's Tier-1 escalation to Peter and Linda's cloud-source routing to Brent exist in JDs and the org chart but not in AGENTS.md's dispatch table. Until fixed, the policy text and the JDs disagree. *(Unchanged by the statements; founder applies §8.)*
- **F-2:** AGENTS.md header "Four named personas" now lists six (Ron, Mark, Graeme, John, Matt, Peter), and the epistemic-honesty clause omits Matt. Cosmetic but misleading for routing. *(Matt acknowledged at live reflection — awareness only; his JD carries the clause inline, behaviour unaffected. Founder applies §8.)*
- **F-3 — RESOLVED IN APPROACH (Peter's live verdict, seconded by Brent):** ADR-022 "Out of Scope" bullets vs shipped spec-70. Peter's verdict: **neither amend nor annotate — author ADR-023**, "Accepted, partially supersedes ADR-022 (scope statements only — the hosting decision stands)", with ADR-022's status line updated in the same commit (the one permitted immutability exception; body untouched). Grounding: `create-adr` Principle 4 + R2 verbatim (Richards & Ford: supersede, never amend; literature silent on partial supersession — Redline codifies the convention, S-6). ADR-022's own Ongoing consequence mandates the new ADR ("multi-environment split requires a new or amended ADR"). Brent seconded: his Hard Constraint 7 sides with spec-70; the stale document is ADR-022. Process gap (swiss-cheese): no layer catches "spec contradicts an accepted ADR's scope in the same week" — spec-70's own Assumptions cited the out-of-scope items, machine-visible, nobody looked. Short-runway fix: Peter adds one Touch-2 checklist line ("does the spec treat any ADR Out-of-Scope item as in-scope? If yes, ADR action precedes merge"); enforcement hook explicitly deferred (long-runway only). **Owner: Peter (A-6).**
- **F-4 (new — Mark):** Duplicate spec numbering on master: `specs/005-docker-deploy-setup/` AND `specs/005-gcp-project-baseline/` both tracked (facilitator-verified on disk). Traceability defect, not a JD defect. **Owner: Peter + founder — renumber or formally accept (A-14).**
- **F-5 (new — systemic, four statements + index):** Reflection-infrastructure gap. Dispatched agent sessions exposed no NotebookLM access path for Ron/Mark/John/Brent (R2 unrunnable), and CCE `session_recall` was unavailable to all eight (no ToolSearch in subagent toolsets). The Reflection Protocol assumes capabilities the dispatch environment does not guarantee. **Fix: S-5 protocol amendment + founder decision on tooling access for dispatched sessions (A-23).**
- **F-6 (new — Matt):** The Two-Touch pipeline is not flowing for the H2 priority. `specs/shaped/` is empty — no Touch 1 constraints memo exists for the Skeleton Generator while the ship target is 2026-06-30 (20 days out) and the deploy chain is live (PR #97). Design is formally blocked by Matt's own JD ("MUST NOT begin design work without a PRD" + Touch 1 gate). **Owner: Peter delivers Touch 1; Mark confirms PRD readiness (A-19). The single most schedule-critical item in this report.**

## 6. SRP Compliance Pass — COMPLETE

`violations-list.md` published at `docs/people/drafts/reports/violations-list.md` (mandatory artifact). Scan covered all 119 `SKILL.md` files.

| Disposition | Count | Items |
|---|---|---|
| **new-violation** | **2** | `prek-find-and-fix` (name), `test-find-and-fix` (name) |
| known-exception | 4 current matches | `sonarqube-find-and-fix`, `hr-sync-agent-topology` (skip-listed under old name), `ceremony-monthly-editorial-session`, `library-management` |
| false-positive | 24 | Category B grammatical/pipeline "and"s and one compound noun — see list |

**Resolution proposed for the 2 new-violations (must resolve before next sync):** both mirror the approved `sonarqube-find-and-fix` `justified-orchestrator` pattern. Founder approves a single edit to the Known Exception Skip-List in `hr-sync-agent-topology/procedures/srp-scan-procedure.md`: add `prek-find-and-fix` and `test-find-and-fix` as `justified-orchestrator`, and rename the stale `sync-agent-topology` entry to `hr-sync-agent-topology`. Harriet cannot apply this edit (Draft-first; `.agents/skills/` not founder-named as an edit target this session).

## 7. Skill Gap Triggers — UPDATED from Delta evidence

| # | Trigger | Source | Action |
|---|---|---|---|
| S-1 | **`terraform-iac`** (HCL authoring, plan/apply discipline, state ops, provider pinning, drift triage) — new | ADR-020; **Brent Delta §5 confirms as his highest-priority skill gap** and adds validated scope: state surgery (`import`/`mv`/`rm`), provider-pinning **maintenance**, and a 6.x→7.x upgrade-evaluation checklist (official upgrade guide documents the breaking changes) | Add to Brent's pending-skills set (now 13); ground from "DevOps & GCP Infrastructure" notebook (incl. Terraform IaC on GCP, Wang) + HashiCorp docs; author via `writing-skills` TDD cycle (A-10) |
| S-2 | SRP skip-list update (2 new-violations + rename) | §6 | Founder approves table edit (A-4) — unchanged |
| S-3 | 12 GCP/DevOps skills (carried) | 2026-06-06 screen | Deferred — next sprint (GitHub issue); Brent interim = WebFetch + Context7 — unchanged |
| S-4 | Carried: `ux-professional-software`, `ux-conversion-design`, `ux-document-design`, `knowledge-infrastructure`, grounding for Peter's four split stubs (`design-eval-*`, `define-ai-policy`, `enforce-ai-batch-discipline`) and `engineering-architecture` | Prior syncs | Per existing taxonomy gap table. **Update:** Peter's V-1 salvage supplies the missing grounding-sources list for `engineering-architecture` (Team Topologies, Accelerate, Farley, Larson, Beck — port from `arch-engineering/procedures/` before deletion, A-5) |
| **S-5** | **`hr-sync-agent-topology` protocol amendment**: (a) acknowledge that R2 question 1 ("what changed since [date]") is structurally unanswerable by static book corpora — null answers are valid protocol output, not failure; (b) add a dispatched-session prerequisite note: reflecting agents need a working NotebookLM path (`nlm` CLI) and should record CCE/ToolSearch availability; (c) R2 falls back to question 2 + R3 when the corpus is static | Linda Delta §3.4 (both her notebooks returned explicit nulls); Mark Delta §3 (log centrally); `_index.md` systemic-gap record; F-5 | Harriet supplies the amendment text; founder applies (`.agents/skills/` outside Harriet's write authority this session) — A-23 |
| **S-6** | **`create-adr`**: add the reciprocal status convention ("Accepted, supersedes ADR-NNN" / "Superseded by ADR-NNN") and a **partial-supersession pattern** (status-line-only update on the partially superseded ADR; body immutable) | Peter Delta §5.1 — R2 verbatim: the literature contains no partial-supersession guidance, so Redline codifies the convention ADR-023 will exercise | Peter owns content; founder approves the skill edit (A-24). ADR-023 is the first exercise of the pattern (A-6) |
| **S-7** | **`engineering-architecture`**: salvage port from `arch-engineering` (Common Mistakes table; Decision Persistence section — AGENTS.md-mandated, absent from successor; grounding-sources list) + 2 stale-pointer fixes (pre-split `evaluation-architecture` reference → `design-eval-rubric`/`design-eval-pipeline`; dead notebook ID `cdb5e862-…` → `91568710-98b3-4448-b038-04f9b48b7111`) | Peter Delta §4 (V-1 verdict; NOT_FOUND found on live query) | One commit, founder executes with A-5 deletion |
| **S-8** | **Brent pending Skill 5 (Cloud IAP / OAuth wiring) — update before issue #73 work begins**: direct IAP-on-Cloud-Run is GA (no load balancer, no added cost, different audience handling) — changes the wiring model his JD template assumed; removes the load-balancer cost objection if IAP-plus-federated-identity is ever evaluated (does not invalidate ADR-022's multi-IdP reasoning) | Brent Delta §2 R3 finding 2 + §5 | Fold into the pending-skill authoring (S-3 set); template conditionality already applied via Patch 4 amendment |
| **S-9** | **Marketing skill annexes — conditional, corroboration-gated**: `marketing-product-led-seo` AI-citation-visibility annex (+ Big 5 note); `linkedin-social-selling` saves/dwell metric update (10:1 LCS rule may undervalue saves/dwell under "360Brew" single-model ranking) | John Delta §2 R3 + §4.3 — John flagged both findings as **directional secondary sources** and correctly refused to patch skills on them | Linda sources one primary reference each (LinkedIn engineering's 360Brew publication; a primary Google AI Overviews/AI Mode source) — A-26; then John drafts annexes; founder approves |
| **S-10** | **`notebooklm-cli`**: upgrade `notebooklm-mcp-cli` 0.7.0 → 0.7.2 (two patch releases in window) and re-verify the skill's command table against the new binary | Linda Delta §4.1 (PyPI evidence; no syntax change identified yet) | Linda re-verifies; founder applies any skill-file edit (A-22) |
| **S-11** | **Standards-monitoring procedure (Linda)**: fold in four standards-currency mechanics, citable to the `engineering-standards` notebook's own "Keeping Standards up-to-date" sources — amendment-level tracking (not just new editions), withdrawal flagging, referenced-overseas-standards tracking, standards-body update-service subscription. Includes the tooling question: extend feeds beyond `snz_scraper.py` (ISO/BSI/Standards AU have no permanent tool) or narrow Outcome 4 wording to what is operational | Linda Delta §3.2 + §4.2 (R2-grounded; all domain decisions stay routed to Graeme) | Bundled with the founder's A-18 decision; Harriet drafts the Linda JD patch only if the founder chooses to narrow Outcome 4 |

## 8. Proposed AGENTS.md Text (founder applies — resolves O-2 / F-1 / F-2)

Under **Engineering (execution)**:

```markdown
- **Brent** (`brent.md`): DevOps Engineer (GCP) -- cloud infrastructure (Terraform), Cloud Run deployment, CI/CD, IAM, SOC 2 technical controls. "Brent, [request]"
```

Add to the **Approved dispatch routes** table:

```markdown
| **Brent** | Peter | Tier-1 GCP service approval (blocking); connection-strategy ADR input |
| **Linda** | Brent | Cloud/DevOps/SOC-2 source-currency triage (structured review template) |
```

Header fix: "Four named personas" → "Six named personas"; add Matt to the epistemic-honesty clause's agent list.

## 9. New Hire Triggers

**None.** The only new orphan with execution weight (Terraform authoring, O-1) sits squarely inside Brent's DevOps domain and is absorbed by his patch — it does not justify a role. No responsibility named in `strategic-bets.md` is unowned after the proposed patches.

## 10. Draft JD Patches Produced — UPDATED post-A-8

| Patch | Path | Status |
|---|---|---|
| Brent | `docs/people/drafts/agents/brent.agent.md` | **VALIDATED by Brent 2026-06-10** (Delta §4 — all six patches confirmed); his two wording amendments applied (Patch 1 "current" → "maintained"; Patch 4 Infra-Ready template IAP fields conditional + stale audience-format note). **Ready for founder promotion (A-1)** |
| Harriet | `docs/people/drafts/agents/harriet.agent.md` | Single-row routing fix (`sync-agent-topology` → `hr-sync-agent-topology`); founder promotes (A-2) — unchanged |
| **John** | `docs/people/drafts/agents/john.agent.md` | **NEW** — drafted from John's Delta (self-reported): Patch 1 persona-path correction (gate was unsatisfiable — nonexistent directory); Patch 2 pre-launch signal-report mode (sections 1–2 conditional on live instrumentation; 3–6 always due). Founder promotes (A-20) |
| **Matt** | `docs/people/drafts/agents/matt.agent.md` | **NEW** — drafted from Matt's Delta (self-proposed, notebook + currency grounded): Patch 1 Knowledge Base → SSOT pointer (ADR-001; JD claimed 7 books, notebook holds 4); Patch 2 WCAG 2.2 AA accessibility baseline (Do #8 + Self-Review Step 2c); Patch 3 canonical Playwright MCP tool names; Patch 4 Self-Review Step 2b (worst-case data) + Step 6 (partner-feedback reconcile). Founder promotes (A-21) |

**Not drafted — correctly, per "agents who declared no JD change get none":**

- **Ron, Graeme, Peter, Linda** — each declared no JD change required at live reflection; their follow-ups are artifact-, skill-, or decision-level (consolidated in §12), not JD patches.
- **Mark's conditional `/standup` one-liner** — pends his sharpening question to the founder (A-15); Mark's own verdict is "status quo stands; do not add a row."
- **Linda's Outcome 4 wording** — pends the founder's extend-tooling-vs-narrow-wording decision (A-18); drafting before that decision would presume its outcome.
- **Kabilan** — no statement (standing no-dispatch rule); no repo-evidenced drift.

## 11. People Artifact Updates (this session, direct write)

| Artifact | Change |
|---|---|
| `docs/people/agent-register.md` | Harriet skills row → `hr-*` family + `notebooklm-cli`; Peter skills row → post-split names (`create-adr`, `adr-constitution-sync`, `design-eval-*`, `define-ai-policy`, `enforce-ai-batch-discipline`); `notebooklm-mcp` → `notebooklm-cli` (Graeme, Matt, Linda); Mark + `agile-sprint-planning`; Brent paths → `deploy/infra/`, `deploy/docker/` + 13-pending note; date + lint fix |
| `docs/people/org-chart.md` | **Harriet maturity contradiction fixed → Draft-first** (06-07 Autonomous grant reverted same day); Brent write-paths updated; sync note appended; date + lint fixes |
| `docs/people/skills-taxonomy.md` | Phantom `ceremony-agent-topology-sync` → `hr-sync-agent-topology`; People & Org → `hr-*` family; `version-control` → `git-version-control`; architecture section reworked to post-split names incl. `arch-engineering` duplicate flag; added `python-fastapi`, `mcp-cce`, `session-handover`, `github-projects`, superseded stubs, `mental-models`; new "Quality Gates & Static Analysis" and "SpecKit Workflow (Layer 0)" sections; gap table updated (terraform-iac, SRP row, dedup row, tool-selection cleanup confirmed) |

**Post-A-8 second pass (same day, from Delta evidence):** agent-register — Brent patch note → "validated, pending promotion"; stale skill name `marketing-social-selling-linkedin` → `linkedin-social-selling` (on-disk folder verified; surfaced by John's Delta). org-chart — sync note updated (A-8 closed; John/Matt patches drafted). skills-taxonomy — `arch-engineering` row → Peter-confirmed deprecation with salvage; `engineering-architecture` gap row gains salvage/stale-pointer detail; `ux-design-critique` row notes pending patch additions; gap table gains S-5, S-6, S-9, S-10, S-11 rows and the Skill-5/IAP note on the GCP/DevOps row; John skill-name fix mirrored.

## 12. Pending Founder Approvals / Next Actions — CONSOLIDATED post-A-8

Every item the eight Delta Statements route to the founder or to another agent is consolidated here. A-1–A-10 keep their original numbers; A-11+ are new from the live collection.

### Founder decisions and approvals

| # | Item | Owner | Source |
|---|---|---|---|
| A-1 | Approve + promote Brent JD patch — **Brent validation COMPLETE 2026-06-10; amendments applied; promotion unblocked** | Founder | Brent Delta §4 |
| A-2 | Approve + promote Harriet routing-row patch | Founder | Morning run |
| A-3 | Apply AGENTS.md text (§8) — resolves O-2/F-1/F-2 | Founder | Morning run; Matt Delta acknowledges F-2 |
| A-4 | Approve SRP skip-list edit (2 additions + 1 rename) in `srp-scan-procedure.md` | Founder | §6 |
| A-5 | Approve deletion of `.agents/skills/arch-engineering/` — **Peter confirms**, now with salvage condition + 2 stale-pointer fixes in `engineering-architecture`, one commit (V-1/S-7) | Founder executes; Peter supplied the verdict | Peter Delta §4 |
| A-6 | **REWRITTEN by Peter's verdict (supersedes "amend/annotate"):** green-light **ADR-023** — "Accepted, partially supersedes ADR-022 (scope statements only — the hosting decision stands)"; staging+prod as separate Cloud Run services, separate Secret Manager secrets (`{env}-redline-{credential}`), shared `locals` block, min-instances prod ≥ 1 / staging 0, max-instance caps, startup-probe parameters, `deletion_protection = false` rationale; ADR-022 status-line update in the same commit; written `create-adr`-compliant | Founder green-lights; **Peter authors**; his constitution-sync check runs on acceptance | Peter Delta §3; Brent Delta §4 (seconds) |
| A-7 | Add `agile-*` entries to `skills-lock.json` (O-4) | Founder / engineering | Morning run |
| A-8 | **CLOSED 2026-06-10.** All eight reflecting agents dispatched from the founder's main-thread session; verbatim Delta Statements at `docs/people/drafts/reports/delta-statements-2026-06-10/` (R1/R3 complete ×8; R2 live ×4, blocked ×4 — see F-5). Kabilan: no-dispatch per standing rule | — | `_index.md` |
| A-9 | Commit this sync's working-tree changes — scope now includes the Delta Statements folder, the amended Brent draft, new John/Matt drafts, the updated report, and the second-pass People artifacts. Harriet does not commit unprompted | Founder | Morning run + this pass |
| A-10 | `terraform-iac` skill authoring (S-1) — schedule next sprint with the 12 carried GCP/DevOps skills; scope now includes Brent's validated additions (state surgery, pinning maintenance, 6.x→7.x upgrade-evaluation checklist) | Founder schedules; Harriet drafts via `writing-skills` | Brent Delta §5 |
| A-11 | **Confirm publication status of `craig-lewis-email.md`** (and the other six artifacts in `docs/product/marketing/content/`) vs the empty AI-content-review log. If sent unreviewed → gate breach to record; if drafts → no breach. Either way John operationalises review-log discipline before the launch wave | Founder confirms; John acts | John Delta §3.3 |
| A-12 | Approve John's **reduced-scope June signal report retro-file** (sections 3–6 this week; sections 1–2 marked "pre-launch — no instrumentation") + July report due 2026-07-01 under the amended rule (John patch, Patch 2) | Founder approves; John files | John Delta §4.2 |
| A-13 | **Bet 1 kill-criterion anchor decision**: the bet header anchors kill timelines to 2026-06-01, but Bet 1's criterion reads "90 days *from launch* (2026-09-01)" — if launch slips past June, the fixed date and the launch anchor diverge. Decide which governs | Founder + Ron at next bet review, **Peter present** (B-1b SSO dependency gates the signup counter) | Ron Delta §3 |
| A-14 | **Duplicate `specs/005-*` numbering** (`005-docker-deploy-setup` + `005-gcp-project-baseline`, both on master — verified): renumber or formally accept (F-4) | Peter + founder | Mark Delta §3 |
| A-15 | **Answer Mark's sharpening question:** has the founder ever conversationally asked Mark to run a standup? **Yes** → one-line Crisp Boundaries addition ("I do not run the daily standup — that is the founder-invoked `/standup` command"; Harriet drafts). **No** → change nothing. Mark's verdict either way: no routing row | Founder answers | Mark Delta §3 |
| A-16 | **Authorise Matt's notebook sourcing request to Linda** (Matt holds no Linda dispatch): add Laws of UX **2nd ed. (2024)**, Refactoring UI, About Face, Practical Typography (URL source); then the five remaining promised titles (Strategic Writing for UX, Writing Is Designing, Articulating Design Decisions, Continuous Discovery Habits, Design That Scales); correct register metadata for Designing with Data (King, Churchill & Tan, O'Reilly, **2017** — not "Suda 2010") | Founder authorises; Linda executes (register is her direct-write authority) | Matt Delta §4.1 |
| A-17 | **`technical-communication` notebook currency review** — sources 2000–2014 by the notebook's own admission. Linda routes candidate-source decisions to consumers (Graeme, Mark, Matt) + founder for the domain call; Linda makes no domain judgment | Founder + consumers decide; Linda executes | Linda Delta §3.3, §4.4 |
| A-18 | **Linda Outcome 4 decision**: extend standards-feed tooling beyond `snz_scraper.py` (ISO/BSI/Standards AU have no permanent tool) **or** narrow Outcome 4 wording to what is operational. Bundle: S-11 procedure mechanics (notebook-citable). If narrowed → Harriet drafts the Linda JD patch | Founder decides | Linda Delta §3.2, §4.2 |
| A-19 | **Unblock the design critical path**: Peter delivers the Touch 1 constraints memo for the Skeleton Generator (`specs/shaped/` empty); Mark confirms PRD readiness. Ship target 2026-06-30 is 20 days out (F-6) | **Peter** (memo) + **Mark** (PRD confirmation); founder sequences | Matt Delta §1 |
| A-20 | Approve + promote **John JD patch** (persona path + pre-launch signal-report mode) | Founder | John Delta §3.1, §4.1 |
| A-21 | Approve + promote **Matt JD patch** (4 items: notebook SSOT, WCAG 2.2 AA, Playwright tool names, Self-Review additions) | Founder | Matt Delta §4.2–4.5 |
| A-22 | Approve `notebooklm-mcp-cli` upgrade 0.7.0 → 0.7.2; Linda re-verifies the `notebooklm-cli` skill command table against the new binary (S-10) | Founder approves; Linda verifies | Linda Delta §4.1 |
| A-23 | Approve the **`hr-sync-agent-topology` protocol amendment** (S-5: R2-null acknowledgment + dispatched-session access prerequisites) and decide the tooling question — whether dispatched reflection sessions get a guaranteed NotebookLM/CCE access path (F-5) | Founder approves; Harriet supplies text | Linda Delta §3.4; Mark Delta §3; `_index.md` |
| A-24 | Approve the **`create-adr` edit** (reciprocal status convention + partial-supersession pattern, S-6) — Peter supplies content; ADR-023 exercises it | Founder approves; Peter authors | Peter Delta §5.1 |
| A-25 | **Persona canonical-location decision (V-2)**: materialise `docs/product/personas/` (Mark's declared co-owned write authority) and move the artifact, or keep `docs/product/strategy/personas.md` (Ron's domain) and patch Mark's JD path. John's patched gate follows the artifact either way | Founder + Ron + Mark | John Delta §3.1; facilitator verification of Mark's JD |
| A-26 | **Marketing corroboration sourcing (S-9)**: Linda sources one primary reference each — LinkedIn engineering's 360Brew publication; a primary Google AI Overviews/AI Mode source. Then John drafts the two skill annexes for founder approval | Founder authorises; Linda sources; John drafts | John Delta §4.3 |

### Agent-owned next actions (no founder approval required; listed for the record)

| Agent | Action | Source |
|---|---|---|
| Peter | Author ADR-023 once A-6 is green-lit (constitution-sync on acceptance); add the Touch-2 checklist line ("does the spec treat any ADR Out-of-Scope item as in-scope? If yes, ADR action precedes merge"); write the one-page platform synthesis of the ADR-019→022 cluster in `docs/architecture/` (satisfies his weekly-artifact constraint); enforcement hook for spec-vs-ADR divergence explicitly **deferred** (long-runway only) | Peter Delta §3, §5 |
| Ron | Bet 7 evidence refresh (DORA "ROI of AI-Assisted Software Development" 2026.01 — independently corroborated by Peter's R3) + Bet 6 Beca/BEYON dated annotation — next strategy session, after notebook access; "Faultless" claim remains unverified (not contradicted) — keep watching | Ron Delta §4; Peter Delta §2 |
| Graeme | EC7 second-generation transition document: write on first domain question or defer via `task-defer` to the first-generation withdrawal milestone (2028-03); verify whether the 06-09 ENZ/NZGS document already covers CPEng/PEngGeol sign-off + consenting-authority reviewer qualifications, else extend `report-writing/audit-trail-sign-off-workflows.md` (feeds Peter's rubric) | Graeme Delta §4 |
| Linda | Add the NZGS/MBIE-modules-vs-NSHM-review watch item to standards monitoring (no revision found as of 2026-06-10; Module 1 hazard values interim) | Graeme Delta §4.3 |
| John | Retro-file June signal report on A-12 approval; no acquisition copy implying SSO/verified-email capability until issue #73 closes (Peter's proactive ADR channel covers this — worked as designed this window) | John Delta §4.2, §4.4 |
| Mark | Torres AI-era discovery enrichment for the `software-dev-methodology-eng-org` notebook — **deferred, evidence-gated**; revisit trigger: KR2 interview prep or LLM-output-quality hypothesis work; route to Peter (notebook owner) via Linda when triggered | Mark Delta §4 |
| Harriet | Draft S-5 amendment text for A-23; draft Linda JD patch only if A-18 narrows; `terraform-iac` drafting at A-10 schedule | This report |

## 13. Next Sync Eligibility

| Trigger | Earliest date |
|---|---|
| Quarterly cadence | **2026-09-08** (90 days from this sync — new baseline per promotion checklist) |
| New hire onboarded | On any future hire |
| Major product milestone | On Skeleton Generator ship (target 2026-06-30) |
| Strategy pivot / client feedback batch | On occurrence |

**Note:** A-8 (live Delta collection) completed this sync's deferred reflections on 2026-06-10 — **closed**. The condition it imposed on A-1 (Brent validation before promotion) is satisfied; A-1, A-20, and A-21 now await only founder approval. This sync is complete: trigger validated, all reflections collected (Kabilan excepted by standing rule), gap/overlap/SRP passes done, patches drafted, artifacts updated. The 2026-09-08 quarterly baseline stands.
