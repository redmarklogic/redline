# ADR-009: Dependency Inversion Principle as the Governing Rule of the Skills/Agents Boundary

## Summary

Redline formally adopts the Dependency Inversion Principle (DIP) as the governing rule of
the boundary between skills and agents. The hard constraint this imposes: skills are the
stable inner core of the system; agents are the volatile outer layer that orchestrates them.
Dependencies must point inward — agents may reference skills, skills must never reference
agents. The direction of dependency is the opposite of the direction of information flow.
Any skill that names an agent, any agent that embeds skill logic in its JD, and any
agent JD that is the only place where a reusable competency is recorded are all violations
of this boundary. Status: Accepted, 2026-05-23.

**Status**: Accepted
**Date**: 2026-05-23
**Deciders**: Peter (architecture), Harriet (agent management)

---

## Decision

Redline's skills system applies the Dependency Inversion Principle from layered software
architecture as its governing rule: skills are the stable inner core; agent manifests are
the volatile outer orchestration layer; all dependencies point inward (agents → skills,
never skills → agents).

---

## Status

Accepted — 2026-05-23.

---

## Context

### The problem this solves

The skills/agents boundary has an implicit rule scattered across three files
(`writing-skills`, `hiring-agent-management`, `skills-create`): "never name a skill after
an agent; skills must not reference agent names." This rule exists but has no formal
principle behind it, no name, and no vocabulary for the failure modes it prevents. Without
that vocabulary, agents cannot reason about *why* the rule exists, cannot detect novel
violations, and cannot apply the principle to new situations not covered by the existing
three files.

### Research basis

Queried the "Software Development Methodology & Engineering Organisation" NotebookLM
(ID: `cdb5e862-443d-4bb5-b24d-1393cacb5906`) on 2026-05-23. Key findings:

**Layered (Onion) Architecture**
The onion pattern organises a system into concentric layers. The innermost layer holds the
stable core — domain models and pure business logic. Outer layers deal with increasingly
volatile concerns: routing, UI, external integrations. Each layer has a single scoped
responsibility and encapsulates inner layers without exposing their internals.

The pattern separates *essential complexity* (what the system is actually solving) from
*accidental complexity* (databases, networks, frameworks — the machinery needed to run on a
computer). Accidental complexity belongs at the outer layers; the inner core must remain
free of it.

**Dependency Inversion Principle (DIP)**
DIP states:
1. High-level modules must not depend on the implementations of low-level modules. They
   should declare what they need (an abstract interface or contract), not how it is provided.
2. Both high-level and low-level modules should depend on abstractions (contracts), not
   on each other's concrete implementations.

This is the governing rule of the layered architecture. It is what makes the inner core
stable and the outer layer swappable.

**Direction of dependency vs direction of information flow**
These are opposite, and conflating them is the most common source of confusion:

| | Direction |
|---|---|
| **Information flow** | Inward (request flows in; response flows out) or top-down in a handoff chain |
| **Dependency (who knows about whom)** | Inward only — outer knows about inner; inner never knows about outer |

A repository adapter supplies data *to* the domain core (information flows inward) while
the domain core does *not depend on* the adapter's concrete implementation (the dependency
arrow points inward — domain → abstract interface, not domain → adapter).

**Failure modes when violated**

| Software failure mode | Formal name |
|---|---|
| Changing one thing forces changes everywhere | Shotgun Updates |
| A depends on B depends on A | Circular Dependency (fatal bootstrapping) |
| Technical failures bleed into business logic | Leaking Accidental Complexity |
| Can't unit-test the core; forced to rely on E2E tests only | Ice Cream Cone antipattern |
| No working layer boundaries; everything knows about everything | Big Ball of Mud |

### Mapping to the skills system

The software concepts map directly to Redline's skills system:

| Software concept | Skills system equivalent |
|---|---|
| Inner core (domain model) | **Skills** — stable, reusable, agent-agnostic competencies |
| Outer layer (application/infrastructure) | **Agent manifests** — orchestrators that wire skills together |
| Dependency direction | Agents depend on skills; skills never depend on agents |
| Information flow direction | Work flows L1 (Strategy) → L5 (Tools); the handoff chain |
| Essential complexity | The competency a skill teaches |
| Accidental complexity | Which agent invokes the skill, when, in what context |
| Abstract interface / contract | The skill's **Boundary Contract** (Applies To / Inputs / Outputs / Out of Scope) |
| Shotgun Updates | A skill named after an agent — renaming/restructuring that agent forces skill updates |
| Leaking Accidental Complexity | A skill that says "Kabilan should…" — agent-specific context bleeds into a reusable competency |
| Circular Dependency | Agent A's JD loads skill X; skill X references Agent A — neither can be defined independently |
| Big Ball of Mud | Skills that embed product decisions, agent names, or layer-crossing concerns |

---

## Options Considered

**Option A — Keep the rule implicit, scattered across three skill files**
The current state. The rule exists but has no name, no formal principle, and no shared
vocabulary for failure modes. Agents must encounter all three files to understand the
constraint; novel violations cannot be detected because the underlying principle is never
stated.

