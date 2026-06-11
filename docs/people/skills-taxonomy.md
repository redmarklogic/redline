# Skills Taxonomy

**Owner:** Harriet  
**Last updated:** 2026-06-10  
**Source of truth for:** all skills in `.agents/skills/` and their domain category.

> Update this file whenever a skill is created, retired, or reassigned.
>
> **Derived column — Used by:** The "Used by" column is a human-readable derivative of the `owner_agent` arrays in `skills-lock.json` (the authoritative source per ADR-001, ADR-009). It must not be treated as canonical. When `skills-lock.json` and this column disagree, `skills-lock.json` wins.
>
> **Note:** "Engineering" in the Used by column refers to **Kabilan** (Python Developer, hired 2026-05-22; slug: `kabilan` in `skills-lock.json`). Kabilan loads these skills on demand per task type.

---

## Taxonomy

### Python — Core

| Skill | Purpose | Used by |
|---|---|---|
| `python-style` | General Python style and `uv` usage conventions | Engineering |
| `python-patterns` | Idiomatic Python patterns (control-flow, iteration, composition) | Engineering |
| `python-typing` | Type hint standards | Engineering |
| `python-linting` | Ruff/lint compliance and safe suppressions | Engineering |
| `python-paths` | File path conventions (pathlib, importlib.resources) | Engineering |
| `python-error-handling` | Exception handling, error translation, logging | Engineering |
| `python-documentation` | Docstring standards (Google Style) | Engineering |
| `python-function-design` | Function decomposition, signatures, side effects | Engineering |
| `python-class-design` | Class responsibilities, init, composition | Engineering |
| `python-domain-modeling` | Value objects, Pandera/Pydantic, DataFrame-first APIs | Engineering |
| `python-module-structure` | Step-down rule, public-before-private ordering, helper extraction | Engineering |
| `python-fastapi` | External (north-south) FastAPI HTTP endpoints conforming to the HTTP API standard (ADR-018) | Engineering |

### Python — Testing

| Skill | Purpose | Used by |
|---|---|---|
| `python-testing-unit` | Unit testing standards | Engineering |
| `python-testing-api` | FastAPI component and contract tests | Engineering |
| `test-driven-development` | RED-GREEN-REFACTOR cycle | Engineering |

### Python — Tooling & Environment

| Skill | Purpose | Used by |
|---|---|---|
| `dev-environment` | Bootstrap and maintain dev environment (uv, tasks, prek) | Engineering |
| `python-usethis` | Add/remove dev tools via usethis CLI | Engineering |
| `python-static-checks` | Running static checks (ruff, mypy) | Engineering |
| `python-deptry` | Dependency hygiene with deptry | Engineering |
| `python-performance` | Profiling and optimisation patterns | Engineering |

### Python — Scripts

| Skill | Purpose | Used by |
|---|---|---|
| `python-script` | Script conventions (stepdown rule, Spyder-style cells) | Engineering |
| `python-script-numbering` | Script naming and execution order conventions | Engineering |

### Data & Domain

| Skill | Purpose | Used by |
|---|---|---|
| `data-tidy` | Tidy data principles, DataFrame schema design | Engineering |
| `python-pins-data-version-control` | Dataset versioning with the pins library | Engineering |
| `python-data-ingestion` | Data ingestion and validation (import/process/read pattern) | Engineering |
| `python-crewai` | CrewAI agent, task, flow, and output model conventions | Engineering |

### EDA & Reporting

| Skill | Purpose | Used by |
|---|---|---|
| `eda-codebook` | Generate and update Markdown codebooks for datasets | Engineering / Data |
| `eda-interpreting-data` | Pre-flight data quality screening and insight writing | Engineering / Data |
| `eda-qa` | QA against existing codebook + raw dataset | Engineering / Data |
| `eda-visual-design` | Chart type selection, encoding, cognitive load | Engineering / Data |
| `python-plot-colors` | Color selection, colormap choice, color-blindness safety | Engineering / Data |
| `qmd-tables` | Rendering tables in Quarto documents | Engineering / Data |
| `qmd-narrative-design` | Narrative design (Hook-Problem-Insight-Proof-Action arc) | John, Engineering |
| `mermaid-diagrams` | Mermaid diagram type selection, syntax constraints (v8.8.0 ceiling), quality guidance | Mark, Ron, John, Matt, Engineering |

