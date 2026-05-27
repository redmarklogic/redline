# Research: Mental Models Skill

**Phase 0 output** | **Feature**: 008-mental-models | **Date**: 2026-05-27

All design decisions were resolved during a structured brainstorming session
(Harriet × Ron × founder, 2026-05-27). No NEEDS CLARIFICATION markers remain in spec.md.

---

## D1 — Skill structure

**Decision**: Approach A — category subfolders, agent assignment handled in SKILL.md (fan-out index)

**Rationale**: Decouples model definitions from agent assignments. Models are stable;
agent assignments evolve. Putting assignment logic in SKILL.md means model files never
need editing when an agent JD changes. Category subfolders (general_thinking, self_awareness,
etc.) match the taxonomy from the source notebooks and support browsing without reading SKILL.md.

**Alternatives considered**:
- Approach B (universal/ + role_specific/ top-level): Over-engineered for 9 files; coupling
  agent identity to file location creates friction when models graduate from role-specific to universal.
- Approach C (agent sections inside each model file): Violates the bottom-layer constraint;
  model files would need updating every time an agent JD changes.

---

## D2 — SKILL.md as bottom layer

**Decision**: SKILL.md contains no agent names, no references to other skills.

**Rationale**: Bottom-layer artifacts must be unconditionally importable — they cannot have
outbound dependencies on agents or other skills because that would create circular dependency
risk as the agent org evolves. Ron's "layer diagram" makes this explicit: skills sit below
agent JDs in the consumption hierarchy.

**Alternatives considered**:
- SKILL.md as fan-out with agent routing: Rejected. The skill becomes stale every time an
  agent is added, renamed, or has their model set changed.

---

## D3 — Model curation: Hybrid 4+1

**Decision**: 4 universal models shared across all 5 agents + 1 role-specific addition per agent.

**Rationale**: Addresses two distinct failure modes simultaneously:
- Failure mode A (generic, confidence-miscalibrated answers) — fixed by the 4 universals
  as a shared epistemic contract across the advisory board.
- Failure mode B (wrong reasoning tool for the domain) — fixed by the 1 role-specific
  addition that targets each agent's primary failure mode.

Strategy Narrow (universals only) leaves Failure Mode B unaddressed.
Strategy Wide (50+ models) fails on maintenance cost and the 12-mental-model overload problem
— agents loaded with too many models apply them indiscriminately.

**Maintenance projection (12-month)**:
- Universals: stable, sourced from foundational texts, minimal drift risk
- Role-specific files: 1 file per agent; when a JD evolves, exactly 1 file to review
- Total: 10 model files + SKILL.md + 5 JD sections = maintainable by one person in under an hour/quarter

---

## D4 — Role calibration location: agent JDs only

**Decision**: Role-specific calibration paragraphs live in agent JDs, not in model files.

**Rationale**: Model files are standalone reference documents. Calibration (how the model
applies to Graeme's geotechnical work specifically) is agent identity content — it belongs
in the JD. Keeping it there means model files never need editing for agent-specific concerns,
and the calibration stays visible to whoever reads the JD.

**Analogy**: A legal dictionary defines "negligence" once. Each law firm's practice guide
explains how negligence applies to their specific practice area. The dictionary does not
know about the firms.

---

## D5 — Universal model selection

**Decision**: Circle of Competence, Inversion, Second-Order Thinking, Probabilistic Thinking.

**Rationale** (Ron's three non-negotiables + one addition):

1. **Circle of Competence** — master key; every over-confident failure traces to operating
   outside known boundaries. Epistemic humility operationalised.
2. **Inversion** — highest single-move leverage across all five roles. "What would make this
   fail?" is universally underused and universally high-leverage.
3. **Second-Order Thinking** — universal antidote to first-order optimism. "And then what?"
   applies to strategy, product, architecture, design, and domain assessment.
4. **Probabilistic Thinking** (Ron's fourth) — the alternative to probability is false certainty;
   all five agents operate in domains where uncertainty is endemic.

---

## D6 — 5 Whys addition

**Decision**: Add `root_cause_analysis/five-whys.md` as an 11th file (not in Ron's original 9).

**Rationale**: Required to support the `resolving-pr-issues` refactor (SC-005, FR-008).
The 5 Whys is already referenced by name in that skill's postmortem-lite step. Without
a canonical file to point to, the refactor cannot remove the inline description.
The 5 Whys is a genuine root-cause analysis method — it belongs in the library independent
of the refactor motivation.

---

## Source material

All model definitions sourced from NotebookLM notebook `c56b0801-40c9-4208-b31f-72ed360da184`:

| Book | Author | Models sourced |
|------|--------|----------------|
| The Great Mental Models Vol.1 | Shane Parrish | Circle of Competence, Inversion, Second-Order Thinking, First Principles, Probabilistic Thinking, Occam's Razor |
| Super Thinking | Gabriel Weinberg & Lauren McCann | Probabilistic Thinking, Inversion, Systems Thinking, Eisenhower Matrix, Reversible vs. Irreversible |
| The Decision Book | Krogerus & Tschäppeler | OODA Loop, Cognitive Biases, Black Swan, 5 Whys |
| The Art of Strategy | Dixit & Nalebuff | Nash Equilibrium, Game theory frameworks |
| Difficult Conversations | Stone, Patton & Heen | Third Story |
