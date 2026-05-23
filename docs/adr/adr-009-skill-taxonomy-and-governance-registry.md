# ADR-009: SkillX Three-Tier Taxonomy and Governance Registry Schema

## Summary

Redline adopts a modified SkillX three-tier taxonomy (Atomic / Functional / Planning) as the canonical classification model for all skills in `.agents/skills/`, and evolves `skills-lock.json` to a governance registry by adding three required fields: `tier`, `owner_agent`, and `status` (accepted 2026-05-22). With 82 skills and no ownership or classification metadata, orphan detection is impossible and context-bloat cannot be reasoned about systematically; this ADR installs the minimum metadata needed to make the skill inventory governable without adding tooling overhead that would kill velocity at Redline's current stage. The hard constraint: any skill that lacks `owner_agent` in the registry is treated as an orphan and is a deletion candidate at the next Agent Topology Sync.

**Status**: Accepted  
**Date**: 2026-05-22  
**Deciders**: Peter (architecture), Harriet (agent management)

---

## Context

### Current state

`skills-lock.json` (version 1) records three fields per skill: `source`, `sourceType`, and `computedHash`. It was designed for integrity checking (detecting upstream changes to vendored skills), not governance. It has no classification, ownership, or lifecycle metadata.

The 82 skills in `.agents/skills/` are:
- Referenced in `AGENTS.md` agent manifests (human-readable, not machine-parseable)
- Protected by a pre-commit hook (`check-skills-documented.py`) that verifies coverage
- Not classified by capability type, ownership, or lifecycle status

The practical consequences of this gap are:

1. **Orphan detection is manual.** There is no automated way to identify skills that belong to no agent. The SkillX audit flagged 37 merge candidates and 28 overlap flags, but without an ownership field these cannot be triaged systematically.
2. **Context-bloat cannot be measured.** Without tier classification, it is not possible to distinguish expensive planning-tier skills (which carry full coordination logic) from cheap atomic-tier skills (single-tool bindings). All skills are loaded identically.
3. **Deprecation is invisible.** A skill can be abandoned without the registry reflecting it, causing future agents to load dead skills.

### Research basis

Linda commissioned deep research (NotebookLM ID: `1bdfb971-e39d-43cd-ae87-778720d940fb`) on reducing skill/prompt bloat. The key finding relevant to classification is arXiv 2604.04804's three-tier SkillX taxonomy:

- **Atomic** ($S_{atomic}$): Single-tool or single-API binding with a semantic specification and usage constraints. Examples in Redline: `miro-mcp`, `notebooklm-mcp`, `python-usethis`.
- **Functional** ($S_{func}$): Multi-step macro-operation composing multiple tool calls or agent invocations to accomplish a named workflow. Examples: `python-data-ingestion`, `git-push-batched`, `spec-kit`.
- **Planning** ($S_{plan}$): Coordination logic, step dependencies, conditional branching, or cross-agent orchestration. Examples: `dispatching-parallel-agents`, `subagent-driven-development`, `ceremony-agent-topology-sync`.

The research also documented progressive disclosure (demand-paging) achieving 93% context reduction in production systems. VS Code's deferred-tool loading already implements demand-paging for Redline's skills; the taxonomy supports that mechanism but does not require rebuilding it.

### Redline stage constraint

Redline is a single-founder, AI-agent-developed startup in early phase. The Surviving the Round test applies:

- **Short runway (3–6 months):** Need: make the 37 merge candidates and 28 overlap flags actionable before the next topology sync. Minimum viable governance. No new tooling unless it can be built in a pre-commit hook.
- **Long runway (2+ years):** Need: automated usage tracking, last-used-date, context-budget reporting. This is theoretical at the current stage and is explicitly deferred.

Any governance mechanism that adds more than one mandatory step to skill creation is too expensive for the current phase.

---

## Decision 1: Adopt the SkillX Three-Tier Taxonomy as Redline's Canonical Skill Classification

