# Skills Taxonomy

**Owner:** Harriet  
**Last updated:** 2026-04-25  
**Source of truth for:** all skills in `.agents/skills/`, their domain category, and which agents use them.

> Update this file whenever a skill is created, retired, or reassigned.

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

### Python — Testing

| Skill | Purpose | Used by |
|---|---|---|
| `python-testing-unit` | Unit testing standards | Engineering |
| `python-testing-api` | FastAPI component and contract tests | Engineering |
| `test-driven-development` | RED-GREEN-REFACTOR cycle | Engineering |

### Python — Tooling & Environment

| Skill | Purpose | Used by |
|---|---|---|
| `dev-environment` | Bootstrap and maintain dev environment (uv, tasks, pre-commit) | Engineering |
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
| `version-control` | Commit conventions, hygiene, pre-commit, pre-push | Engineering |
| `git-push-batched` | Push changes in thematically cohesive commits | Engineering |
| `pre-commit-hooks-create` | Writing bespoke pre-commit hooks | Engineering |
| `python-mcp-tools` | MCP tooling usage in this repo | Engineering |
| `notebooklm-mcp` | Query NotebookLM notebooks from Copilot Agent | Harriet, Graeme, Ron, John, Mark, Linda |
| `miro-mcp` | Create diagrams and visual artifacts on Miro boards | Mark, John, Ron |

### Research & Knowledge

| Skill | Purpose | Used by |
|---|---|---|
| `redline-research` | Structured research workflow querying NotebookLM knowledge bases | Graeme, Ron, Mark, John |
| `rag-prompting` | Query design for NotebookLM — prompt anatomy, retrieval rules, structured extraction | Graeme, Ron, Mark, John, Linda |
| `library-management` | Index, rename, and add books to the digital library | Linda |

### Development Workflow

| Skill | Purpose | Used by |
|---|---|---|
| `brainstorming` | Socratic design refinement before implementation | Engineering |
| `spec-kit` | Specification-driven development (specs, plans, tasks) | Engineering |
| `subagent-driven-development` | Fast iteration with two-stage review | Engineering |
| `dispatching-parallel-agents` | Concurrent subagent workflows | Engineering |
| `using-git-worktrees` | Parallel development in isolated git worktrees | Engineering |
| `finishing-a-development-branch` | Merge/PR decision workflow | Engineering |
| `requesting-code-review` | Pre-review checklist | Engineering |
| `receiving-code-review` | Responding to code review feedback | Engineering |
| `verification-before-completion` | Verify errors are truly resolved before claiming done | Engineering |
| `systematic-debugging` | 4-phase root cause debugging process | Engineering |

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
| `pm-structural-integrity-auditor` | Audit any product artifact for structural gaps | Mark, Ron, John |

### Marketing

| Skill | Purpose | Used by |
|---|---|---|
| `marketing-content-big-5` | They Ask You Answer / Big 5 content framework | John |
| `marketing-product-led-seo` | Product-Led SEO strategy and marketing-brief-to-PRD handoff | John |
| `marketing-social-selling-linkedin` | LinkedIn social selling, PIPA profiles, outreach | John |
| `marketing-ai-content-review` | AI-assisted content review with mandatory expert sign-off | John |

### Skills Management & Meta

| Skill | Purpose | Used by |
|---|---|---|
| `skills-create` | Create a new skill folder and SKILL.md | Harriet, Engineering |
| `writing-skills` | TDD-based skill authoring and testing | Harriet, Engineering |
| `using-superpowers` | Introduction to the skills system | All |
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
| `hiring-agent-management` | Operating playbook for the People & Agent Development role (hire, audit, PIP, org management) | Harriet |

### UX & Design

| Skill | Purpose | Used by |
|---|---|---|
| `ux-professional-software` | Information-dense UI design for professional/technical software, document-centric interaction patterns, annotation overlays, form design for technical inputs | Matt |
| `ux-conversion-design` | Co-development partner conversion UX (quota-exhaustion nudges, SSO gate, onboarding friction, 10→100→1000 phased conversion surfaces). Phase 1: founder-led recruitment. Phase 2: self-serve Pro purchase + referral loop | Matt |
| `ux-document-design` | Document-as-product design: structural hierarchy, placeholder formatting, metadata presentation, and standards citation styling in generated DOCX output | Matt |
| `ux-design-critique` | Structured self-review checklist: Nielsen heuristics scoring, cognitive load check, AI Language Policy compliance, cross-surface consistency, persona walk-through. Adapted from pbakaus/impeccable/critique framework for Markdown/Miro outputs | Matt |
| Playwright MCP *(built-in)* | Live website review via browser automation: navigate, screenshot, interact, inspect console/network, resize viewports. Governed by Matt's Website Review Protocol (pre-flight check, acceptance criteria loop, stop-on-unavailable). No separate skill file — protocol is embedded in Matt's JD. | Matt |

> `ux-professional-software`, `ux-conversion-design`, and `ux-document-design` are pending creation (see Skills Coverage Gaps below). `ux-design-critique` is embedded in Matt's agent JD (`.github/agents/rl.matt.agent.md`) — no separate skill file. Playwright MCP is a built-in tool governed by the Website Review Protocol in Matt's JD.

### Ceremonies

| Skill | Purpose | Used by |
|---|---|---|
| `ceremony-monthly-editorial-session` | Monthly Ground Engineering magazine editorial session | Graeme, John |

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
