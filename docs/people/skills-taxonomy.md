# Skills Taxonomy & Catalog

**Owner (steward):** Harriet
**Last updated:** 2026-06-13

> **SOT for the category vocabulary and each skill's category assignment.** Nothing else.
>
> **Read this document to answer one question: "I have task X — which skill do I load?"**
> Scan the category, read the *Use when* column, load the skill. Everything else lives
> elsewhere:
>
> - *Who owns or uses a skill?* → `skills-lock.json` (`owner_agent`, authoritative per ADR-001/ADR-009) and the agent JDs in `.claude/agents/` (each agent's routing table is that agent's advertised interface)
> - *What layer is a skill / what may it reference?* → [docs/architecture/skills-architecture.md](../architecture/skills-architecture.md)
> - *What is missing, pending creation, deprecated, or awaiting a decision?* → [docs/people/skills-gaps.md](skills-gaps.md)
> - *Why the skills system works this way* → [docs/knowledge/software-engineering/skills-system.md](../knowledge/software-engineering/skills-system.md)
>
> **Derived column — Use when:** condensed from each skill's `SKILL.md` frontmatter
> `description` (the authoritative purpose statement). If this table and a frontmatter
> description disagree, the frontmatter wins; fix the row here.
>
> **Scope:** live, loadable skills only. Pending and deprecated skills are tracked in the
> gaps ledger, not here. Update this file in the same commit that creates, renames, or
> retires a skill.

---

## Category Vocabulary

A skill belongs to **exactly one** category — the one matching the task a consumer is
performing when they reach for it (not its layer, owner, or implementation language).

| Category | Definition |
|---|---|
| Python | Writing Python in this repo: style, typing, design, structure, documentation, errors, scripts, frameworks |
| Testing & Quality Gates | Writing tests and driving automated quality cycles: unit/API tests, TDD, static analysis, dependency hygiene, scan-triage-fix loops |
| Dev Environment | Bootstrapping and maintaining the local toolchain |
| Data & Datasets | Designing, ingesting, validating, and versioning datasets |
| EDA & Reporting | Exploring data and communicating results: codebooks, QA, visual design, Quarto outputs, diagrams |
| Git & Delivery | Version control conventions and the change-delivery path: commits, hooks, worktrees, code review, PR resolution |
| Security & Compliance | Secure coding policy: secrets, configuration, logging |
| Platform Adapters | Operating an external platform from this repo: Miro, NotebookLM, CCE, MCP tooling, GitHub Projects |
| Research & Knowledge | Querying and maintaining the knowledge infrastructure: notebooks, library, research workflows |
| Engineering Workflow | Cross-cutting engineering process: design exploration, debugging, parallel work, verification, session discipline, deferral |
| Architecture & Evaluation | System design, ADRs, domain-driven design, shaping, evaluation design, AI engineering policy |
| Product & Strategy | Product management and strategy artifacts: problems, hypotheses, PRDs, personas, roadmaps, prioritisation, bets |
| Marketing | Content, SEO, social selling, and AI-content review |
| Org & People | Hiring, auditing, and maintaining the agent workforce and its registers |
| Ceremonies | Recurring structured sessions with defined cadence and outputs |
| Skills System & Meta | Creating, selecting, and governing skills and customization mechanisms themselves |
| SpecKit (vendor) | Vendor-generated SpecKit command files — discovery listing only, never edited manually |

**Category placement rule:** choose the category whose *task* the consumer is doing.
Adding a new category requires: at least three live skills that fit no existing category,
a one-line definition added to this table in the same commit, and founder approval.
Parallel grouping schemes in other documents are prohibited (ADR-001).

---

## Catalog

### Python