**Redline adopts the Atomic / Functional / Planning taxonomy from arXiv 2604.04804 as the canonical classification model for skills in `.agents/skills/`, with the Redline-specific modification that tier is declared in `skills-lock.json` rather than in the SKILL.md frontmatter.**

---

## Decision 2: Evolve `skills-lock.json` to a Governance Registry

**`skills-lock.json` is promoted from an integrity-check manifest to a governance registry by adding three required fields per skill entry: `tier`, `owner_agent`, and `status`. The schema version increments to `2`.**

**Minimal viable schema (version 2):**

```json
{
  "version": 2,
  "skills": {
    "<skill-name>": {
      "source": "...",
      "sourceType": "...",
      "computedHash": "...",
      "tier": "atomic | functional | planning",
      "owner_agent": ["<agent-slug>"],
      "status": "active | draft | deprecated"
    }
  }
}
```

Field definitions:

| Field | Type | Rules |
|---|---|---|
| `tier` | enum string | Required. One of: `atomic`, `functional`, `planning`. |
| `owner_agent` | array of strings | Required, non-empty. Agent slugs (e.g. `kabilan`, `peter`). A skill with an empty array is an orphan. |
| `status` | enum string | Required. One of: `active`, `draft`, `deprecated`. |

**Explicitly deferred** (not in scope for version 2): `last_used_date`, `version`, `context_tokens`, `merge_target`. These are long-runway governance fields. Adding them now would be speculative engineering.

---

## Options Considered

### Decision 1 — Taxonomy options

- **Option A — Adopt SkillX taxonomy as-is with tier in SKILL.md frontmatter:** Keeps governance metadata co-located with skill content. Rejected because SKILL.md frontmatter is content, not registry metadata; mixing them creates two sources of truth. The `check-skills-documented` hook already operates on SKILL.md; adding a registry field there would couple content integrity checks with governance checks.
- **Option B — Adopt SkillX taxonomy with tier in `skills-lock.json` (selected):** Separates content from registry metadata. The lock file is already the machine-readable single source of truth for skill identity.
- **Option C — Reject taxonomy; use ad-hoc labels:** No benefit over current state. Orphan detection and context-budget reasoning both require a stable, machine-parseable classification.
- **Option D — Defer taxonomy pending audit completion:** Rejected. The audit (37 merge candidates, 28 overlap flags) cannot be actioned without a classification framework. Deferring taxonomy defers the audit indefinitely.

### Decision 2 — Registry schema options

- **Option A — Separate registry file (e.g. `skills-registry.json`):** Introduces a second file that must stay in sync with `skills-lock.json`. Two sources of truth for skill metadata violates the single-source principle without compensating benefit.
- **Option B — Use `AGENTS.md` as the registry:** `AGENTS.md` is human-readable and not machine-parseable at the skill level. Using it as a registry would require parsing free-form Markdown tables, which is fragile. It is the correct format for agent-readable manifests; it is the wrong format for programmatic governance checks.
- **Option C — Evolve `skills-lock.json` with three required fields (selected):** Minimal change to an existing, already-trusted file. Pre-commit hooks can validate field presence without new tooling.
- **Option D — Add all seven SkillX registry fields (including `last_used_date`, `version`, `context_tokens`):** Over-engineering for the current stage. Usage tracking requires instrumentation that does not exist. Adding fields that cannot be populated produces a corrupt registry from day one.

---

## Decision Rationale

### Why this taxonomy, why now

The three-tier taxonomy maps cleanly onto Redline's existing skill inventory without requiring reclassification of content. The boundary between tiers is semantically stable: Atomic binds one tool, Functional chains multiple tools into a named workflow, Planning coordinates agents or step-dependencies. This stability matters because Harriet's topology sync ceremony can apply the classification consistently without subjective judgement calls.

The modification — tier in the lock file, not in SKILL.md frontmatter — preserves the integrity of content files. SKILL.md is instructional prose, not metadata. Adding a frontmatter key to 82 files creates a maintenance burden and a new category of pre-commit failure (malformed frontmatter), without adding information that is not already captured in the lock file.

### Why these three registry fields, in this order