### Infrastructure & Security

| Skill | Purpose | Used by |
|---|---|---|
| `security` | Secure coding (secrets, configuration, logging) | Engineering |
| `git-version-control` | Commit conventions, hygiene, prek hooks, pre-push | Engineering |
| `git-push-batched` | Push changes in thematically cohesive commits | Engineering |
| `git-hooks-create` | Writing bespoke git hooks | Engineering |
| `tool-selection` | CLI-first routing across `gh`, `gws`, `gcloud`, MCP, and direct API (ADR-016) | All |
| `python-mcp-tools` | MCP tooling usage in this repo | Engineering |
| `notebooklm-cli` | Query NotebookLM notebooks via the `nlm` CLI (setup, auth, config) | Harriet, Graeme, Ron, John, Mark, Linda, Peter, Kabilan |
| `miro-mcp` | Create diagrams and visual artifacts on Miro boards | Mark, John, Ron, Peter |

### Research & Knowledge

| Skill | Purpose | Used by |
|---|---|---|
| `redline-research` | Structured research workflow querying NotebookLM knowledge bases | Graeme, Ron, Mark, John, Peter |
| `rag-prompting` | Query design for NotebookLM — prompt anatomy, retrieval rules, structured extraction | Graeme, Ron, Mark, John, Linda |
| `notebooklm-deep-research` | Run NotebookLM deep research with 5 Whys intake, selective source import, and notebook indexing | Ron, Mark, Peter, Linda |
| `library-management` | Index, rename, and add books to the digital library | Linda |
| `notebooklm-index` | Index NotebookLM notebooks into the register spreadsheet | Linda |

### Development Workflow

| Skill | Purpose | Used by |
|---|---|---|
| `brainstorming` | Socratic design refinement before implementation | Engineering |
| `spec-kit` | Specification-driven development (specs, plans, tasks) | Engineering |
| `subagent-driven-development` | Fast iteration with two-stage review | Engineering |
| `dispatching-parallel-agents` | Concurrent subagent workflows | Engineering |
| `using-git-worktrees` | Parallel development in isolated git worktrees | Engineering |
| `requesting-code-review` | Pre-review checklist | Engineering |
| `resolving-pr-issues` | Resolve incoming PR code-review comments (structured triage, fail-first test, fix, CI closure) | Engineering |
| `verification-before-completion` | Verify errors are truly resolved before claiming done | Engineering |
| `systematic-debugging` | 4-phase root cause debugging process | Engineering |
| `task-defer` | Defer a task, idea, decision, or knowledge gap to a future date or condition; register in `docs/deferred/` with a mandatory unfreeze condition | Ron, Mark, Peter, Graeme, John, Matt, Harriet, Engineering |
| `mcp-cce` | Code Context Engine (CCE) discovery: semantic codebase/docs search, session decision memory | All |
| `session-handover` | Structured session close: handover note, CCE decision writes, uncommitted-work flags | All |
| `github-projects` | Create, update, move, and query tasks on the Redline GitHub Projects board | Mark, Engineering, Founder |

### Quality Gates & Static Analysis

| Skill | Purpose | Used by |
|---|---|---|
| `sonarqube-scan` | Trigger a SonarQube static analysis scan and wait for compute-engine task success | Engineering |
| `sonarqube-review` | Retrieve, triage, and record false positives for open SonarQube issues on the current branch | Engineering |
| `sonarqube-find-and-fix` | End-to-end SonarQube quality-gate cycle (scan → triage → fix → re-scan) — SRP known-exception (`justified-orchestrator`) | Engineering |
| `prek-find-and-fix` | End-to-end prek (pre-commit) triage-and-fix cycle — **SRP new-violation 2026-06-10; skip-list addition proposed** | Engineering |
| `test-find-and-fix` | End-to-end test-suite triage-and-fix cycle — **SRP new-violation 2026-06-10; skip-list addition proposed** | Engineering |

### SpecKit Workflow (Layer 0 — vendor-managed + extensions)

> Vendor-generated by the `specify` CLI or installed as `.specify/extensions/`. **Never edit manually** — `specify upgrade` overwrites. Redline-specific behaviour belongs in `.specify/extensions.yml`. Listed here for inventory completeness only; Harriet does not govern their content.