| Skill | Use when |
|---|---|
| `python-style` | Applying Python style conventions — `uv` usage, formatting rules, idiomatic patterns |
| `python-typing` | Writing type hints — annotation style, generics, Optional, fixing mypy errors |
| `python-linting` | Resolving Ruff lint violations or deciding whether a suppression is safe |
| `python-paths` | Resolving file paths — pathlib vs importlib.resources vs repo helper; banned patterns |
| `python-patterns` | Writing idiomatic Python — control-flow, iteration, resource management, composition, concurrency |
| `python-function-design` | Designing functions — decomposing responsibilities, signatures, side effects |
| `python-class-design` | Designing classes — responsibilities, init patterns, composition over inheritance |
| `python-module-structure` | Ordering functions within a module — step-down rule, public-before-private |
| `python-documentation` | Writing docstrings — Google Style, type-hint integration |
| `python-error-handling` | Writing exception handling, translating errors across layers, structured logging |
| `python-domain-modeling` | Modeling domain objects — value objects, Pandera/Pydantic contracts, DataFrame-first APIs |
| `python-fastapi` | Implementing or testing external (north-south) FastAPI endpoints per the HTTP API standard (ADR-018) |
| `python-crewai` | Building CrewAI agents, tasks, flows, or output models |
| `python-script` | Writing scripts in `src/scripts/` — thin orchestration, Spyder-style cells |
| `python-script-numbering` | Naming pipeline scripts and documenting execution order |

### Testing & Quality Gates

| Skill | Use when |
|---|---|
| `python-testing-unit` | Writing unit tests — structure, fixtures, mocking, coverage patterns |
| `python-testing-api` | Writing API component or contract tests for FastAPI endpoints |
| `test-driven-development` | Implementing any feature or bugfix — RED-GREEN-REFACTOR before implementation code |
| `python-static-checks` | Running static checks — linting, type errors, pre-commit validation |
| `python-deptry` | Fixing deptry dependency-hygiene violations |
| `python-performance` | Profiling or optimising — tool choice, bottleneck diagnosis, algorithmic fixes |
| `sonarqube-scan` | Triggering a SonarQube scan and waiting for the compute-engine task to succeed |
| `sonarqube-review` | Retrieving, triaging, and recording false positives for open SonarQube issues on the branch |
| `sonarqube-find-and-fix` | Running the end-to-end SonarQube cycle: scan → triage → fix → re-scan |
| `prek-find-and-fix` | Running the end-to-end prek (pre-commit) cycle: run → triage → fix → re-run |
| `test-find-and-fix` | Running the end-to-end test-suite cycle: run → triage failures → fix → re-run |

### Dev Environment

| Skill | Use when |
|---|---|
| `dev-environment` | Bootstrapping or maintaining the dev environment — uv, tasks, prek |
| `python-usethis` | Adding, removing, or inspecting dev tools via the usethis CLI |

### Data & Datasets

| Skill | Use when |
|---|---|
| `data-tidy` | Designing DataFrame schemas or value-object models to tidy-data principles |
| `python-data-ingestion` | Implementing ingestion or validation — import/process/read patterns, Pandera contracts |
| `python-pins-data-version-control` | Versioning datasets with pins — board layout, naming, read/write patterns |

### EDA & Reporting

| Skill | Use when |
|---|---|
| `eda-codebook` | Generating or updating a Markdown codebook for a CSV/Excel dataset |
| `eda-interpreting-data` | Screening data quality before plotting, or writing insights after results |
| `eda-qa` | Auditing an existing codebook plus raw dataset for data-quality problems |
| `eda-visual-design` | Choosing chart types, encoding data, reducing cognitive load in visualisations |
| `python-plot-colors` | Selecting plot colors — colormaps, color-blindness safety, cross-figure consistency |
| `qmd-tables` | Rendering tabular output in Quarto — formatting helpers, table-vs-chart decisions |
| `qmd-narrative-design` | Designing Quarto reports/presentations — Hook-Problem-Insight-Proof-Action arc |
| `mermaid-diagrams` | Adding or reviewing Mermaid diagrams — type selection, v8.8.0 syntax ceiling, quality rules |

### Git & Delivery

