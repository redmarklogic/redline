# Patch: engineering-architecture skill

> DRAFT -- pending user approval. Do not promote to production.

**Target file:** `.agents/skills/engineering-architecture/SKILL.md`
**Session:** 2026-05-17 DDD Topology Sync
**Gaps addressed:** 2 (Context Mapping), 3 (Subdomain Classification), 4 (EventStorming), 5 (ACL)

---

## Changes

### 1. Add YAML frontmatter

The current file has no YAML frontmatter. Add at the top:

```yaml
---
name: engineering-architecture
description: Use when making system-level design decisions, writing ADRs, defining component boundaries, or reviewing architectural compliance of shaped work and SpecKit output.
---
```

### 2. Add Boundary Contract (after Purpose section)

```markdown
## Boundary Contract

### Applies To
- System-level design decisions (component boundaries, service interfaces, API design)
- ADR writing and maintenance
- Technology selection within Redline constraints
- Architectural compliance review of SpecKit output (Touch 2)

### Produces
- ADRs in `docs/adr/`
- Architecture documents in `docs/architecture/`
- Shaped Pitches in `specs/shaped/`
- Architectural constraint tests

### Does Not Cover
- Strategic DDD decisions (subdomain classification, context mapping, EventStorming) -- use `ddd-strategic`
- Tactical DDD implementation (Pydantic, value objects) -- use `python-domain-modeling`
- Evaluation architecture (rubric design, LLM-as-judge) -- use `evaluation-architecture`
```

### 3. Add cross-references to ddd-strategic (after Grounding Sources)

```markdown
## Strategic DDD

For strategic DDD decisions that inform architectural boundaries, use the `ddd-strategic` skill:

- **Subdomain classification** determines investment level per component -- `ddd-strategic` `procedures/subdomain-classification.md`
- **Context mapping** reveals integration relationships between components -- `ddd-strategic` `procedures/context-mapping.md`
- **EventStorming** discovers bounded context boundaries from domain events -- `ddd-strategic` `procedures/eventstorming.md`
- **ACL pattern** protects Core domains from upstream corruption -- `ddd-strategic` ACL Pattern section

These feed directly into ADR decisions and component boundary design.
```

### 4. Replace Status section

Replace:
```markdown
## Status

**Pending notebook grounding.** This skill requires queries to the Software Development Methodology & Engineering Organisation notebook and the Software Architecture & Domain-Driven Design notebook before the content can be fully elaborated. The structure above defines what the skill must cover; the notebook grounding will provide the specific principles, patterns, and anti-patterns.
```

With:
```markdown
## Status

**Partially grounded.** Strategic DDD content (Gaps 1-6) has been extracted from the Software Architecture & DDD notebook (`c04e18d3-e1e6-47f0-879a-d0e4a65adcb0`) and placed in the `ddd-strategic` skill. System-level architecture content (Team Topologies fracture planes, Accelerate loosely coupled architecture, component boundary principles) still requires notebook grounding from the Software Development Methodology & Engineering Organisation notebook (`cdb5e862-443d-4bb5-b24d-1393cacb5906`).
```

### 5. Remove "Who Uses This Skill" section

Skills must never reference which agent uses them (skill naming rules). Delete the entire section:
```markdown
## Who Uses This Skill

Peter (primary). Engineering agents may reference for architectural context.
```
