# Feature Specification: Mental Models Skill

**Feature Branch**: `008-mental-models`

**Created**: 2026-05-27

**Status**: Draft

**Input**: Design and implement a `mental-models` skill for the Redline agent system — a reusable, agent-agnostic library of mental models (thinking frameworks) that advisory and expert agents can reference.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Agent invokes a mental model by name during reasoning (Priority: P1)

An advisory agent (Ron, Mark, Graeme, Peter, or Matt) is reasoning through a problem. The agent references the `mental-models` skill to retrieve a specific model's definition, application guide, and anti-patterns.

**Why this priority**: This is the primary consumer workflow. Without retrievable model files there is no skill.

**Independent Test**: Load `mental-models/general_thinking/circle-of-competence.md` in isolation and verify it contains all required sections (What it is / Core principle / When to invoke / How to apply / Anti-patterns / Source). No other files required.

**Acceptance Scenarios**:

1. **Given** an agent needs to apply second-order thinking, **When** it references `mental-models/general_thinking/second-order-thinking.md`, **Then** the file exists, is self-contained, and contains all six required sections.
2. **Given** an agent is performing root cause analysis, **When** it references `mental-models/root_cause_analysis/five-whys.md`, **Then** the file describes the 5-Whys method with application steps and anti-patterns.
3. **Given** any mental model file, **When** read in isolation, **Then** it contains no references to agent names, agent JD files, or other skill files (standalone constraint).

---

### User Story 2 — Agent applies the Accountable Response Protocol (Priority: P1)

An advisory agent produces a response. The agent must be able to state (1) which reasoning pattern was used, (2) what would falsify the conclusion, and (3) what falls outside its competence. The `mental-models` skill provides the vocabulary and frameworks to satisfy this protocol.

**Why this priority**: Directly implements Ron's Accountable Response Protocol — the primary goal of the entire feature.

**Independent Test**: After adding the `## Mental Models` section to one agent JD (e.g., Ron), verify the agent can name the models it invokes and describe their falsification conditions. Deliverable is demonstrable in a single agent update.

**Acceptance Scenarios**:

1. **Given** Ron answers a strategy question, **When** asked "what reasoning pattern did you use?", **Then** Ron names at least one model from its `## Mental Models` section and cites the corresponding file.
2. **Given** Mark reviews a hypothesis, **When** challenged on a bias, **Then** Mark can reference `cognitive-biases.md` and explain whether confirmation bias or sunk cost applies.
3. **Given** Graeme assesses a geotechnical risk, **When** asked what would change the conclusion, **Then** Graeme references `black-swan.md` and identifies the tail-risk condition.

---

### User Story 3 — SKILL.md catalog enables discovery of all available models (Priority: P2)

An agent or developer opens `mental-models/SKILL.md` to discover what models exist, how they are organised, and where each model file lives.

**Why this priority**: Discoverability is necessary for agents to browse and select models without knowing filenames in advance.

**Independent Test**: Read `SKILL.md` alone and verify it lists all 10 model files, their categories, and a one-line description. No other skill files required.

**Acceptance Scenarios**:

1. **Given** `mental-models/SKILL.md`, **When** read, **Then** it lists all 10 models grouped by category subfolder with file paths and one-line descriptions.
2. **Given** `mental-models/SKILL.md`, **When** read, **Then** it contains no agent names, agent JD references, or cross-skill references (bottom-layer constraint).
3. **Given** a new model is added to a category subfolder, **When** `SKILL.md` is updated, **Then** the new entry appears in the correct category section.

---

### User Story 4 — Agent JDs updated to declare mental model competence (Priority: P2)

The five agent JD files (Ron, Mark, Graeme, Peter, Matt) each gain a `## Mental Models` section declaring four universal models plus one role-specific model, with a role-calibration paragraph.

**Why this priority**: Without JD updates agents cannot reference the skill with any specificity; the Accountable Response Protocol cannot be enforced.

**Independent Test**: Update Ron's JD only. Verify it contains the `## Mental Models` section with Circle of Competence, Inversion, Second-Order Thinking, Probabilistic Thinking, and Reversible vs. Irreversible Decisions, plus a calibration paragraph.

**Acceptance Scenarios**:

1. **Given** Ron's JD, **When** read, **Then** it contains `## Mental Models` with all 4 universal models + Reversible vs. Irreversible Decisions.
2. **Given** Matt's JD, **When** read, **Then** it contains `## Mental Models` with all 4 universal models + Third Story.
3. **Given** any updated JD, **When** its `## Mental Models` section is read, **Then** each model entry links to its corresponding file in `.agents/skills/mental-models/`.

---

### User Story 5 — `resolving-pr-issues` skill refactored to reference 5-Whys model (Priority: P3)

The inline 5-Whys description in `resolving-pr-issues/SKILL.md` and `procedures/resolve-comments.md` is stripped and replaced with a pointer to `mental-models/root_cause_analysis/five-whys.md`.

**Why this priority**: Reduces duplication and establishes `mental-models` as the canonical source; lower priority than creating the skill itself.

**Independent Test**: After refactoring `resolving-pr-issues/SKILL.md`, verify the inline 5-Whys steps are removed and a reference link to `five-whys.md` is present.

**Acceptance Scenarios**:

