# Audit — `agile-sprint-planning` skill + `/sprint-planning` command wrapper

**Auditor:** Harriet (Head of People & Agent Development)
**Date:** 2026-06-11 · **Branch:** `feature/sprint-planning` · **State audited:** working tree (uncommitted growth: +365/−25 lines on SKILL.md, +22/−3 on the wrapper, vs HEAD `1775c80`)
**Subject:** `.agents/skills/agile-sprint-planning/SKILL.md` (672 lines, 33.4 KB) and `.claude/commands/sprint-planning.md` (52 lines)
**Method:** `hr-audit-agent` (audit mode) + `writing-skills` (CSO/token rules) + ADR-001/ADR-009 compliance pass + mental-models protocol on the decomposition decision. NotebookLM grounding via `nlm` against the `software-dev-methodology-eng-org` notebook (register ID `91568710-98b3-4448-b038-04f9b48b7111`; Harriet is a listed consumer).

**Harness note (epistemic honesty):** this session ran as a one-shot subagent — CCE MCP tools and subagent dispatch were unavailable. Discovery was done by direct file reads. RED-phase scenarios in `scenarios.md` are specified but **not yet executed**; where production evidence already exists (Sprint 2 board failure) it is cited as the RED observation per the founder's directive.

---

## 1a. Taxonomy placement

| Dimension | Current value | Verdict |
|---|---|---|
| Domain category (`docs/people/skills-taxonomy.md`) | **Ceremonies** (Mark steward, Peter consulted) | **Correct.** Start-of-sprint ritual; siblings `agile-daily-standup`, `hr-sync-agent-topology`, `ceremony-monthly-editorial-session`. |
| ADR-009 tier (`skills-lock.json`) | **planning** | **Correct.** Coordination logic, conditional branching (two modes, founder gates), cross-agent consultation (Mark leads; Ron/Peter/Graeme one-hop). Matches ADR-009's $S_{plan}$ definition. The defect is not the tier — it is that the file *also* inlines Functional/Atomic-tier content owned at L1/L2/L6 (see §1b). |
| Layer (`skills-lock.json` `layer: 9`) | **9** | **Correct.** References `github-projects` (L6), `mermaid-diagrams` (L2), `shaping` (L8), `mental-models` (L1), `pm-hypothesis-builder` / `strategy-pre-mortem` (L9, horizontal — allowed per skills-architecture Principle 7). Placement Rule yields L9. No upward references. |
| `owner_agent` | `["mark"]` | **Correct.** Peter is *consulted*, not owner — consultation does not confer ownership under ADR-009. |
| `status` | `active` | Correct. |

### Registry deltas required

| # | Registry | Delta | Status |
|---|---|---|---|
| R1 | `skills-lock.json` | **None for this skill.** My 2026-06-10 taxonomy-currency flag ("`agile-sprint-planning` and `agile-daily-standup` missing from skills-lock.json") is now **resolved on the engineering side**: both entries exist in the working-tree lock file (tier `planning`, owner `["mark"]`, `active`, layer 9) and match the taxonomy steward mapping. | Verified resolved 2026-06-11 |
| R2 | `docs/people/skills-taxonomy.md` | **Close the gap-table row** ("lock-file entry pending engineering" → Resolved 2026-06-11, entries verified). Patch drafted: `drafts/registry/skills-taxonomy-patch.md`. Also update the Ceremonies row's Purpose text after the refactor (current text mirrors the old CSO-violating description). | Patch drafted |
| R3 | `docs/architecture/skills-architecture.md` | **Layer 9 listing and the Layer Map ASCII omit both ceremony skills.** Add `agile-sprint-planning` and `agile-daily-standup` to the L9 Organisation group (proposed sub-group "Ceremonies"). Patch drafted: `drafts/registry/skills-architecture-patch.md`. | Patch drafted |
| R4 | `AGENTS.md` | **No change required.** The `check-skills-documented` hook runs with `--prefix=redline-` (prek.toml line 205), so non-`redline-*` folders carry no AGENTS.md documentation gate. Discoverability flows through Mark's JD routing table (verified: mark.md routes the ceremony) and the `/sprint-planning` command. Recommend no AGENTS.md edit. | No action |

### Adjacent registry defects observed in passing (outside this skill's scope — flag only)

