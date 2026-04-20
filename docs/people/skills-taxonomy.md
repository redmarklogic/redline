# Skills Taxonomy

**Owner:** Harriet  
**Last updated:** 2026-04-20  
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

### Infrastructure & Security

| Skill | Purpose | Used by |
|---|---|---|
| `security` | Secure coding (secrets, configuration, logging) | Engineering |
| `version-control` | Commit conventions, hygiene, pre-commit, pre-push | Engineering |
| `git-push-batched` | Push changes in thematically cohesive commits | Engineering |
| `pre-commit-hooks-create` | Writing bespoke pre-commit hooks | Engineering |
| `python-mcp-tools` | MCP tooling usage in this repo | Engineering |
| `notebooklm-mcp` | Query NotebookLM notebooks from Copilot Agent | Harriet, Graeme, Ron, John, Mark |
| `miro-mcp` | Create diagrams and visual artifacts on Miro boards | Mark, John, Ron |

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

### People & Org

| Skill | Purpose | Used by |
|---|---|---|
| `hiring-agent-management` | Operating playbook for the People & Agent Development role (hire, audit, PIP, org management) | Harriet |

### Ceremonies

| Skill | Purpose | Used by |
|---|---|---|
| `ceremony-monthly-editorial-session` | Monthly Ground Engineering magazine editorial session | Graeme, John |

---

## Skills Coverage Gaps

> Harriet maintains this section. When a gap is identified during a hire or audit, log it here with the proposed remediation.

| Gap | Identified by | Proposed remediation | Status |
|---|---|---|---|
| UX for technical professional software | Harriet (2026-04-20, during Alex hire) | Install `frontend-design` from `anthropics/skills`; commission `rl-ux-for-engineers` from `Product Design & UX` notebook | Pending notebooks load + user approval |
