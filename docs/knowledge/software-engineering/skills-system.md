# Skills System — Narrative Guide

> **NOT a source of truth for layer assignments or skill ownership.**
> This document contains narrative context, onboarding prose, and design history only.
> It must never enumerate skills by layer or tier.
>
> Authoritative sources:
> - Layer assignments (L0-L9): [docs/architecture/skills-taxonomy.md](../../architecture/skills-taxonomy.md)
> - Tier, ownership, status: `skills-lock.json`
> - Handoff chain: [docs/architecture/skills-architecture.md](../../architecture/skills-architecture.md)

**Owner**: Peter (Principal Engineer)

---

## What is a skill?

A **skill** is a small Markdown file that teaches the AI a single, well-defined competence.
Think of it like a recipe card pinned to a kitchen wall. The AI does not memorise the
recipe; it walks over to the wall, reads the card, and follows the steps when the situation
calls for it.

Each skill lives in its own folder at `.agents/skills/<skill-name>/SKILL.md` and answers
three questions:

1. **When should I use this?** (the trigger)
2. **When should I NOT use this?** (the guardrail)
3. **How do I do it?** (the steps)

Without organisation, the AI would have to read all skills every time you ask a question.
Layering solves this by constraining which skills are relevant to a given context.

---

## Why layers exist — the handoff and dependency problem

Two distinct organisational concerns govern the skill system:

**The handoff chain** (who gives work to whom) runs top-down:
strategy → product → shaping → spec → implementation.

**The dependency graph** (which skills may reference which) runs bottom-up:
a skill at a higher layer may reference skills at lower layers, never the reverse.

These are two different views of the same system. The handoff chain is like an org chart
(reporting lines). The dependency graph is like a module import graph (what each module
is allowed to import). The taxonomy governs the import graph. The architecture doc
governs the org chart.

---

## Why the layer ordering is what it is

The ordering was arrived at by asking: *"Which skill actually references which?"* —
not by analogy to other architectural patterns.

### Mistakes corrected from v1

The first version cargo-culted the onion architecture from software (domain core at center,
infrastructure outside) and applied it to skills without verifying the causal mechanism.

| v1 error | Root cause | Correction |
|---|---|---|
| Python implementation patterns at Layer 2 (low) | Assumed code patterns are stable like domain models — they are not; they change as defects are found | Moved to Layer 6 (high, volatile) |
| Quality & tooling above implementation patterns | Assumed tests depend on patterns — actually patterns reference tests | Inverted: Quality (L5) below Implementation (L6) |
| Only `spec-kit` identified as vendor | Missed 12 skills from `obra/superpowers` | All vendor skills at Layer 0 |
| Language-agnostic and Python-specific mixed in same layer | No polyglot principle | Separated: polyglot at Layer 2, Python at Layer 4+ |
| MCPs placed above quality/tooling | Assumed platform adapters are volatile — they are not; they are narrow and stable | MCPs at Layer 3, below quality |

Mental models that would have prevented these errors:
- **Cargo Cult** (`mental-models/root_cause_analysis/cargo-cult.md`) — reproducing the
  form of onion architecture without verifying the causal mechanism
- **First Principles** (`mental-models/general_thinking/first-principles.md`) — start from
  observed dependencies, not analogies

---

## Why each layer is where it is — narrative rationale

**Layer 0 — Vendor Primitives**: Skills the project does not control. Placed at the
foundation because nothing project-owned should depend on something that can be silently
overwritten by a vendor update. *Don't depend on what you can't control* (Dependency
Inversion Principle).

**Layer 1 — Foundational Registries**: Concepts defined once, referenced everywhere.
`mental-models` has zero outbound references by design — it is the bedrock. Everything
above can cite it; it cites nothing. A change here has the largest blast radius in the
system (Reversible vs Irreversible: `mental-models/strategic_decisions/reversible-vs-irreversible.md`).

**Layer 2 — Language-Agnostic Standards**: Rules that apply regardless of programming
language. Placed above foundational registries and below language-specific rules because
Python skills in Layer 4+ are *implementations* of these polyglot concepts, not the
other way around.