1. **ADR-001 layer-SSOT pointer mismatch:** ADR-001 names `docs/architecture/skills-taxonomy.md` as the layer SSOT; the file on disk is `docs/architecture/skills-architecture.md` (which self-declares SOT and is what `hooks/sync-layer-to-lock.py` reportedly derives from). One of the two names is stale. Peter owns ADR-001 — route to him.
2. **skills-architecture.md staleness:** L9 listing and the Agent–Skill Topology diagram still say `sync-agent-topology` (renamed `hr-sync-agent-topology`).
3. **Lock-file drift beyond this skill:** lock still carries pre-split/renamed names (`hiring-agent-management`, `evaluation-architecture`, `ai-acceptable-use-policy`, `marketing-social-selling-linkedin`) and lacks `hr-*` family, `mental-models`, `tool-selection`, `session-handover`, `linkedin-social-selling`, sonarqube skills. Engineering-controlled; belongs to the broader lock reconciliation, not this refactor.
4. **`skills-create` is a phantom:** listed in the taxonomy (live) and lock (L8, harriet+kabilan) but **no folder exists on disk**. My own JD routing table names it. Needs its own resolution (create or delist).
5. **`check-skills-documented.py` docstring promises two checks; only check 1 is implemented** (external-skills check absent from code). Engineering note.
6. **Sibling skill stale pointer:** `agile-daily-standup` Step 3 says "Sprint dates from `cadences.md` → Sprint Conventions → current sprint entry" — cadences.md has no per-sprint date table. Same family of defect as wrapper V9d below; fix when daily-standup is next touched.

---

## 1b. ADR-001 SSOT violations

ADR-001: "duplication of an authoritative artifact — by copy-paste, static snapshot, or parallel definition — is a defect." Each violation below names the owning source and exactly one remedy.

### Founder's overlap hypotheses — verdicts first

| Hypothesis | Verdict |
|---|---|
| `github-projects` | **Holds — worst violation.** Restated *and drifted against* (V1). |
| `pm-hypothesis-builder` | **Holds.** Near-verbatim restatement (V3). |
| `mental-models` | **Holds** for pre-mortem + inversion definitions (V2). The "Stop Rule" section is a *false* pointer to mental-models — it is actually pm-hypothesis-builder's failure threshold under a colliding name (V8). |
| `mermaid-diagrams` | **Holds, minor.** Version ceiling + diagram-type guidance restated (V4). |
| `shaping` | **Holds, minor.** Rationale prose duplicated; the skill already cross-references `shaping` correctly elsewhere (V5). |
| `strategy-pre-mortem` | **Does not hold as a violation.** No restatement of its four-step procedure or risk taxonomy; both skills share ancestry in the mental-models registry. Remedy folds into V2 (V6). |
| `task-defer` | **Does not hold.** Zero restatement; the real finding is a *missing* optional cross-reference — and auto-deferral would violate task-defer's own "do not apply proactively" rule (V7). |
| Wrapper restating preflight + step sequence | **Holds — with drift in both directions** (V9). |

### Violations register

**V1 — Board mechanics restated and drifted. Owner: `github-projects` (L6).**

- Steps 1, 2, 8b, 11c inline `list_tasks` / `update_task` / `TaskUpdate` Python snippets — restating github-projects procedures 2 and 4.
- **Drift defect 1 (contradiction):** Steps 8b and 11c instruct writing the `depends_on` **text field** via `TaskUpdate(depends_on=frozenset(...))`. github-projects procedure 6 deprecates the legacy `Depends on`/`Blocked by` text fields ("leave them blank") in favour of **native issue dependencies**, and its Common Mistakes table explicitly forbids exactly what 8b instructs ("Recording dependencies in the `Depends on` text field → No Blocked badge, no `is:blocked` filter"). The copy has drifted from its source — the failure mode ADR-001 predicts.
- **Drift defect 2 (invented value):** Step 11b instructs "exactly one type label … `feature`, `ops`, `design`, or `content`". github-projects defines exactly **three** canonical labels (`ops`, `feature`, `design`). `content` does not exist on the repo.
- **Drift defect 3 (under-specification):** Step 11b's sub-issue mechanics ("`gh issue create` then `gh api` to set parent, or via the GitHub UI") restate procedure 7 (`set-parent`) while omitting the internal-DB-id / `-F` typed-integer gotcha — following the sprint-planning text instead of the SSOT produces a predictable `422`.
- **Doctrine conflict:** Steps 11a/11b mandate "the board must mirror the WBS exactly — every level-2 WBS row becomes a sub-issue". github-projects' Structuring Doctrine says the **default is one issue**, sub-issues must earn their keep (P1–P5 vs K1–K4), and the Redline filter breaks ties toward flat. Two stewarded rules now contradict. (Context: the WBS-mirror rule was added in reaction to the Sprint 2 failure — see Open Question Q1.)
- **Remedy: replace-with-reference.** The ceremony keeps only its *outcome gates* (counts equal, sprint field set on every committed item, dependencies recorded on the board, sub-issues per doctrine) and defers all call mechanics to github-projects procedures 1, 2, 4, 6, 7, 10 by name.

