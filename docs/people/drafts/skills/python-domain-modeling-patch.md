# Patch: python-domain-modeling skill

> DRAFT -- pending user approval. Do not promote to production.

**Target file:** `.agents/skills/python-domain-modeling/SKILL.md`
**Session:** 2026-05-17 DDD Topology Sync
**Gaps addressed:** 1 (UL Stewardship), 6 (Model Evolution Governance)

---

## Changes

### 1. Update strategic DDD cross-reference (top of file)

Replace:
```markdown
This skill defines **tactical DDD** conventions: how to implement domain objects in
Python. For **strategic DDD** decisions (subdomain classification, bounded context
identification, EventStorming, context maps), use the `spec-kit` skill's plan phase
and `docs/architecture/domain-model.md`.
```

With:
```markdown
This skill defines **tactical DDD** conventions: how to implement domain objects in
Python. For **strategic DDD** decisions (subdomain classification, bounded context
identification, EventStorming, context maps, anti-corruption layers, model evolution
governance), use the `ddd-strategic` skill.
```

### 2. Add to Ubiquitous Language section (after existing content)

After the existing UL bullet points, add:

```markdown
- **Language change = code refactor.** When the team discovers a better domain term,
  the code changes immediately. Code and speech are the two enduring expressions of
  the model; documents go stale. This rule is non-negotiable -- see `ddd-strategic`
  skill, UL Rules.
```

### 3. Add Model Evolution Governance section (before "Pre-commit hook enforcement")

```markdown
## Model evolution governance

Domain models must evolve as understanding deepens. Follow these tactical rules when
changing domain objects:

- **Value Objects:** Replace entirely. Value objects are immutable -- create a new type
  rather than mutating an existing one.
- **Entities:** Update attributes while maintaining identity. Entity refactors must
  preserve the identity mechanism.
- **Aggregates:** Keep small. One transaction per aggregate. Use eventual consistency
  between aggregates.
- When a model change affects the Ubiquitous Language, update the UL table in
  `docs/architecture/domain-model.md` first, then refactor the code.
- When a model change affects multiple bounded contexts, update the Context Map
  (see `ddd-strategic` `procedures/context-mapping.md`) before propagating changes.

For the full strategic governance framework, use the `ddd-strategic` skill.
```