**Layer 3 — Platform Integrations (MCPs)**: Narrow adapters to external platforms. Stable
and rarely changing — they know nothing about how they are used. Placed below quality
tooling because quality tools reference the dev environment and MCP setup, not the reverse.

**Layer 4 — Core Language Standards**: Baseline Python conventions that change
infrequently. They assume polyglot standards (Layer 2) and platform adapters (Layer 3)
but know nothing about how functions or classes are designed (Layer 6).

**Layer 5 — Quality & Tooling**: Skills that verify, check, or install. Testing references
core language standards (Layer 4) and MCPs (Layer 3). Implementation patterns (Layer 6)
reference quality skills — the causality runs upward from tests to code patterns, not
downward. This inversion from the v1 order is the most counter-intuitive correction.

**Layer 6 — Python Implementation (volatile)**: The most frequently changing layer. How
functions, classes, modules, and domain models are written. Volatile because real-world
defects in coding workflows are discovered and corrected here. Belongs high in the stack
so lower layers are not destabilised by these changes.

**Layer 7 — Applied Capabilities**: Compound workflows that combine Python implementation,
MCPs, and quality tools into coherent domain-specific capabilities. EDA, reporting,
research. These are the first layer where the skills are visibly about *Redline's work*
rather than general programming.

**Layer 8 — Engineering Workflows**: End-to-end processes spanning the entire stack:
shaping a pitch, reviewing architecture, releasing code, creating a skill. These reference
everything below and are the highest layer Peter owns directly.

**Layer 9 — Product, Strategy & Organisation**: Agent-level skills for named personas
(Ron, Mark, John, Matt, Harriet). Most volatile in terms of business context. May reference
anything below — they are the orchestration layer.

---

## How to find the right skill

1. **Identify the layer** — which question does your task answer?
   - "Should we build this?" → L1 (Ron, strategy)
   - "What problem, for whom?" → L2 (Mark, product)
   - "Is this buildable, what are the boundaries?" → L2.5 (Peter, shaping)
   - "What exactly are we building?" → L3 (spec-kit)
   - "How do we write the code?" → L4-L6 (implementation)
   - "What tools can we call?" → L5 (tools & platform)
2. **Open `AGENTS.md`** — every skill is listed under its layer with a one-line description.
3. **Read the skill's `description:` line** — starts with "Use when..." and tells you
   the trigger. If your situation matches the trigger, the skill applies.
4. **Read the "When NOT to Use" section** — often where you discover you are reaching
   for the wrong skill.

---

## A worked example: the trip from idea to code

Suppose you say: *"I want users to be able to export their reports as PDF."*

| Step | Layer | What happens |
|---|---|---|
| 1 | L1 — Ron | "Does this map to one of our strategic bets? If yes, which one? If no, stop and revisit." |
| 2 | L2 — Mark | "Who exactly wants PDF export? What problem does it solve? Is this top of the list? Write the PRD." |
| 3 | L2.5 — Peter | "Is this feasible in 6 weeks? Shape it: set boundaries, remove rabbit holes, write the Pitch." |
| 4 | L3 — spec-kit | "Turn the Pitch into a spec with acceptance scenarios, a plan, and a task list." |
| 5 | L4-L6 — implementation | "Write the code following style, function-design, and testing-unit standards." |
| 6 | L5 — tools | At any point, use `miro-mcp` to draft a roadmap, `redline-research` to look up prior decisions, or `version-control` to commit work. |

Skipping a layer is the most common failure mode:
- PRD without a strategic bet (skipping L1) → work nobody wanted
- Spec without a PRD (skipping L2) → feature the team cannot explain
- Spec without shaping (skipping L2.5) → scope with hidden rabbit holes
- Code without a spec (skipping L3) → something that works but solves the wrong problem

---

## Two RICE skills, two altitudes — why they were not merged

Two skills both mention RICE prioritisation:

- `pm-prioritization` (L9) — ranks **initiatives across the portfolio**. Should we build
  the PDF exporter, or the new dashboard, or the Salesforce integration?
- `spec-kit` (L3) — ranks **acceptance scenarios within a single spec**. Inside the PDF
  exporter spec, which scenarios ship in v1 and which in v2?

