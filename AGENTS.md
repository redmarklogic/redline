# Custom Instructions

## General Guidelines

- We are using Windows for development and Linux for deployment. So, when running commands in terminal, use Windows commands, like ";" instead of "&&" to separate commands.
- Run scripts and tests in virtual environment: .\.venv\Scripts\activate; python -m <...>
- Every time I ask you to fix linter errors and provide the error messages, update the linting skill (`.agents/skills/python-linting/SKILL.md`) accordingly (add a concise one-line reminder only if it's not already covered).
- Never tell me what I want to hear. I want you to look at things objectively, contradict me when needed. If you think otherwise, go with your strong opinion.
- Never create notebooks (ipynb files) unless asked explicitly.
- For lessons (reusable observations from LLM conversations and review sessions), see `docs/lessons/lesson_template.md` for format and filing rules.
- **Lessons workflow**: When a concrete, non-obvious insight emerges during a conversation
  (or the user asks to document a learning), create a new file in `docs/lessons/` following
  the template (`NNNN-kebab-slug.md`). Before creating, check existing lesson files to avoid
  duplication -- update the existing file if the insight refines a known principle. Do NOT
  create a lesson when the observation is too vague, the conversation is still evolving, or
  the insight is already covered.

## Skills

All skills live at `.agents/skills/<name>/SKILL.md`. Load the relevant skill(s) before starting any task that falls within their domain.

### Python --- Core

- **`python-style`**: General style and `uv` usage conventions
- **`python-patterns`**: Idiomatic patterns and idioms
- **`python-typing`**: Type hint standards
- **`python-linting`**: Ruff/lint compliance and safe suppressions
- **`python-paths`**: File path conventions (pathlib, importlib.resources, repo\_)
- **`python-error-handling`**: Exception handling, error translation, and logging
- **`python-documentation`**: Docstring standards (Google Style)
- **`python-function-design`**: Function decomposition, signatures, and side effects
- **`python-class-design`**: Class responsibilities, init, and composition
- **`python-domain-modeling`**: Value objects, Pandera/Pydantic, DataFrame-first APIs
- **`python-module-structure`**: How to order functions within a Python module --- the step-down rule, public-before-private ordering, helper extraction, and separating executable code from implementation.

### Python --- Testing

- **`python-testing-unit`**: Unit testing standards
- **`python-testing-api`**: FastAPI component and contract tests
- **`test-driven-development`**: RED-GREEN-REFACTOR cycle --- enforces write failing test, watch it fail, write minimal code, watch it pass, commit; deletes code written before tests.

### Python --- Tooling & Environment

- **`dev-environment`**: Bootstrap and maintain the dev environment (uv, tasks, pre-commit)
- **`python-usethis`**: Add/remove dev tools (pyproject-fmt, ruff, deptry, etc.)
- **`python-static-checks`**: Running static checks (always do this before finishing)
- **`python-deptry`**: Dependency hygiene with deptry
- **`python-performance`**: Profiling and optimisation patterns

### Python --- Scripts

- **`python-script`**: Script conventions (stepdown rule, thin orchestration, Spyder-style cells)
- **`python-script-numbering`**: Script naming and execution order conventions

### Data & Domain

- **`data-tidy`**: Tidy data principles (Wickham) and guidelines for designing tidy tables, DataFrame schemas, and value-object models (language-agnostic).
- **`python-pins-data-version-control`**: Dataset versioning with the pins library
- **`python-data-ingestion`**: Data ingestion and validation (import/process/read pattern, Pandera schemas, multi-worksheet handling, TDD workflow)
- **`python-crewai`**: CrewAI agent, task, flow, and output model conventions

### EDA & Reporting

- **`eda-codebook`**: Generates and updates comprehensive Markdown codebooks (data dictionary + statistical profile) for CSV and Excel datasets.
- **`eda-interpreting-data`**: Pre-flight data quality screening and post-plot insight writing (apply before any distribution, scatter, or time-series plot)
- **`eda-qa`**: Ingests an existing codebook + raw dataset, nominates data quality problems, validates hypotheses, and updates the codebook's Findings section with concrete findings. If no codebook exists, stops and directs the user to run `eda-codebook` first.
- **`eda-visual-design`**: Chart type selection, encoding, labelling, cognitive load (apply _after_ `eda-interpreting-data`)
- **`python-plot-colors`**: Color selection, colormap choice, color-blindness safety, and cross-figure consistency for all plotting libraries used in this repo.
- **`qmd-tables`**: Rendering tables in Quarto documents (great_tables GT, HTML/PDF helpers)
- **`qmd-narrative-design`**: Narrative design for reports and presentations (Hook-Problem-Insight-Proof-Action arc)
- **`mermaid-diagrams`**: Mermaid diagram type selection, syntax constraints (v8.8.0 ceiling), when-to-diagram rules, and quality guidance for Markdown documents

### Infrastructure & Security

- **`security`**: Secure coding (secrets, configuration, logging)
- **`version-control`**: Commit conventions, hygiene, pre-commit, and pre-push checks
- **`git-push-batched`**: Push changes to git in thematically organised commits — groups dirty files into cohesive batches, proposes them for user confirmation, then stages and commits each batch before pushing. By default, auto-commits without waiting for confirmation.
- **`pre-commit-hooks-create`**: Writing bespoke pre-commit hooks
- **`python-mcp-tools`**: MCP tooling usage in this repo
- **`notebooklm-mcp`**: NotebookLM MCP server setup, authentication, and allowed/forbidden tools in VS Code
- **`notebooklm-index`**: Index NotebookLM notebooks into the register spreadsheet at `G:\My Drive\Library\index-notebooklm.xlsx`
- **`rag-prompting`**: Prompt engineering for NotebookLM queries --- prompt anatomy, RAG retrieval rules, structured extraction schemas, and hallucination scoping
- **`spec-kit`**: Specification-driven development (specs, plans, tasks, implementation) --- wraps GitHub Spec Kit CLI with project presets for RICE scoring, MoSCoW, vertical slice sizing, and domain impact assessment.
- **`doc-updater`**: Documentation and codemap maintenance (codemaps, README, guides)

### Advisory Board (Product & Strategy)

Four named personas. Invoke by name. None writes code.

**Epistemic honesty (binding on all Advisory Board agents):** When any agent (Graeme,
Ron, Mark, or John) cannot find grounded material to answer a question, they say "I don't
know" and identify the gap. They never invent facts, fabricate citations, or present
ungrounded speculation as knowledge. Unverified pointers to external resources are
permitted only when clearly labelled as such.

- **Ron** (`rl.ron.agent.md`): Strategy & GTM Advisor. Vision, strategic bets, OKRs, positioning,
  GTM motion. Advisory Board access unlocks the Founder Memos notebook via `redline-research`.
  Invoke: "Ron, [request]"

- **Mark** (`rl.mark.agent.md`): Principal Product Manager. Problem framing, hypotheses, PRDs,
  decision architecture. Every PRD must reference a Ron-defined strategic bet.
  Invoke: "Mark, [request]"

- **Graeme** (`rl.graeme.agent.md`): Principal Geotechnical Engineer (25+ years in a large civil
  engineering consultancy). Domain expert for geotechnical engineering questions. Knowledge
  grounded in the engineering and geotechnical NotebookLM notebooks. Curates domain knowledge
  to `docs/knowledge/geotechnical/`. Advisory Board access unlocks engineering notebooks.
  Invoke: "Graeme, [request]"

- **John** (`rl.john.agent.md`): Head of Marketing — Demand, Content & Brand. Owns content
  marketing (They Ask You Answer / Big 5), SEO and Product-Led SEO, LinkedIn social selling,
  brand voice, editorial calendar, and the monthly market-signal report fed back to Ron and
  Mark. Sits downstream of Ron (consumes positioning/ICP/GTM motion) and parallel to Mark
  (co-owns Product-Led SEO via marketing-brief-to-PRD handoff). Advisory Board access
  unlocks `Digital Marketing & Social Selling`, `Entrepreneurship & Startup Strategy`, and
  `Monetizing & Scaling Innovation` notebooks. Writes only to `docs/product/marketing/`.
  Invoke: "John, [request]"

- **Matt** (`rl.matt.agent.md`): UI/UX Designer across four product surfaces (web, Word
  documents, Word taskpane, email agent). Interaction design, wireframes, component specs,
  and user flow design. Downstream of Mark (consumes PRDs), upstream of speckit (produces
  design specs). Knowledge grounded in the Product Design & UX notebook. Writes only to
  `docs/product/design/`.
  Invoke: "Matt, [request]"

**PM skills (loaded on demand by Mark and/or Ron):**

- `pm-problem-framer`, `pm-hypothesis-builder`, `pm-prd-builder`, `pm-decision-architect`,
  `pm-product-strategist`, `pm-structural-integrity-auditor`
- `strategy-pre-mortem` — pre-mortem stress-testing of un-implemented plans (Ron-owned)
- `strategy-psf-domain` — PSF/A/E/C domain grounding for competitor analysis, market segmentation, PI insurance, and engineering workflows (Ron-owned)
- `pm-personas` — customer archetypes (Mark + Ron co-owned)
- `pm-roadmap` — visual roadmaps and opportunity solution trees (Mark-owned, Ron-contributed)
- `pm-prioritization` — portfolio-level RICE / MoSCoW / Value-Effort (Mark-owned). Distinct
  from `spec-kit`'s scenario-level RICE; see `docs/architecture/skills-architecture.md`.

**Marketing skills (loaded on demand by John):**

- `marketing-content-big-5` — They Ask You Answer / Big 5 content framework
- `marketing-product-led-seo` — Product-Led SEO co-design with Mark (marketing brief → PRD)
- `marketing-social-selling-linkedin` — PIPA profiles, 10:1 LCS rule, Sales Navigator targeting
- `marketing-ai-content-review` — AI-assisted drafting with mandatory Graeme/Mark/Ron sign-off
- John also uses `pm-personas` (shared), `pm-prioritization` (campaign ranking),
  `pm-structural-integrity-auditor` (`/challenge`), `qmd-narrative-design` (long-form), and
  `miro-mcp` (Content Segmentation Grid, campaign maps).

**UX skills (loaded on demand by Matt):**

- `ux-professional-software` — information-dense UI design, document-centric interaction patterns
- `ux-conversion-design` — co-development partner conversion UX (quota-exhaustion, SSO gate, onboarding)
- `ux-document-design` — document-as-product design for generated DOCX output
- `ux-design-critique` — structured self-review checklist (Nielsen heuristics, cognitive load, AI Language Policy). *Embedded in Matt's agent JD (`.github/agents/rl.matt.agent.md`) — no separate skill file.*
- Matt also uses `pm-personas` (shared read-only), `pm-structural-integrity-auditor` (`/challenge`),
  `miro-mcp` (wireframes, user flows), and `notebooklm-mcp` (Product Design & UX notebook).

**Handoff chain (non-negotiable):**
```
Graeme (domain facts) → Ron (vision → bets → OKRs → positioning → GTM motion)
                          ↓
               Mark (problem → hypothesis → PRD)        John (content, SEO, social, campaigns)
                          ↓                                ↓
               Matt (design specs, wireframes)          published assets / channels
                          ↓                                ↓
               spec-kit (engineering)                      ↓
                                       ↘             ↙
                                Monthly Signal Report → back to Ron + Mark
```

Key John-specific dynamics:
- Ron → John: positioning, ICP, GTM motion. John never invents these.
- Mark → John: validated personas, launch-ready PRDs, Product-Led SEO PRDs.
- John → Mark: Product-Led SEO marketing briefs (John never writes the PRD).
- John → Graeme: every technical claim before publishing (mandatory, blocking).
- John → Ron + Mark: monthly signal report (John's most strategic contribution).

Key Matt-specific dynamics:
- Mark → Matt: PRDs. Matt never designs without a PRD.
- Matt → Graeme: domain terminology verification (mandatory, blocking).
- Matt → John: conversion-critical designs for positioning and micro-copy review.
- Matt → speckit.specify: design specs for engineering handoff.

**`/challenge <artifact>`** loads `pm-structural-integrity-auditor` on any document.

**Output directory:** `docs/product/` (strategy/, strategic-bets.md, okrs/, positioning.md, gtm/,
hypotheses/, initiatives/, prds/, problems/, decisions/, marketing/, design/), `docs/knowledge/geotechnical/` (Graeme)

#### Visual Artifacts Policy (Markdown vs Miro)

Markdown is canonical for narrative and decision artifacts. Miro is canonical for relational
and spatial artifacts. PM skills declare which medium they own; `miro-mcp` is the rendering
toolset, not a skill that decides what to render.

| Artifact | Canonical medium | Owner |
|---|---|---|
| Strategic bets, OKRs, positioning, GTM plan | Markdown | Ron |
| PRDs, problem statements, hypotheses, decision logs | Markdown | Mark |
| Geotechnical domain knowledge | Markdown (`docs/knowledge/geotechnical/`) | Graeme |
| Roadmaps, opportunity solution trees, story maps, journey maps | **Miro** (Markdown synthesis optional) | Mark (Ron contributes strategic thread) |
| Customer archetypes / personas | **Hybrid**: Miro for collaborative drafting; Markdown canonical reference | Mark + Ron |
| Prioritization matrices (RICE / MoSCoW / Value-Effort) | **Miro** matrix or spreadsheet; Markdown table for the final ranking | Mark |
| Marketing campaigns, content briefs, signal reports, editorial calendar, style guide | Markdown (`docs/product/marketing/`) | John |
| Content Segmentation Grid (content × persona × buying-cycle stage) | **Miro** matrix; Markdown index in `docs/product/marketing/` | John |
| Design specifications, interaction pattern docs | Markdown (`docs/product/design/`) | Matt |
| Wireframes, user flows, annotated mockups | **Miro** (Markdown design spec canonical) | Matt |

Do not auto-mirror every Markdown artifact to Miro — mirror on demand. Drift starts when both
surfaces try to be canonical for the same content.

> **Note on `speckit.*` agents:** These files are vendor-generated by the `specify` CLI and
> **must not be edited manually**. Running `specify upgrade` will overwrite manual changes.
> All Redline-specific extensions belong in `.specify/extensions.yml`, not in these files.

### Internal Operations (platform functions)

Two platform agents that serve all other agents. Neither makes domain decisions.

- **Linda** (`rl.linda.agent.md`): Knowledge Infrastructure Operator. Curates and indexes
  the digital library at `G:\My Drive\Library`, maintains NotebookLM notebooks and
  `register.json`, monitors standards body feeds and routes updates to Graeme. Domain-agnostic
  --- organises content but never interprets it. X-as-a-Service interaction mode.
  Invoke: "Linda, [request]"

- **Harriet** (`rl.harriet.agent.md`): Head of People & Agent Development. Agent hiring,
  audits, PIPs, skill gap management, org design. Maintains agent register, org chart, and
  skills taxonomy. Draft-first maturity.
  Invoke: "Harriet, [request]"

### Marketing (loaded on demand by John)

- **`marketing-content-big-5`**: Use when planning content marketing topics, deciding what blog posts, videos, or pages to publish next, or when prospects keep asking the same sales questions — applies the They Ask You Answer / Big 5 framework.
- **`marketing-product-led-seo`**: Use when planning SEO strategy beyond blog content, considering free programmatic tools or calculators to capture organic search traffic, or when handing an SEO idea off to product and engineering.
- **`marketing-social-selling-linkedin`**: Use when building LinkedIn presence for the founder or sales team, optimising LinkedIn profiles, planning prospecting outreach, or designing comment-and-engagement campaigns on LinkedIn.
- **`marketing-ai-content-review`**: Use when drafting marketing content with generative AI for a technical domain, or before publishing any AI-assisted content that makes domain claims requiring expert verification.

### Redline Project Research

- **`redline-research`**: Structured research workflow for Redline --- queries multiple NotebookLM knowledge bases with iterative cross-referencing; outputs cited Markdown documents to `docs/research/`. Never uses online search. Notebook register at `.agents/skills/redline-research/register.json`. Apply whenever the user asks to "research", "investigate", or "look up" something in the Redline knowledge base.

### Skills Management

- **`skills-create`**: Creating new skills

### External Skills (obra/superpowers)

Source: <https://github.com/obra/superpowers>

- **`brainstorming`**: Socratic design refinement --- activates before writing code; teases out a spec through questions, explores alternatives, and presents design in sections for validation. Terminal state invokes `spec-kit`.
- **`dispatching-parallel-agents`**: Concurrent subagent workflows --- dispatches multiple agents in parallel to work on independent tasks.
- **`finishing-a-development-branch`**: Merge/PR decision workflow --- verifies tests, presents options (merge/PR/keep/discard), cleans up worktrees.
- **`receiving-code-review`**: Responding to feedback --- structured process for addressing code review comments. **This is the canonical skill for all PR comment handling, including irrelevant comments. NEVER use the `address-pr-comments` VS Code extension skill — it is superseded by this skill.**
- **`requesting-code-review`**: Pre-review checklist --- reviews against plan, reports issues by severity before submitting for review.
- **`subagent-driven-development`**: Fast iteration with two-stage review --- dispatches fresh subagent per task with spec compliance then code quality review.
- **`systematic-debugging`**: 4-phase root cause process --- structured debugging with root-cause-tracing, defense-in-depth, and condition-based-waiting techniques.
- **`using-git-worktrees`**: Parallel development branches --- creates isolated workspaces on new branches, runs project setup, verifies clean test baseline.
- **`using-superpowers`**: Introduction to the skills system --- explains how to load and use skills effectively.
- **`verification-before-completion`**: Ensure it's actually fixed --- verifies that errors are truly resolved before declaring success.
- **`writing-skills`**: Create new skills following best practices --- includes testing methodology for skill creation.

## General Style

- **MUST** use meaningful, descriptive variable and function names.
- **MUST** use spaces for indentation (never tabs).
- **NEVER** use emoji, or unicode that emulates emoji (e.g. ✓, ✗). The only exception is when
  writing tests and testing the impact of multibyte characters.
- **NEVER** import `argparse`. We are not building CLI tools; scripts should be configured via
  environment variables or constants.
- **NEVER** implement custom environment loaders (e.g., manual `.env` file parsers). Assume the
  environment is correctly configured by the caller (shell, orchestrator, or container).
- **NEVER** set default values for environment variables in scripts (e.g., use `os.environ.get("VAR")` or a required helper, not `os.getenv("VAR", "default")`), unless explicitly asked to do so by the user.
- **AVOID** adding unnecessary helper functions that increase code bloat; assume the "happy path"
  unless complex error handling is explicitly required by domain logic.
- **NEVER** introduce section rules, e.g. `# ---------------------------------------------------------------------------`.

## Version and Package Assumptions

- The workspace is Python 3.12-only, so code should not branch on `sys.version_info`, package
  `__version__`, or similar interpreter/package predicates.
- Supported Python versions are declared in `pyproject.toml` under `project.requires-python`.
- Dependencies are declared in `pyproject.toml` and reproduced via the `uv.lock` lockfile.
- Before using any new third-party API, consult the Context7 docs for that package to confirm the function/class exists and behaves as expected---do not rely on runtime feature detection.

## Python

- Baseline Python style and `uv` usage: see `.agents/skills/python-style/SKILL.md`.
- Dev environment setup (including `uv sync`): see `.agents/skills/dev-environment/SKILL.md`.

## Code Structure & Data Handling

- Baseline domain modeling rules: see `.agents/skills/python-domain-modeling/SKILL.md`.

## Linter

- Baseline linting rules: see `.agents/skills/python-linting/SKILL.md`.
- When you ask me to fix linter errors and provide the error messages, I will update
  `.agents/skills/python-linting/SKILL.md` (not this file) with a concise one-line reminder only if it's
  not already covered.

## Documentation & Workflow Management

- **ALWAYS** report which skills from `.agents/skills/` were used and for what purpose in your final response using the format **skill-name**: <what did you apply> on what **element**, and link to `.agents/skills/<skill-name>/SKILL.md`. IF you did not use any skills, explicitly state "No skills applied".
- Document reusable knowledge (e.g., library versions, fixes, corrections) in the `Lessons` section of `scratchpad.md`.
- ADRs are immutable decision records, not project management tools. They sit at
  the bottom of the documentation hierarchy. Rules:
  - **Include**: Decision, Status, Context, Options Considered, Rationale, Consequences,
    References (other ADRs, external docs, RFCs, library docs only).
  - **Exclude**: follow-up actions or task checklists (belong in tasks.md); links to specs,
    plans, or tasks (upward dependencies); scratchpad notes (ephemeral). Embed any
    relevant research findings directly in the ADR body instead.

## Refactors

- Do not keep deprecated shim modules/packages after refactors; migrate imports and delete old paths immediately.
- You may offer backward-compatibility options, but do not implement backward compatibility unless the user explicitly asks for it.

## Archive

- The `archive/` directory contains archived code from previous implementations. This code is for **reference only** and **MUST NOT** be imported or used in the current codebase.

## Ask for clarification

- If any part of the request is ambiguous or unclear, ask for clarification before proceeding.
- Ask questions, enumerate the alternatives, recommend the best option, and wait for confirmation before proceeding.

## Perform static checks before finishing

Always finish by using the `python-static-checks` skill to check for linting errors, type errors, and other static issues before finalizing your response. This ensures that the code you provide is clean and adheres to our quality standards.

# Coding Guidelines

Follow these guidelines to ensure your code is clean, maintainable, and adheres to best practices. Remember, less code is better. Lines of code = Debt.

# Key Mindsets

**1** **Simplicity**: Write simple and straightforward code.
**2** **Readability**: Ensure your code is easy to read and understand.
**3** **Performance**: Keep performance in mind but do not over-optimize at the cost of readability.
**4** **Maintainability**: Write code that is easy to maintain and update.
**5** **Testability**: Ensure your code is easy to test.
**6** **Reusability**: Write reusable components and functions.