**Option B — Formalise DIP as the governing principle in a dedicated ADR (selected)**
Gives the rule a name, a principle, and a vocabulary for failure modes that agents can
apply to novel situations. `skills-architecture.md` references this ADR as the source of
truth. The three existing skill files retain their operational rules but no longer need to
each independently justify the same constraint.

**Option C — Encode as a pre-commit hook check**
Mechanically enforce "no agent names in skill files" via grep. Rejected: regex cannot
detect semantic violations (a skill that defers to an agent without naming them explicitly,
a skill whose Boundary Contract is written for a single agent rather than as a general
abstraction). The principle is too nuanced for mechanical enforcement at this stage.

---

## Decision Rationale

DIP is the correct formal name for the existing implicit rule because the skills/agents
relationship has the same structure as the domain/infrastructure relationship in layered
software:

- Skills are stable and change rarely (they encode engineering principles, DDD patterns,
  domain workflows). Agents change frequently (they are wired to personas, product
  decisions, and organisational structure, all of which evolve).
- The stable component should not know about the volatile component. Enforcing this in
  software eliminates shotgun updates and circular dependencies. The same is true here:
  a skill that references Kabilan by name must be updated every time Kabilan's role
  description changes, and cannot be used by any other agent — it has become an
  agent-specific document masquerading as a reusable skill.
- The Boundary Contract in a SKILL.md is the abstract interface: it declares inputs,
  outputs, and scope without encoding which agent calls it. This is the precise equivalent
  of a port in ports-and-adapters architecture.

Option B is preferred over Option A because an unnamed principle cannot be taught to new
agents, cannot be cited in code reviews, and cannot be extended to novel situations.
Option C is rejected because mechanical enforcement catches syntax violations but not
semantic ones; the principle must be understood, not just obeyed.

---

## Consequences

### Positive

- **Agents can reason about novel violations** using the DIP vocabulary, not just the
  three existing rules. A new agent encountering an unfamiliar situation can ask: "does
  this skill depend on an agent?" rather than pattern-matching against a list.
- **Boundary Contract becomes load-bearing**, not decorative. It is now the formal abstract
  interface between a skill and its callers. A skill without a Boundary Contract is an
  unpublished API — it cannot be depended upon safely.
- **`skills-architecture.md` has a formal principle it can reference** rather than
  describing the handoff chain empirically without explaining the dependency direction.
- **Failure mode vocabulary is shared**. Harriet's topology sync ceremony can cite
  "Leaking Accidental Complexity" or "Shotgun Update risk" when flagging skill violations,
  rather than describing each problem from scratch.

### Negative / risks

- **Retroactive audit required.** Existing skills were written before this principle was
  named. Many may contain subtle violations (agent-specific language in procedural steps,
  Boundary Contracts scoped to a single agent's workflow). A compliance audit of all 82+
  skills is a one-time task for Harriet's next topology sync.
- **Principle can be misapplied.** DIP in software allows inner layers to call *abstractions*
  of outer layers (via injected interfaces). In the skills system, the equivalent would be
  a skill that calls a *named tool* (e.g., `notebooklm-mcp`) but not a named agent. The
  distinction must be taught: tool skills in L5 are atomic bindings — referencing them
  from L4 skills is not a violation. Referencing an agent name is.

### Boundary rules (binding on all agents and skill authors)

1. A skill's name must never contain an agent name (personal name or role title).
2. A skill's content must never address or constrain a named agent. Use "this role", "the
   invoking agent", or "the operator" instead.
3. A skill's Boundary Contract must be written as a general abstract interface: inputs and
   outputs defined in terms of artifact types and file paths, not in terms of which agent
   will call it.
4. An agent manifest may reference any number of skills. A skill must never reference an
   agent manifest.
5. The direction of dependency (agent → skill) is always opposite to the direction of
   information flow (work flows L1 → L5 through the handoff chain).

---

## References

- Research source: NotebookLM "Software Development Methodology & Engineering Organisation"
  (ID: `cdb5e862-443d-4bb5-b24d-1393cacb5906`) — *Building Generative AI Services with
  FastAPI* (Iusztin, 2024) and *Modern Software Engineering* (Farley, 2021) and
  *Continuous Delivery* (Humble & Farley, 2010)
- `docs/architecture/skills-architecture.md` — six-layer stack and handoff chain
- ADR-008 — SkillX three-tier taxonomy and governance registry (skills as typed assets)
- `.agents/skills/writing-skills/SKILL.md` — operational rule: "Never name a skill after an agent"
- `.agents/skills/hiring-agent-management/SKILL.md` — operational rule: "Skills must never be named after an agent and must never reference a specific agent name inside their content"
- `.agents/skills/skills-create/SKILL.md` — operational rule: "NEVER name a skill after an agent"
- Dependency Inversion Principle — Robert C. Martin, *Clean Architecture* (2017)
- Ports and Adapters (Hexagonal Architecture) — Alistair Cockburn (2005)