| Skill | Kind |
|---|---|
| `speckit-specify`, `speckit-clarify`, `speckit-plan`, `speckit-tasks`, `speckit-implement`, `speckit-analyze`, `speckit-checklist`, `speckit-constitution`, `speckit-taskstoissues` | Vendor core |
| `speckit-critique-run`, `speckit-red-team-gate`, `speckit-red-team-run`, `speckit-plan-review-gate-check`, `speckit-version-guard-check`, `speckit-version-guard-load`, `speckit-version-guard-validate` | Extension |
| `speckit-shaping-gate-check`, `speckit-source-reconciliation-run`, `speckit-static-checks-run`, `speckit-verification-gate-run` | Extension (pointer files into `.specify/extensions/`) |

### Product Management

| Skill | Purpose | Used by |
|---|---|---|
| `pm-problem-framer` | Frame vague problems into testable statements | Mark |
| `pm-hypothesis-builder` | Formalise assumptions into falsifiable hypotheses | Mark |
| `pm-prd-builder` | Write Product Requirements Documents | Mark |
| `pm-decision-architect` | Structure deferred or instinct-driven decisions | Mark, Ron |
| `pm-personas` | Define customer archetypes and GTM segments | Mark, Ron, John |
| `pm-roadmap` | Build and refresh roadmaps and opportunity solution trees | Mark, Ron |
| `pm-prioritization` | Portfolio-level RICE / MoSCoW / Value-Effort ranking | Mark, John |
| `pm-product-strategist` | Vision, OKRs, strategic bets | Ron |
| `pm-structural-integrity-auditor` | Audit any product artifact for structural gaps | Mark, Ron, John, Peter |
| `strategy-pre-mortem` | Pre-mortem stress-testing of un-implemented plans | Ron |
| `strategy-psf-domain` | PSF/A/E/C domain grounding for competitor analysis, market segmentation, PI insurance | Ron |

### Marketing

| Skill | Purpose | Used by |
|---|---|---|
| `marketing-content-big-5` | They Ask You Answer / Big 5 content framework | John |
| `marketing-product-led-seo` | Product-Led SEO strategy and marketing-brief-to-PRD handoff | John |
| `linkedin-social-selling` | LinkedIn social selling, PIPA profiles, outreach (10:1 LCS rule) — *name corrected 2026-06-10 to match the on-disk folder; the taxonomy previously listed a phantom `marketing-social-selling-linkedin`. Metric-currency annex pending corroboration (gap table)* | John |
| `marketing-ai-content-review` | AI-assisted content review with mandatory expert sign-off | John |

### Skills Management & Meta

| Skill | Purpose | Used by |
|---|---|---|
| `writing-skills` | TDD-based skill authoring and testing (covers folder creation; absorbed the delisted `skills-create` phantom, founder ruling 2026-06-12) | Harriet, Engineering |
| `customization-mechanism-triage` | Select the correct VS Code Copilot customization mechanism (instruction, skill, agent, hook, prompt file, spec-kit extension, or plugin) before creating any artifact; auto-corrects misnamed requests | Harriet, Engineering |
| `using-superpowers` | Introduction to the skills system | All |
| `mental-models` | Structured thinking frameworks for decisions, root cause analysis, risk, communication (per `mental-models-protocol` instruction) | All |
| `doc-updater` | Keep codemaps and docs in sync with the codebase | Engineering |
| `redline-research` | Query multiple NotebookLM knowledge bases | All |

### Knowledge Infrastructure

| Skill | Purpose | Used by |
|---|---|---|
| `knowledge-infrastructure` | Digital library curation, notebook maintenance, register.json upkeep, standards monitoring procedures | Linda |

> `knowledge-infrastructure` skill is pending creation. Requires grounding from the "Information Architecture and Knowledge Management" notebook.

### People & Org

| Skill | Purpose | Used by |
|---|---|---|
| `hr-hire-agent` | Hiring a new agent: gap identification, JD drafting, onboarding, single-agent REFRESH for detected drift | Harriet |
| `hr-audit-agent` | Agent audits (scope overlaps, skill gaps) and Performance Improvement Plans (PIPs) | Harriet |
| `hr-maintain-agent-registry` | Updating org chart, agent register, and skills taxonomy after hires, deprecations, role changes, or post-sync promotions | Harriet |