`owner_agent` is the highest-priority field because it directly enables the orphan detection that the audit requires. Without it, the 37 merge candidates and 28 overlap flags cannot be assigned to any agent for triage. It is deliberately an array: shared skills (e.g. `pm-personas`, used by Mark and Ron) exist and should not be forced into artificial single-ownership.

`status` is the second-highest priority because it makes deprecation visible. A skill that has been superseded but is still `active` in the registry will be loaded by agents indefinitely. `draft` signals skills under development that should not yet appear in production agent manifests.

`tier` is the third field because it enables context-budget reasoning and the demand-paging optimisation already present in VS Code's deferred-tool loading. It is the only field that requires domain judgement (what tier is this skill?) rather than assignment (who owns it?).

### Why `last_used_date` and `version` are deferred

`last_used_date` requires instrumentation at skill invocation time. Redline has no instrumentation layer. Populating this field manually defeats its purpose; populating it incorrectly makes orphan detection less reliable, not more. It belongs in a version-3 registry.

`version` is unnecessary given that Git is already the version history for SKILL.md content. Adding a monotonically-increasing version field adds a mandatory bump step to every skill edit, which increases friction without adding information that `computedHash` does not already provide.

---

## Consequences

### Positive

- **Orphan detection becomes automated.** The pre-commit hook `check-skills-documented.py` (or a new companion hook) can flag any skill where `owner_agent` is an empty array. This makes the 37 merge candidates actionable at the next topology sync.
- **Context-budget reasoning becomes possible.** Planning-tier skills carry more context weight than Atomic-tier skills. Once classified, Harriet can report on context-budget per agent.
- **Deprecation is visible.** Setting `status: deprecated` in the registry is the single required action when a skill is retired. No other artefact needs to change until the deletion decision is made.
- **AGENTS.md and the registry serve different purposes without conflict.** AGENTS.md remains the human-readable agent manifest. The registry is the machine-readable governance layer. They are complementary, not competing.

### Negative / risks

- **Classification ambiguity for multi-concern skills.** Skills like `python-data-ingestion` (chains tool calls and imposes Pandera schema contracts) sit ambiguously between Atomic and Functional. Misclassification does not break anything but degrades the taxonomy's decision value. Harriet should apply a default rule: if in doubt, classify as Functional.
- **Schema migration burden.** Upgrading 82 entries in `skills-lock.json` from version 1 to version 2 is a one-time manual effort. Until the migration is complete, the registry will contain a mix of v1 and v2 entries, which pre-commit hooks must tolerate during the transition window.
- **Owner_agent drift vs AGENTS.md.** If `owner_agent` entries in the registry diverge from the skills tables in `AGENTS.md`, the registry becomes unreliable. This is the primary ongoing maintenance risk. Mitigation: extend the pre-commit hook to cross-check both sources.

### Explicitly out of scope

- Progressive disclosure / demand-paging implementation changes. VS Code already implements this; no changes required.
- Merging the 37 candidate skills. That is a separate task for Harriet's topology sync ceremony.
- Automated usage tracking. Deferred to version 3.

---

## References

- ADR-001: Single Source of Truth — foundational SSOT principle; this ADR records the authoritative location for skill classification and ownership
- arXiv 2604.04804 — SkillX three-tier taxonomy (Atomic / Functional / Planning), source for Decision 1
- Research notebook: NotebookLM ID `1bdfb971-e39d-43cd-ae87-778720d940fb` — Linda's skill-bloat deep research
- `docs/architecture/skills-architecture.md` — existing architecture constraints on skill structure
- `hooks/check-skills-documented.py` — pre-commit hook that validates skill documentation coverage (extension target)
- `AGENTS.md` — agent skill manifests (human-readable canonical source, complementary to registry)
- ADR-007 — shared taxonomy for skeleton/checklist pre-review (pattern for shared-taxonomy decisions at Redline)
- `.agents/skills/hiring-agent-management/SKILL.md` — Harriet's agent topology sync procedure (governance consumer of this ADR)