1. **Given** `resolving-pr-issues/SKILL.md`, **When** read after refactoring, **Then** it contains no inline 5-Whys explanation and includes a reference to `mental-models/root_cause_analysis/five-whys.md`.
2. **Given** `procedures/resolve-comments.md`, **When** read after refactoring, **Then** the inline 5-Whys label is replaced with a link to `five-whys.md`.

---

### Edge Cases

- What happens when an agent references a model file that does not yet exist? → Agents must only reference files listed in `SKILL.md`; the catalog is the authoritative index.
- How does a model file handle a concept that overlaps with another model? → Each file is self-contained; cross-references are permitted in the Anti-patterns section only, and only by filename (not by agent name or skill name).
- What if a role-specific model conflicts with a universal model's guidance? → Role calibration paragraphs in agent JDs provide the resolution; model files themselves are never modified for agent-specific concerns.
- What happens when the NotebookLM source notebook is unavailable? → Model files are static Markdown; they do not depend on live notebook access after initial authoring.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `mental-models` skill MUST provide a `SKILL.md` catalog file that lists all model files organised by category subfolder, with file paths and one-line descriptions, and contains no agent names or cross-skill references.
- **FR-002**: The skill MUST include 10 model files arranged in category subfolders: `general_thinking/` (4 files), `root_cause_analysis/` (1 file), `strategic_decisions/` (2 files), `self_awareness/` (1 file), `risk_analysis/` (1 file), `communication/` (1 file).
- **FR-003**: Every model file MUST use a uniform six-section structure: **What it is** / **Core principle** / **When to invoke** / **How to apply** / **Anti-patterns** / **Source**.
- **FR-004**: Every model file MUST be standalone — no references to agent names, agent JD files, or other skill files.
- **FR-005**: Model definitions MUST be sourced from the "Strategy and Mental Models" NotebookLM notebook (ID: c56b0801-40c9-4208-b31f-72ed360da184), which contains *Super Thinking* (Weinberg), *The Great Mental Models Vol. 1* (Parrish), *The Decision Book* (Krogerus), and *The Art of Strategy* (Dixit & Nalebuff).
- **FR-006**: The five agent JDs (Ron, Mark, Graeme, Peter, Matt) MUST each gain a `## Mental Models` section containing the four universal models (Circle of Competence, Inversion, Second-Order Thinking, Probabilistic Thinking) plus one role-specific model, with a role-calibration paragraph.
- **FR-007**: Role-specific model assignments MUST be: Ron → Reversible vs. Irreversible Decisions; Mark → Cognitive Biases; Graeme → Black Swan; Peter → OODA Loop; Matt → Third Story.
- **FR-008**: `resolving-pr-issues/SKILL.md` MUST be refactored to remove any inline 5-Whys description and replace it with a reference link to `mental-models/root_cause_analysis/five-whys.md`.
- **FR-009**: `procedures/resolve-comments.md` (if it exists and contains an inline 5-Whys label) MUST be updated to reference `mental-models/root_cause_analysis/five-whys.md` instead.
- **FR-010**: The `.specify/feature.json` MUST be updated to reflect `specs/008-mental-models` as the active feature directory.

### Key Entities

- **Mental Model File**: A self-contained Markdown document with six fixed sections. Identified by category subfolder and filename. Has no dependencies on other files.
- **SKILL.md Catalog**: The index file for the `mental-models` skill. Lists all model files with paths and one-line descriptions, grouped by category. Consumed by agents; never consumes other skills.
- **Agent JD `## Mental Models` section**: A section added to each advisory agent's JD declaring which models the agent uses, with role calibration. Consumes mental model files; never modifies them.
- **Category Subfolder**: An organisational unit within `.agents/skills/mental-models/`. One of: `general_thinking/`, `root_cause_analysis/`, `strategic_decisions/`, `self_awareness/`, `risk_analysis/`, `communication/`.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 10 model files exist at their specified paths and each passes a manual review confirming all six required sections are present and no agent names appear in the file.
- **SC-002**: `SKILL.md` lists all 10 model files with correct paths and one-line descriptions; a reviewer can locate any model within 30 seconds of opening the catalog.
- **SC-003**: All five agent JDs contain a `## Mental Models` section; each section correctly assigns 4 universal models + 1 role-specific model.
- **SC-004**: At least one advisory agent (Ron or Mark), when prompted with a strategy or product question, references a named mental model from its JD section in its reasoning, demonstrating the Accountable Response Protocol in practice.
- **SC-005**: `resolving-pr-issues/SKILL.md` contains zero inline 5-Whys steps after refactoring; a single reference link to `five-whys.md` is present instead.
- **SC-006**: No model file contains references to agent names, agent JD paths, or other skill file paths (verified by grep across all files in the skill folder).

---

## Assumptions

- The "Strategy and Mental Models" NotebookLM notebook (c56b0801-40c9-4208-b31f-72ed360da184) is accessible and contains the four listed source books; model definitions will be drafted from this notebook.
- Agent JD files are at `.agents/` (e.g., `rl.ron.agent.md`, `rl.mark.agent.md`, etc.); their exact filenames will be confirmed before editing.
- `procedures/resolve-comments.md` may or may not exist; FR-009 is conditional on its existence.
- Kabilan's JD update is explicitly deferred and out of scope for this specification.
- No automated enforcement hooks are in scope; model usage by agents is by convention, not tooling.
- The skill sits at the bottom layer of the agent architecture: it is consumed by agent JDs and skills, but it itself consumes nothing.
- Mental model content is static Markdown after initial authoring; no live data sources are required at runtime.