> The former `hiring-agent-management` monolith was split into the `hr-*` family (see also `hr-sync-agent-topology` under Ceremonies). No folder named `hiring-agent-management` exists on disk.

### UX & Design

| Skill | Purpose | Used by |
|---|---|---|
| `ux-professional-software` | Information-dense UI design for professional/technical software, document-centric interaction patterns, annotation overlays, form design for technical inputs | Matt |
| `ux-conversion-design` | Co-development partner conversion UX (quota-exhaustion nudges, SSO gate, onboarding friction, 10→100→1000 phased conversion surfaces). Phase 1: founder-led recruitment. Phase 2: self-serve Pro purchase + referral loop | Matt |
| `ux-document-design` | Document-as-product design: structural hierarchy, placeholder formatting, metadata presentation, and standards citation styling in generated DOCX output | Matt |
| `ux-design-critique` | Structured self-review checklist: Nielsen heuristics scoring, cognitive load check, AI Language Policy compliance, cross-surface consistency, persona walk-through. Adapted from pbakaus/impeccable/critique framework for Markdown/Miro outputs. *Patch pending founder approval (drafted from Matt's 2026-06-10 Delta — `docs/people/drafts/agents/matt.agent.md`): adds worst-case-data stress check (Step 2b), WCAG 2.2 AA accessibility check (Step 2c), and co-development partner-feedback reconcile (Step 6)* | Matt |
| Playwright MCP *(built-in)* | Live website review via browser automation: navigate, screenshot, interact, inspect console/network, resize viewports. Governed by Matt's Website Review Protocol (pre-flight check, acceptance criteria loop, stop-on-unavailable). No separate skill file — protocol is embedded in Matt's JD. | Matt |

> `ux-professional-software`, `ux-conversion-design`, and `ux-document-design` are pending creation (see Skills Coverage Gaps below). `ux-design-critique` is embedded in Matt's agent JD (`.claude/agents/matt.md`) — no separate skill file. Playwright MCP is a built-in tool governed by the Website Review Protocol in Matt's JD.

### Engineering — Architecture, Evaluation & Governance

| Skill | Purpose | Used by |
|---|---|---|
| `ddd-strategic` | Strategic DDD: subdomain classification, context mapping, EventStorming, ACL pattern, UL stewardship, model evolution governance | Peter |
| `engineering-architecture` | System design, component boundaries, architectural compliance review of shaped work and SpecKit output | Peter |
| `arch-engineering` | **DUPLICATE** of `engineering-architecture` (frozen since `acba676` 2026-05-31; no JD routes to it; its "writing ADRs" claim also overlaps `create-adr`). **Deprecation CONFIRMED by Peter at the 2026-06-10 live Delta collection**, with a one-commit salvage condition: port the Common Mistakes table, the Decision Persistence section, and the grounding-sources list into `engineering-architecture` before deletion; discard its ADR Conventions (weaker subset of `create-adr`). Founder executes (sync item A-5) | *(none — orphaned)* |
| `create-adr` | Canonical ADR template and content rules — single source of truth for ADR authoring and review | Peter |
| `adr-constitution-sync` | Determine whether `.specify/memory/constitution.md` needs updating after an ADR is added/amended, and execute the sync | Peter |
| `design-eval-rubric` | Evaluation rubric design: scoring systems, test formats, LLM-as-judge patterns, judge calibration | Peter |
| `design-eval-pipeline` | Evaluation pipeline architecture: FTI pattern, HITL review, production monitoring, ground-truth collection | Peter |
| `define-ai-policy` | AI acceptable-use policy authoring: policy structure, DORA AI capabilities map, acceptable-use stance | Peter |
| `enforce-ai-batch-discipline` | PR size thresholds, author-side AI flagging, deliberate practice design, AI output verification mentoring | Peter |
| `shaping` | Shape Up shaping process adapted for Redline (Pitch format, breadboarding, rabbit hole identification, appetite setting, Two-Touch model) | Peter, Mark |

> `ddd-strategic` is live (promoted May 2026). The former `evaluation-architecture` stub was split into `design-eval-rubric` + `design-eval-pipeline`, and the former `ai-acceptable-use-policy` stub into `define-ai-policy` + `enforce-ai-batch-discipline` (commit `acba676`, 2026-05-31 "skill bloat reduction"). Notebook grounding remains pending where flagged in the Skills Coverage Gaps table. Peter's JD routing table is current with these names; this taxonomy caught up at the 2026-06-10 sync.

### Ceremonies

| Skill | Purpose | Used by |
|---|---|---|
| `ceremony-monthly-editorial-session` | Monthly Ground Engineering magazine editorial session | Graeme, John |
| `hr-sync-agent-topology` | Periodic cross-agent Topology Sync: Reflection Protocol (R1–R4), Delta Statements, orphan/overlap analysis, mandatory SRP Compliance Pass (`violations-list.md`), JD patch drafting — run quarterly or on: new hire, strategy pivot, major milestone, client feedback batch | Harriet (facilitating agent) |
| `agile-sprint-planning` | Start-of-sprint ceremony (Suggest/Lead modes): falsifiable sprint goal, INVEST-gated task selection, out-of-scope list, board materialization with blocking close gate, sprint plan document. Board mechanics deferred to `github-projects`. PM steward (Mark); Principal Engineer (Peter) consulted on unshaped tasks; founder confirms goal and scope | Mark (steward), Peter (consulted) |
| `agile-daily-standup` | Daily standup ceremony: read-only board review, blocker surfacing, optional `sync-this-week` write. PM steward (Mark); board writes blocked to PM | Mark (steward) |

> `hr-sync-agent-topology` is live at `.agents/skills/hr-sync-agent-topology/` — renamed from `sync-agent-topology` to match the `hr-*` family (rename uncommitted as of the 2026-06-10 sync). Harriet's JD routing-table update is staged at `docs/people/drafts/agents/harriet.agent.md`.

---

## Skills Coverage Gaps

> Harriet maintains this section. When a gap is identified during a hire or audit, log it here with the proposed remediation.

| Gap | Identified by | Proposed remediation | Status |
|---|---|---|---|
| `ux-professional-software` (information-dense UI, document-centric interaction, form design) | Harriet (2026-04-20, Matt hire) | Query `Product Design & UX` and `Information Architecture and Knowledge Management` notebooks; draft skill using `writing-skills` TDD cycle | Pending notebook grounding |
| `ux-conversion-design` (co-development partner conversion UX, 10→100→1000 phasing) | Harriet (2026-04-20, Matt hire; rescoped 2026-05-09) | Route through John for `Monetizing & Scaling Innovation` and `Digital Marketing & Social Selling` notebooks; combine with `Product Design & UX`; draft skill using `writing-skills` TDD cycle | Pending notebook grounding + John consultation |
| `ux-document-design` (document-as-product design for generated DOCX output) | Harriet (2026-05-09, Matt scope expansion) | Query `Product Design & UX` notebook for document design principles; consider Word/OOXML formatting constraints; draft skill using `writing-skills` TDD cycle | Pending — Sprint 1 priority |
| `ux-taskpane-design` (Word taskpane add-in interaction patterns) | Harriet (2026-05-09, Matt scope expansion) | Deferred until P-024 unfreezes. Query `Product Design & UX` notebook when ready | Deferred (P-024) |
| `ux-email-as-interface` (email template design for co-development and impact communication) | Harriet (2026-05-09, Matt scope expansion) | Collaborate with John on email copy patterns; draft skill using `writing-skills` TDD cycle | Deferred — Phase 2 |
| `knowledge-infrastructure` (library curation, notebook maintenance, register upkeep, standards monitoring) | Harriet (2026-04-25, Linda hire) | Query `Information Architecture and Knowledge Management` notebook; draft skill using `writing-skills` TDD cycle | Pending notebook grounding |
| `ddd-strategic` (strategic DDD: subdomain classification, context mapping, EventStorming, ACL, UL stewardship, model evolution governance) | Harriet (2026-05-17, DDD topology sync session) | Grounded via NotebookLM Software Architecture & DDD notebook. Promoted to `.agents/skills/ddd-strategic/` with 3 procedures. | **Live** |
| `engineering-architecture` (system design, ADRs, component boundaries) | Harriet (2026-05-16, Peter hire) | Strategic DDD content extracted to `ddd-strategic`. System-level architecture content still requires notebook grounding from Software Development Methodology & Engineering Organisation notebook. **2026-06-10 (Peter Delta):** salvage port from `arch-engineering` before its deletion (Common Mistakes table; Decision Persistence / `record_decision` section — AGENTS.md-mandated, absent from this skill; grounding-sources list: Team Topologies, Accelerate, Farley, Larson, Beck) **plus two stale-pointer fixes found live**: "Does Not Cover" cites pre-split `evaluation-architecture` (→ `design-eval-rubric`/`design-eval-pipeline`); cited notebook ID `cdb5e862-…` returns NOT_FOUND (correct register ID `91568710-98b3-4448-b038-04f9b48b7111`). One commit with sync item A-5. | Partially grounded — salvage + pointer fixes pending founder execution |
| `design-eval-rubric` + `design-eval-pipeline` (formerly `evaluation-architecture`; split 2026-05-31) | Harriet (2026-05-16, Peter hire) | Query `Software Development Methodology & Engineering Organisation` and `AI System Engineering` notebooks; ground both stubs | Stubs live under new names — notebook grounding pending |
| `shaping` (Shape Up process adapted for Redline) | Harriet (2026-05-16, Peter hire) | Query `Software Development Methodology & Engineering Organisation` notebook for Shape Up content; ground stub at `.agents/skills/shaping/` | Stub promoted — notebook grounding pending |
| `define-ai-policy` + `enforce-ai-batch-discipline` (formerly `ai-acceptable-use-policy`; split 2026-05-31) | Harriet (2026-05-16, Peter hire) | Query `Software Development Methodology & Engineering Organisation` notebook for DORA content; incorporate external DORA 2024-2026 research; ground both stubs | Stubs live under new names — notebook grounding + external research pending |
| `dev-environment` extension: dependency management guidance | Peter (2026-05-22, Kabilan hire consultation) | Add to existing `dev-environment` skill: `uv add` / `uv remove` patterns, `pyproject.toml` dependency declarations, when to escalate to Peter. Peter provides content; Harriet drafts patch. | **Live** (2026-05-23) |
| `python-domain-modeling` extension: layer architecture | Peter (2026-05-22, Kabilan hire consultation) | Add to existing `python-domain-modeling` skill: visual reference for Redline's layer architecture (`domain/`, `functions/`, `api/`), what belongs in each layer, prohibited cross-layer imports, escalation triggers. Peter provides content; Harriet drafts patch. | **Live** (2026-05-23) |
| `version-control` extension: PR discipline thresholds | Peter (2026-05-22, Kabilan hire consultation) | Add to existing `version-control` skill: maximum PR size (lines/files), "one logical change" definition, how to split PRs, SonarQube/Copilot detection, author-side AI feedback window. Peter provides content; Harriet drafts patch. | **Live** (2026-05-23) |
| `tool-selection` (CLI-first routing: `gh`, `gws`, `gcloud`, MCP, direct API) | ADR-016 (2026-06-06) | Promoted to `.agents/skills/tool-selection/`. Stale draft duplicate deleted — `docs/people/drafts/skills/` verified empty 2026-06-10. | **Live** (2026-06-06; cleanup confirmed 2026-06-10) |
| 13 GCP/DevOps skills: Cloud Run deploy, CI/CD pipeline, IAM least-privilege, Cloud SQL, IAP/OAuth wiring, observability, cost controls, container tuning, WIF, multi-tenancy, Secret Manager, infra-boundary-contract, **`terraform-iac` (added 2026-06-10 per ADR-020 — HCL authoring, plan/apply discipline, state operations)** | Harriet (2026-06-06, Brent topology screen; +1 at 2026-06-10 sync) | Ground from "DevOps & GCP Infrastructure" (8 books) and "GCP DevOps Tactical Playbook" (promoted to register 2026-06-07); `terraform-iac` additionally from HashiCorp documentation. Author with `writing-skills` TDD cycle. Until written, Brent uses WebFetch + Context7. **Brent's validated Delta (2026-06-10) refines two of the 13:** `terraform-iac` gains state surgery (`import`/`mv`/`rm`), provider-pinning maintenance, and a 6.x→7.x upgrade-evaluation checklist; the IAP/OAuth wiring skill must be updated **before issue #73 work begins** — direct IAP-on-Cloud-Run is GA (no load balancer, different audience handling), staling the JD template's audience format. | Deferred — next sprint (GitHub issue) |
| `agile-sprint-planning` and `agile-daily-standup` missing from `skills-lock.json` (authoritative source per ADR-001/ADR-009) | Harriet (2026-06-10, taxonomy currency check) | Resolved — both entries verified present in `skills-lock.json` at the 2026-06-11 sprint-planning skill audit (tier `planning`, `owner_agent: ["mark"]`, status `active`, layer 9), matching the taxonomy steward mapping. | **Resolved 2026-06-11** |
| SRP new-violations: `prek-find-and-fix`, `test-find-and-fix` (structural "and" in skill names) | Harriet (2026-06-10, Topology Sync SRP Compliance Pass) | Both mirror the approved `sonarqube-find-and-fix` `justified-orchestrator` pattern. Founder to approve adding both (plus the `sync-agent-topology` → `hr-sync-agent-topology` rename) to the Known Exception Skip-List in `hr-sync-agent-topology/procedures/srp-scan-procedure.md`. Must resolve before next sync. | Pending founder approval |
| Duplicate skill: `arch-engineering` vs `engineering-architecture` | Harriet (2026-06-10, Topology Sync) | `arch-engineering` frozen since 2026-05-31, unrouted by any JD, and overlaps `create-adr` on ADR authoring. Propose deletion of `.agents/skills/arch-engineering/` (founder approval — outside Harriet's write authority). **Peter confirmed at live Delta collection** — with the salvage condition recorded in the taxonomy row above and in the sync report (V-1/S-7). | Pending founder execution (A-5) |
| `hr-sync-agent-topology` protocol amendment: R2 question 1 is structurally unanswerable by static book corpora (null answers = valid protocol output, not failure; fall back to R2 question 2 + R3); add dispatched-session prerequisites (NotebookLM path via `nlm`, record CCE/ToolSearch availability) | Linda + Mark Delta Statements (2026-06-10, live collection); 4 of 8 sessions had no NotebookLM path | Harriet supplies amendment text; founder applies (`.agents/skills/` outside Harriet's write authority). Sync items S-5/A-23. | Pending founder approval |
| `create-adr` extension: reciprocal status convention ("Accepted, supersedes ADR-NNN") + **partial-supersession pattern** (status-line-only update on the partially superseded ADR; body immutable) | Peter Delta (2026-06-10) — R2 verbatim: literature silent on partial supersession; Redline codifies the convention | Peter supplies content; founder approves the edit; ADR-023 is the first exercise. Sync items S-6/A-24. | Pending founder approval |
| `marketing-product-led-seo` AI-citation-visibility annex (+ Big 5 note) and `linkedin-social-selling` saves/dwell metric update | John Delta (2026-06-10) — R3 findings flagged directional (secondary sources only) | **Corroboration-gated:** Linda sources one primary reference each (LinkedIn engineering 360Brew publication; primary Google AI Overviews/AI Mode source); then John drafts annexes; founder approves. Sync items S-9/A-26. No skill change until corroborated. | Blocked on primary sourcing |
| `notebooklm-cli` re-verification at `notebooklm-mcp-cli` 0.7.2 (we run 0.7.0; two patch releases in window) | Linda Delta (2026-06-10, PyPI evidence) | Founder approves the upgrade; Linda re-verifies the skill's command table against the new binary (no syntax change identified yet). Sync items S-10/A-22. | Pending founder approval |
| Standards-monitoring procedure mechanics (Linda): amendment-level tracking, withdrawal flagging, referenced-overseas-standards tracking, standards-body update-service subscription; plus the feed-tooling question (only `snz_scraper.py` exists — ISO/BSI/Standards AU unmonitored by tooling vs Linda's Outcome 4 wording) | Linda Delta (2026-06-10) — citable to `engineering-standards` notebook sources; domain decisions stay routed to Graeme | Bundled with founder decision A-18 (extend tooling vs narrow Outcome 4); Harriet drafts the Linda JD patch only if narrowed. Sync item S-11. | Pending founder decision |