**V2 — Pre-mortem and inversion definitions restated. Owner: `mental-models` (L1 registry).**
The Lead procedure defines both concepts inline ("treat sprint failure as fact…", "ask 'how would I guarantee this sprint fails?'"). skills-architecture Principle 4: registries define concepts once; never redefine inline. `strategic_decisions/pre-mortem.md` and `general_thinking/inversion.md` exist and carry the definitions with sources (*Super Thinking*; *The Great Mental Models* vol. 1).
**Remedy: replace-with-reference**, keeping only the ceremony-specific application rules (agent self-generates from interview context; founder confirms/adjusts failure modes; the inversion list is internal-only and never shown).

**V3 — Hypothesis template and falsifiability rules restated. Owner: `pm-hypothesis-builder` (L9, horizontal).**
Lead Layers 2–3 restate, near-verbatim: the hypothesis template sentence ("We believe [segment] experiences [problem]…"); the three non-negotiables (named metric, specific threshold, time boundary); the success-AND-failure-threshold rule; and the red-flag language list ("users will like", "it will be better", "should improve") — the last is word-for-word from pm-hypothesis-builder's Behaviour Rules.
**Remedy: replace-with-reference** (`REQUIRED SUB-SKILL: pm-hypothesis-builder`). Keep only the sprint adaptation: the goal is a falsifiable sprint hypothesis; the failure clause is recorded verbatim in the plan as the tripwire (see V8).

**V4 — Mermaid constraints restated. Owner: `mermaid-diagrams` (L2).**
"flowchart LR", "Mermaid <= 8.8.0" in Step 8a and the Output Format. The taxonomy assigns diagram-type selection and the v8.8.0 ceiling to mermaid-diagrams.
**Remedy: replace-with-reference** ("dependency diagram per `mermaid-diagrams` (flowchart LR) only if real dependencies exist").

**V5 — Shaping rationale restated. Owner: `shaping` (L8).**
The "Feasibility before planning (Inspired by Marty Cagan)" paragraph duplicates shaping's purpose statement; the INVEST-Estimable fail signal and the risk table both already route unshaped tasks to `shaping`.
**Remedy: delete the paragraph; keep the single fail-signal route** ("no spec, no Pitch → push to `shaping`, do not commit").

**V6 — `strategy-pre-mortem`: no violation.** The ceremony implements a lightweight in-session variant against the same L1 registry source; it does not copy the four-step procedure, the three risk categories, or the output structure. Disposition: V2's mental-models references suffice; optionally note strategy-pre-mortem as the full-strength tool for bet-level plans (one line).

**V7 — `task-defer`: no violation; missing optional integration.** Out-of-scope rows say "Deferred to Sprint N+1 / Backlog" but nothing registers in `docs/deferred/`. task-defer itself forbids proactive application ("an explicit instruction to defer is required"), so the ceremony must NOT auto-register. **Remedy: one optional line** — if the founder explicitly says "defer X", apply `task-defer`; otherwise the out-of-scope table is sufficient.

**V8 — Intra-skill duplication** (content stated more than once inside the skill):