| Skill | Use when |
|---|---|
| `git-version-control` | Applying version-control conventions — commit hygiene, prek hooks, pre-push checks |
| `git-push-batched` | Pushing changes — organising dirty files into thematically cohesive commits |
| `git-hooks-create` | Implementing, registering, or testing project-specific git hooks in `hooks/` |
| `using-git-worktrees` | Starting feature work needing isolation from the current workspace |
| `requesting-code-review` | Completing tasks or features — pre-review checklist before merging |
| `resolving-pr-issues` | Resolving PR review comments — structured triage, fail-first test, fix, CI closure |

### Security & Compliance

| Skill | Use when |
|---|---|
| `security` | Writing secure code — secrets handling, configuration safety, structured logging |

### Platform Adapters

| Skill | Use when |
|---|---|
| `mcp-cce` | Discovering code/docs/company memory via CCE; persisting context across sessions |
| `miro-mcp` | Working with Miro boards — creating/reading diagrams, layouts, structured context |
| `notebooklm-cli` | Setting up, authenticating, or troubleshooting NotebookLM access via the `nlm` CLI |
| `python-mcp-tools` | Calling MCP tools or servers from Python code |
| `rag-prompting` | Writing queries for a NotebookLM notebook — prompt anatomy, retrieval rules, extraction |
| `github-projects` | Creating, updating, moving, or querying tasks on the Redline GitHub Projects board |

### Research & Knowledge

| Skill | Use when |
|---|---|
| `redline-research` | Asked to research, investigate, or look something up — knowledge base before online search |
| `notebooklm-deep-research` | Running NotebookLM deep research with 5 Whys intake and notebook indexing |
| `notebooklm-index` | Adding, updating, or auditing a notebook in the NotebookLM index spreadsheet |
| `library-management` | Indexing, renaming, or adding books to the digital library |

### Engineering Workflow

| Skill | Use when |
|---|---|
| `brainstorming` | Before any creative work — explores intent, requirements, and design first |
| `systematic-debugging` | Encountering any bug, test failure, or unexpected behavior — before proposing fixes |
| `subagent-driven-development` | Executing implementation plans with independent tasks in the current session |
| `dispatching-parallel-agents` | Facing 2+ independent tasks with no shared state or ordering |
| `verification-before-completion` | About to claim work complete — evidence before assertions |
| `session-handover` | Ending a development session — handover note, CCE decision writes, uncommitted-work flags |
| `task-defer` | Deferring a task, idea, or decision — `docs/deferred/` entry with mandatory unfreeze condition |
| `doc-updater` | Updating codemaps or docs to match the codebase — packages, routes, scripts, README |
| `spec-kit` | Planning a feature, writing a spec, breaking work into tasks — wraps the SpecKit CLI |

### Architecture & Evaluation

| Skill | Use when |
|---|---|
| `engineering-architecture` | Making system-level design decisions, defining component boundaries, reviewing architectural compliance |
| `create-adr` | Writing, extending, or reviewing an ADR — canonical template and content rules |
| `adr-constitution-sync` | After an ADR is added or amended — checks and executes constitution sync |
| `ddd-strategic` | Classifying subdomains, context mapping, EventStorming, ACLs, ubiquitous-language stewardship |
| `shaping` | Translating product intent or a PRD into a scoped Pitch before SpecKit |
| `design-eval-rubric` | Designing evaluation rubrics — scoring, test formats, LLM-as-judge calibration |
| `design-eval-pipeline` | Architecting evaluation pipelines — FTI, HITL review, monitoring, ground truth |
| `define-ai-policy` | Authoring or reviewing AI acceptable-use policy — structure, DORA map, stance |
| `enforce-ai-batch-discipline` | Configuring PR-size thresholds, AI flagging, deliberate practice, AI-output verification mentoring |

### Product & Strategy