These are different decisions made by different people at different times. Merging them
would force the engineering team to import portfolio-level concerns into every spec, and
force product to think about acceptance scenarios when ranking initiatives.

---

## Two media for artifacts — Markdown and Miro

Some artifacts are best as text, others as visual layouts. The split is codified in the
"Visual Artifacts Policy" section of `AGENTS.md`. Short version:

- **Markdown wins** for narrative, decisions, and version-controlled records: PRDs,
  strategic bets, OKRs, positioning, decision logs, hypotheses.
- **Miro wins** for spatial and relational artifacts: roadmaps, opportunity solution trees,
  story maps, journey maps, prioritisation matrices.
- **Hybrid** for personas: Miro to draft collaboratively, Markdown as the canonical
  reference once stable.

Miro is rendered via the `miro-mcp` skill. Skills declare which medium they own;
`miro-mcp` is the rendering tool, not the decision-maker.

---

## Named agents vs skills

Mark, Ron, Peter, Matt, and Harriet are not skills. They are **personas** —
addressable identities you invoke by name. Each persona has a routing table that tells it
which skills to load when. Think of them as the chefs who know which recipe cards to pick
off the wall.

Persona files live in `.github/agents/<name>.agent.md` and are governed by the same
handoff rules described in the architecture doc.

---

## Principle elaborations

### Dependency Direction — why the import rule

"A skill at layer N may reference skills at layers 0 through N — never higher." This
mirrors the Python import rule: a module in a lower package must not import from a higher
one. For skills, "import" means "reference" — invoking, loading, or pointing to another
skill as a prerequisite or cross-reference. The invariant is enforced by convention and
verified when adding any cross-skill reference.

### Stability Gradient — the corollary

Changes to lower layers are harder to reverse because the blast radius is larger
(`mental-models/strategic_decisions/reversible-vs-irreversible.md`). Skills that change
frequently as defects are found (implementation patterns, coding guidance) belong in upper
layers, not lower ones. Platform adapters and standards that rarely change belong near the
foundation.

### Vendor Boundary — don't depend on what you can't control

Vendor updates overwrite local modifications. A project-owned skill that references a
vendor skill would have its reference silently invalidated on the next vendor update.
Vendor skills therefore sit at Layer 0 with no outbound references to project-owned skills.
Sourced from the Dependency Inversion Principle (AI System Engineering notebook).

### Single Source of Truth — registries at the bottom

`mental-models` defines concepts once. Other skills reference its files rather than
redefining concepts inline. Each inline definition is a fork that drifts. This applies
ADR-001 to the skill layer.

### Polyglot Before Language-Specific

Language-agnostic skills sit below language-specific skills. Python skills are
implementations or customisations of polyglot concepts. If a concept applies regardless
of programming language, it belongs in a lower layer.

### Deep Modules at Layer Boundaries

Each layer exposes a minimal, stable interface upward. Prefer fewer powerful skills per
layer over many shallow ones that leak implementation details
(`mental-models/general_thinking/deep-modules.md`).

### Horizontal Independence

Skills within the same layer may reference each other when logically necessary. This is
not a violation. The rule applies only to *vertical* dependencies: no upward references.

### Placement Rule

When placing a new skill:
> *"What is the highest-numbered layer containing all the skills this skill needs to reference?"*
> Place the new skill at that layer + 1 (or at the same layer if it references nothing).

---

## References

- [skills-taxonomy.md](../../architecture/skills-taxonomy.md) — authoritative layer map and dependency rules (SOT for layer assignments)
- [skills-architecture.md](../../architecture/skills-architecture.md) — handoff chain
- `AGENTS.md` — agent invocation manifests
- `skills-lock.json` — machine-readable registry (tier, owner, layer)
- `hooks/sync-layer-to-lock.py` — derives `layer` field in lock file from taxonomy
- ADR-001 — single source of truth policy
- ADR-009 — skill classification and governance registry
- `mental-models/general_thinking/deep-modules.md`
- `mental-models/general_thinking/systems-thinking.md`
- `mental-models/strategic_decisions/reversible-vs-irreversible.md`
- `mental-models/root_cause_analysis/cargo-cult.md`
- `mental-models/general_thinking/first-principles.md`