| Item | Occurrences | Keep |
|---|---|---|
| INVEST criteria | 3× — "Why Sprint Planning Matters" bullets; "INVEST — Task Readiness Reference" table; Step 4 mini-table | One table, once (grounded: *Clean Agile*; see §Grounding). Step 4 points to it. |
| Yesterday's weather | 2× — Why-matters prose; Step 1 | Once, in capacity step (grounded: *Clean Agile*). |
| Out-of-scope rationale | 2× — Why-matters item 2; Step 7 | Once, in the out-of-scope step (grounded: *Shape Up* scope hammering / *Clean Agile* immutable iteration). |
| Founder-confirmation gate | 3 phrasings — Step 5, Step 11c, Kickoff Checklist | One Hard Gates block; checklist references it. |
| Board-completeness gate | 3× — 11b success criterion, 11c gate, Kickoff blocking items | One blocking gate, stated once. |
| Failure threshold / "Stop Rule" | 2× — Layer 3 template failure clause; separate "Stop Rule" section. Also a **name collision**: mental-models `stop-rule.md` is a different concept (search/retry budgets), so the section title is a false pointer. | One: the Layer-3 failure clause, recorded verbatim in the plan as the **failure tripwire** (renamed). |
| Task-table format | 2 competing formats — Output Format "Committed Tasks" table vs "WBS Table Format". Production evidence: `docs/product/tasks/sprint-3-goal.md` uses the WBS format; the Output Format table went unused. | WBS table; fold Done-when/Risk columns into it. |
| "Why Sprint Planning Matters" essay | Educational prose duplicating the three items above | Delete; one Overview sentence + grounded one-liners at point of use. |

**V9 — Command wrapper restates the skill, with drift in both directions. Owner: the skill itself.**

- (a) The wrapper's "Sequence" section restates both modes' step lists — already wrong: it says "Run Steps 1–9 … wait … then Steps 10–12" while the skill places the goal-confirmation gate at Step 5 and blocking gates inside Step 11; it also omits the WBS reconciliation entirely.
- (b) The wrapper's preflight restates skill prerequisites G1–G3 with drift: wrapper says "strategic-bets.md must exist"; skill G3 requires "exists **and has at least one active bet**".
- (c) The wrapper's "Critical rule" restates the skill's confirmation gates (third phrasing).
- (d) The wrapper's "Sprint numbering" section is **unique content living only in the wrapper** — and is half-wrong: it says to detect the sprint from `cadences.md`, which contains no sprint table (only the boundary convention). The reliable source is the Sprint options in `project_config.json` / the live board.
- **Remedy:** move a corrected sprint-numbering rule INTO the skill's prerequisites; reduce the wrapper to a pure pointer (load skill, follow it). Drafted.

**V10 — Phantom skill pointer.** "Does Not Cover … use `session-retro`" — no such skill exists; `/session-retro` is a command (`.claude/commands/session-retro.md`). **Remedy: point to the command.** (Same phantom exists in agile-daily-standup — adjacent note 6.)

**V11 — Agent Assignment overlay declares a manual-sync duty.** "If the layer-responsibilities file is updated, this mapping must be updated to match" — that is ADR-001's rejected Option A (tolerated duplication with manual synchronisation). The layer→agent mapping exists nowhere else (layer-responsibilities.md records code/content ownership, not sprint-spec ownership), so the table is *not* duplication today — but its sync clause institutionalises future drift. **Remedy:** keep the mapping (sole home) in the Lead procedure with a REQUIRED reference to `docs/architecture/layer-responsibilities.md` for layer definitions; delete the sync clause; propose to Peter relocating the agent column into layer-responsibilities.md itself (Open Question Q2).

### Token / CSO violations (writing-skills bar)

- **672 lines ≈ 5,100 words** against the writing-skills guidance of <500 words for a standard skill (planning-tier skills justifiably run longer, but not 10×). The drafted refactor (measured): entry SKILL.md 908 words + three procedure files (325/817/572) + one reference file (481) = **3,103 words ≈ 58% of current volume (a 42% cut)** with zero behavioural loss — and the per-session load drops further because procedures load on demand (a Suggest session loads ~1,700 of the 3,103).
- **Frontmatter description summarizes workflow** ("…set a sprint goal, select tasks…, sequence them by risk, … Reads the GitHub Projects board… Writes sprint goal to docs/product/tasks/ and assigns sprint field…"). writing-skills CSO: a workflow-summarizing description becomes a shortcut Claude follows *instead of reading the skill* — the exact mechanism behind skipped write-back steps. Rewritten to triggering conditions only.
- `@`-style force-load links: none found (good). Cross-references lack REQUIRED markers — added in drafts.

---

## 1c. SRP analysis

### Responsibilities currently bundled (18)