| Skill | Use when |
|---|---|
| `pm-problem-framer` | A problem statement is vague, contested, or missing segment/outcome/strategic link |
| `pm-hypothesis-builder` | Formalising an assumption into a falsifiable hypothesis before any experiment |
| `pm-prd-builder` | An initiative has a validated hypothesis and engineering/design needs a formal brief |
| `pm-decision-architect` | A decision is avoided, delayed, or instinct-driven with no explicit options or criteria |
| `pm-personas` | Defining a customer archetype or GTM segment before PRD, strategy, or campaign work |
| `pm-roadmap` | Building, refreshing, or auditing roadmaps and opportunity solution trees |
| `pm-prioritization` | Ranking features or bets at portfolio level — RICE, MoSCoW, Value-Effort |
| `pm-structural-integrity-auditor` | Auditing any product artifact for structural gaps before it causes misaligned work |
| `pm-product-strategist` | Starting a product, refreshing strategy, or reconnecting OKRs to customer problems |
| `strategy-pre-mortem` | Stress-testing an un-implemented plan, launch, or bet before execution |
| `strategy-psf-domain` | Competitor analysis, market segmentation, or product-market fit for civil-engineering consultancies |

### Marketing

| Skill | Use when |
|---|---|
| `marketing-content-big-5` | Planning content topics — They Ask You Answer / Big 5 framework |
| `marketing-product-led-seo` | Planning SEO beyond blog content — programmatic tools, brief-to-PRD handoff |
| `linkedin-social-selling` | Building or auditing a LinkedIn presence for B2B social selling |
| `marketing-ai-content-review` | Drafting AI-assisted content with domain claims — mandatory expert sign-off |

### Org & People

| Skill | Use when |
|---|---|
| `hr-hire-agent` | Hiring a new agent — gap identification, JD drafting, onboarding, single-agent refresh |
| `hr-audit-agent` | Auditing an agent for scope overlaps or skill gaps; running a PIP |
| `hr-maintain-agent-registry` | Updating org chart, agent register, or this catalog after hires, retirements, or role changes |
| `hr-sync-agent-topology` | Running the periodic Agent Topology Sync — Reflection Protocol, Delta Statements, SRP pass |

### Ceremonies

| Skill | Use when |
|---|---|
| `agile-sprint-planning` | Starting a new sprint, or a sprint is running with no goal on record |
| `agile-daily-standup` | Every morning — structured daily brief from live board state |
| `agile-backlog-grooming` | On-demand backlog audit: classify items, produce decision table, execute founder-approved rows |
| `ceremony-monthly-editorial-session` | A new Ground Engineering issue arrives — editorial processing for content and product signals |

### Skills System & Meta

| Skill | Use when |
|---|---|
| `using-superpowers` | Starting any conversation — how to find and use skills |
| `writing-skills` | Creating, editing, or verifying skills — TDD-based authoring (covers folder creation) |
| `mental-models` | A structured thinking framework is needed — decisions, root cause, risk, communication |
| `customization-mechanism-triage` | Before creating any customization artifact — selects instruction vs skill vs agent vs hook vs prompt file vs plugin |
| `tool-selection` | Deciding which CLI (`gh`, `gws`, `gcloud`), MCP, or API to use, and which orchestration tier fits a fan-out task (ADR-016) |

### SpecKit (vendor)

> Vendor-generated by the `specify` CLI or installed as `.specify/extensions/`.
> **Never edit manually** — `specify upgrade` overwrites. Redline-specific behaviour
> belongs in `.specify/extensions.yml`. Outside `skills-lock.json` governance; listed for
> discovery only.

| Skill | Kind |
|---|---|
| `speckit-specify`, `speckit-clarify`, `speckit-plan`, `speckit-tasks`, `speckit-implement`, `speckit-analyze`, `speckit-checklist`, `speckit-constitution`, `speckit-taskstoissues` | Vendor core |
| `speckit-critique-run`, `speckit-red-team-gate`, `speckit-red-team-run`, `speckit-plan-review-gate-check`, `speckit-version-guard-check`, `speckit-version-guard-load`, `speckit-version-guard-validate` | Extension |
| `speckit-shaping-gate-check`, `speckit-source-reconciliation-run`, `speckit-static-checks-run`, `speckit-verification-gate-run` | Extension (pointer files into `.specify/extensions/`) |