R1 mode routing · R2 agile education essay · R3 capacity (yesterday's weather) · R4 backlog read + bet/OKR alignment screen · R5 INVEST readiness gating · R6 Suggest-mode goal drafting · R7 Lead-mode 3-layer interview · R8 pre-mortem/inversion application · R9 failure tripwire · R10 backlog reconciliation (3 buckets, Torres duplicate test) · R11 agent assignment (layer→agent overlay) · R12 WBS construction + format · R13 sequencing + dependency mapping · R14 out-of-scope naming · R15 board materialization (issues, sub-issues, sprint field, dependencies, count gate) · R16 plan-document writing · R17 this-week regeneration · R18 (external) wrapper duplication.

Of these: R2 is deletable (V8); R5's definition, R8's definitions, R13's syntax, and R15's mechanics are owned elsewhere (V1–V4); R9 merges into R7 (V8). What genuinely remains is **one** responsibility at planning tier: *run the sprint-planning ceremony end-to-end* — with two elicitation front-ends (R6 | R7+R8+R10+R11+R12) converging on one shared commit backbone (R3-R4-R5 feed in; R13–R17 execute).

### The decision: (i) thin orchestrator + composable sub-skills vs (ii) single skill with extracted shared references

**Mental-models protocol applied** (models selected from `.agents/skills/mental-models/` by trigger match):

1. **`deep-modules` (general_thinking)** — trigger: "deciding how to split or consolidate a module". A skill's interface = its frontmatter description + entry contract; its implementation = procedure content. The ceremony must present ONE narrow interface (invoke → full ceremony → board + plan doc) hiding substantial internal complexity. Option (i) mints sub-skills whose only consumer is this ceremony — textbook *classitis*: shallow modules, interface cost (new descriptions, new registry rows, new dispatch surface) ≈ implementation moved, abstraction benefit ≈ zero. Option (ii) keeps the module deep: progressive disclosure via skill-internal procedure files costs no new interface.
2. **`inversion` (general_thinking)** — "how would I guarantee this refactor fails?" (a) Give extracted parts their own `Use when…` descriptions → the dispatcher matches a fragment directly → ceremony preflight and founder gates get bypassed → board writes without confirmation. (b) Token-diet away the Common Mistakes table → Sprint 2 failure mode recurs unguarded. (c) Leave any board call mechanics inline → they re-drift from github-projects. (d) Keep the wrapper's step summary → wrapper drifts again. Therefore: one dispatchable entry point only; sub-files carry NO frontmatter; Common Mistakes preserved verbatim where they encode production evidence; zero inline board mechanics; pointer-only wrapper.
3. **`second-order-thinking` (general_thinking)** — first-order effect of (i): smaller files. Second-order: every new registered skill = a lock entry + taxonomy row + layer assignment + an audit surface at every future Topology Sync, forever — at solo-founder scale this is pure governance drag. And the content the sub-skills would hold *already has owners* (github-projects, pm-hypothesis-builder, mermaid-diagrams, mental-models): creating new homes for owned content is negative-value. Deletion-by-reference beats extraction-to-new-skill wherever an owner exists.

**Recommendation — exactly one: Option (ii). Single registered skill, thin SKILL.md router, mode procedures and plan template as skill-internal files, all owned content replaced by references.**

Justification against ADR-009 tiers: planning-tier skills are *defined* as carriers of coordination logic, step dependencies, and conditional branching — the ceremony's residual responsibility is exactly that and nothing else once tier-inappropriate content (Functional L6 board mechanics, Atomic L2 diagram syntax, L1 registry definitions, L9 sibling templates) is returned to its owners. Option (i) would mint single-consumer Functional-tier skills that fail ADR-009's ownership-and-justification logic (a skill no other agent or workflow triggers independently) and would recreate the `prek-find-and-fix`-style SRP-flag surface I am required to police at every sync. The existing **justified-orchestrator** precedent (`sonarqube-find-and-fix`) sanctions precisely what remains: one ceremony skill orchestrating *pre-existing, independently useful* skills. No new skills. No lock/taxonomy/layer additions. The decomposition is internal: `SKILL.md` (contract + routing + hard gates + mistakes) → `procedures/suggest.md` | `procedures/lead.md` → `procedures/commit.md` (shared backbone) → `reference/plan-format.md`.

**End-to-end guarantee (founder's hard constraint):** the entry skill's Hard Gates section makes the commit backbone non-optional — a session that elicits a goal but does not finish `procedures/commit.md` (issues + sub-issues per doctrine, sprint field, dependencies on the board, plan doc, this-week.md) is defined as an incomplete ceremony, with the Sprint 2 evidence cited inline. Both modes terminate in the same backbone; no path exits before it.

---

## Grounding (NotebookLM, `software-dev-methodology-eng-org`, queried 2026-06-11)

| Claim in skill | Source (notebook citation) | Status |
|---|---|---|
| INVEST criteria, per-letter definitions | *Clean Agile* (Martin), Ch. 3 Business Practices — INVEST acronym, all six letters; also referenced in *Continuous Delivery* (Humble & Farley), Ch. 4 | **Grounded** |
| Yesterday's weather; capacity = last iteration's actual | *Clean Agile* — "the best predictor of today's weather is yesterday's weather"; plan next iteration at exactly the prior completed amount | **Grounded** |
| One goal per sprint; goal as measuring stick | *Sprint* (Knapp) — one important goal, sprint questions as beacon/measuring stick | **Grounded** |
| Out-of-scope discipline / scope protection | *Shape Up* (Singer) — fixed time variable scope, scope hammering ("scope grows like grass"); *Clean Agile* — requirements immutable once the iteration begins | **Grounded** (the specific "name ≥3 out-of-scope items" is a Redline convention — labelled as such in drafts) |
| Pre-mortem definition | [Pre-mortem](../../../../.agents/skills/mental-models/strategic_decisions/pre-mortem.md) (*Super Thinking*, Weinberg & McCann) | **Grounded via registry** — referenced, not restated |
| Inversion definition | [Inversion](../../../../.agents/skills/mental-models/general_thinking/inversion.md) (*The Great Mental Models* vol. 1, Parrish) | **Grounded via registry** |
| Hypothesis template, three non-negotiables, red-flag language | `pm-hypothesis-builder` skill (its own grounding) | **Grounded via owning skill** |
| **Not grounded (labelled Redline conventions in drafts):** 20–30 min ceremony duration; max-3-questions-per-turn cap; the four Layer-2 probes; "out-of-scope ≥ 3 items"; falsifiable-sprint-goal framing (an application of pm-hypothesis-builder to sprints, not a literature claim) | — | Labelled |

---

## Open questions (could not dispatch — recorded per one-shot constraint)

**Q1 — for Mark (board steward) + founder:** Steps 11a/11b's "board mirrors WBS exactly; every level-2 row becomes a sub-issue" conflicts with github-projects' Structuring Doctrine (default flat; K1–K4; Redline filter ties → flat). The WBS-mirror rule was the reaction to Sprint 2 (8/10 planned tasks never reached the board) — but the *fix* for that failure is the count gate + verification, not mandatory decomposition. Drafts resolve it as: **every level-1 WBS row must be a board item (count gate, blocking); level-2 rows become sub-issues only where the Structuring Doctrine's PROMOTE signals hold, founder confirms the structure.** Mark should ratify or overrule.

**Q2 — for Peter:** the layer→agent assignment overlay's only home is this skill, with a manual-sync clause against `layer-responsibilities.md` (ADR-001 Option-A pattern). Proposal: add an "Owning agent (spec/decision)" column to `layer-responsibilities.md` (his file) and have the ceremony reference it; until then the drafts keep the table in `procedures/lead.md` with the sync clause removed and a provenance line.

**Q3 — for Mark + engineering:** dependency write path. github-projects procedure 6 says native issue dependencies are canonical and the legacy `depends_on`/`blocked_by` text fields are deprecated — but `agile-daily-standup` (and possibly the Python tool's TaskRecord) still read the legacy fields for Diagram 2. Drafts instruct writes via `set-dependencies` (native, per the SSOT) and flag this question. If the tool reads only legacy fields, either the tool follows native links or the deprecation note is wrong — one of them must move.

**Q4 — for Peter (ADR-001 owner):** the layer-SSOT filename mismatch (adjacent finding 1).

**Q5 — for founder:** `skills-create` phantom (adjacent finding 4) — create the folder or delist from taxonomy + lock + my JD routing table.

---

## Verdict

Category, tier, layer, owner: all correct — no reclassification. The skill's defect is **SSOT violation at scale plus intra-skill duplication**, already producing real drift (legacy dependency field vs native; invented `content` label; wrapper gate drift). Remedy is Option (ii): keep one planning-tier ceremony skill, return owned content to its owners by reference, restructure internally for progressive disclosure, reduce the wrapper to a pointer. No new skills; no registry additions; two registry patches (taxonomy gap-row closure, layer-doc listing). Full target design in `design.md`; test suite in `scenarios.md`; complete drafts in `drafts/`.
