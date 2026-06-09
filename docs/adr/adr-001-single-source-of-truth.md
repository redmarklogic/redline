# ADR-001: Single Source of Truth

## Summary

Redline adopts a Single Source of Truth (SSOT) principle: for each well-defined concern,
there is exactly one authoritative location, and everything else imports, derives, or
queries it (accepted 2026-05-23). This ADR is the foundational principle; every subsequent
decision that establishes or relocates an authoritative source is a derivative of this ADR
and must cite it. The hard constraint: duplication of an authoritative artifact — by
copy-paste, static snapshot, or parallel definition — is a defect, not a shortcut.

**Status**: Accepted
**Date**: 2026-05-23
**Deciders**: Peter (architecture), Ron (strategy), Mark (PM), Harriet (agent topology)

---

## Decision

This project adopts a Single Source of Truth for each concern listed in the table below.
For each concern, exactly one authoritative location exists. All other locations import,
derive, or query from that location. Nothing copies it.

---

## Context

Software systems accumulate duplication silently. The same fact — a constant, a schema, a
business rule, a design token, a configuration value — appears in multiple places. Over
time those copies drift. The downstream effects span architecture, UX, and engineering
organisation:

- **Configuration drift**: environments deviate from one another; deployment failures
  emerge on release day, not in testing. (*Continuous Delivery*)
- **Connascence of Meaning**: hard-coded magic values scatter the same concept across
  modules; one change requires hunting every copy. (*Fundamentals of Software Architecture*)
- **Anemic domain models**: business logic leaks out of domain objects into UI and
  persistence layers, making the authoritative rule impossible to locate. In Redline's
  context, geotechnical rules leaking into the report generation layer are the canonical
  instance of this failure. (*Domain-Driven Design*)
- **Visual noise**: per-component style overrides in generated DOCX output diverge from
  the authoritative template; every document looks slightly different.
- **Lost research**: domain knowledge and experiment results re-derived from scratch
  because findings were never centralised.
- **Fragmented agent topology**: agent responsibilities described inconsistently across
  skill files, chat threads, and ADRs; no single place answers "who owns what?".

A SSOT principle declares: for each well-defined concern, there is exactly one
authoritative location. Everything else imports, derives, or queries it.

---

## Concerns and Their Authoritative Sources

*This table is the index. Each row either resolves the concern directly or points to a
derivative ADR that records the specific decision. Extend this table whenever a new
concern acquires an authoritative location.*

| Concern | Authoritative Source | Prohibited Pattern | Derivative ADR |
|---------|---------------------|-------------------|----------------|
| **DOCX generation engine and facade protocol** | `DocumentFacade` protocol in `src/rl/` | Application code importing `python-docx` directly; facade bypassed for "quick" operations | ADR-002 |
| **Report section structures and heading conventions** | Frozen `ReportDefinition` Pydantic objects in `src/rl/` | Hard-coded section strings in builder functions; per-jurisdiction constant sets; branching logic on jurisdiction/report type | ADR-003 |
| **DocumentFacade method signatures** | Primitives-only protocol (`str`, `int`, `list[str]`) | Domain objects crossing the facade boundary; Pydantic models in facade signatures | ADR-004 |
| **DOCX output visual formatting (styles, typography, spacing)** | Styles-only DOCX template (`src/rl/` templates); template is the style source, content cleared and rebuilt | Per-section style overrides in generation code; style values hard-coded in python-docx calls | ADR-005 |
| **NZ/AU standards citations and applicability mappings** | Standards Knowledge Store — citation references only, never full text | Full proprietary standards text stored anywhere in the system; public-facing query interface | ADR-006 |
| **Geotechnical report section taxonomy** | `docs/knowledge/geotechnical/report-writing/checklist-taxonomy-cross-jurisdiction.md` | Per-component private section taxonomies; section names redefined in each consumer (Skeleton Generator, Checklist Engine, Pre-Review Engine) | ADR-007 |
| **Standards nominations for skeleton generation** | Human-curated Standards Registry (deterministic lookup) | LLM inference of applicable standards; hybrid fallback to LLM for unregistered project types | ADR-008 |
| **Skill classification and ownership** | `skills-lock.json` governance registry (`tier`, `owner_agent`, `status` fields) | Skill ownership implied by `AGENTS.md` only (human-readable, not machine-parseable); orphan skills undetectable | ADR-009 |
| **Notebook-agent access mapping** | `register.json` (`owner` + `consumers` fields in `.agents/skills/redline-research/register.json`) | Notebook ownership or consumer lists stated in agent JDs or `docs/people/agent-register.md`; access grants duplicated outside the register | |
| **Skill layer assignment (L0-L9)** | `docs/architecture/skills-taxonomy.md` (Layer Definitions section) | Layer assignments stated in any other document (`skills-architecture.md`, `skills-system.md`, `AGENTS.md`, inline in skill files) | ADR-009 |
| **Skill layer field in machine-readable registry** | `skills-lock.json` (`layer` field, derived from `skills-taxonomy.md` via `hooks/sync-layer-to-lock.py`) | Setting `layer` in the lock file without first updating `skills-taxonomy.md`; `layer` diverging from taxonomy | ADR-009 |
| **Layer reclassification governance** | Owner-based sign-off: any change to a skill's `layer` field requires approval from all agents listed in that skill's `owner_agent` before merge | Reclassifying a skill's layer without owner review; using a layer-range blanket trigger instead of ownership |  |
| **Skills narrative and onboarding** | `docs/knowledge/software-engineering/skills-system.md` (examples, analogies, worked flows — no skill enumeration by layer) | Enumerating skills by layer or tier in the narrative doc; re-stating layer assignments outside the taxonomy |  |
| **Agent invocation manifests (which skills each agent invokes)** | `AGENTS.md` (consumer of taxonomy and lock file — read-only for layer/tier concerns) | Layer assignments or tier classifications written inline in `AGENTS.md`; `AGENTS.md` treated as authoritative for layer/tier |  |
| **Business rules and domain logic** | Domain layer entities and value objects in `src/rl/domain/` | Logic duplicated in UI, persistence, report generation, or API layers |  |
| **Domain layer architecture boundaries** | Import-linter contracts in `pyproject.toml [tool.importlinter]` | Layer violations detected at runtime; manual import reviews; architecture enforced by convention only |  |
| **Ubiquitous Language (UL) glossary** | UL table in `docs/architecture/domain-model.md` | Domain terms used inconsistently across code, docs, and conversation; terminology divergence between domain layer and UI copy |  |
| **Pandera DataFrameModel schema contracts** | Schema modules in `src/rl/schemas/` co-located with the code that owns the data | Schema redefined per reader function; free-form DataFrame manipulation without a validated schema; schema duplicated in test fixtures |  |
| **Constants and magic values** | Named constants in `src/rl/domain/` | Inline literals; copies of domain constants in tests or scripts; test fixtures that redefine values instead of importing them |  |
| **Dependency versions** | `uv.lock` lockfile (One-Version Rule) | Multiple versions of the same library in flight; dependency pinning scattered across files |  |
| **Architecture decisions** | Architecture Decision Records in `docs/adr/` | Decisions communicated only in chat or email; decisions repeated in multiple documents |  |
| **External HTTP API conventions (current operational rules)** | `docs/architecture/api/` — HTTP API standard in force (`http-api-standard.md`); ADR-018 owns the decision+rationale | Clause text copied into the ADR or into endpoint code; per-endpoint divergence from the standard; status-code/error-envelope/auth rules redefined per route | ADR-018 |
| **System behaviour (what the system does)** | SpecKit acceptance criteria (`specs/`) + automated test suite (executable documentation) | Prose specs that can silently diverge from implementation; acceptance criteria living only in PRDs |  |
| **Strategic bets and OKRs** | `docs/product/strategy/strategic-bets.md` and `docs/product/strategy/okrs/` | Bets communicated in chat; agents operating without knowing the active bets; orphan OKRs without a parent bet |  |
| **Positioning and ICP (Ideal Customer Profile)** | `docs/product/strategy/positioning.md` | Positioning redefined per marketing asset; agents inventing ICP language without consulting the canonical file |  |
| **Feature hypotheses** | `docs/product/hypotheses/` | Hypotheses embedded only inside PRDs; hypotheses in chat threads without a formal record |  |
| **Customer personas** | `docs/product/personas/` (co-owned: Mark authors, Ron validates against positioning) | Persona attributes scattered across PRDs, campaign briefs, and design specs |  |
| **Brand voice and tone** | Brand voice document in `docs/product/marketing/` | Tone described differently in each content brief; copy written without consulting the canonical guide |  |
| **Design specifications per product surface** | Design spec documents in `docs/product/design/` — one spec per surface (web, Word document, Word taskpane, email agent) | Design decisions communicated in chat; implementation proceeding without a design spec |  |
| **Agent identity, file authority, and role boundaries** | `.github/agents/*.agent.md` (canonical, machine-readable) + `AGENTS.md` (human-readable manifest) | Role names embedded in reusable skill documents; agent responsibilities defined in chat and never formalised |  |
| **Org chart and agent register** | `docs/people/agent-register.md` + `docs/people/org-chart.md` | Team topology described in chat history; register not updated after a hire or topology change |  |
| **Geotechnical domain knowledge (facts, standards, field practice)** | Knowledge documents in `docs/knowledge/geotechnical/`, grounded in NotebookLM notebooks | Domain facts inferred from LLM output without notebook citation; conflicting sources silently resolved |  |
| **Research and product experiment results** | `docs/research/` (exported findings) + NotebookLM notebooks (live research store) | Per-team write-ups in personal drives; experiments re-run without consulting prior findings |  |
| **Documentation** | Version-controlled alongside the code or concern it documents, with clear ownership | Copied into chat threads, slide decks, or email that drift from the source |  |

---

## Options Considered

- **Option A — Tolerate duplication with manual synchronisation**: Copies are acceptable
  if kept in sync. Rejected: synchronisation discipline degrades under deadline pressure;
  the defect is invisible until it bites.

- **Option B — Single Source of Truth with derivation (chosen)**: Authoritative
  definitions exist in one place; everything else derives from or imports that place.
  Changes propagate automatically.

- **Option C — Federated ownership with contracts**: Multiple owners publish contracts
  (APIs, schemas, events) that others consume. Partially accepted: this is the correct
  pattern for *inter-bounded-context* boundaries (Data Sovereignty per *Software
  Architecture: The Hard Parts*). Within a single bounded context, it reintroduces
  duplication.

---

## Decision Rationale

Option B with the Option C carve-out for inter-context boundaries because:

1. **Structural impossibility of drift**: when a change to an authoritative source
   propagates everywhere at once, drift is architecturally impossible rather than
   just discouraged.
2. **Single point of review**: reviewers have exactly one place to look for any concern.
3. **Documentation as live contract**: if a constant is wrong in the docs, it is wrong
   in the code too — inconsistency becomes immediately visible.
4. **Eliminates a class of test**: constant-value assertion tests and schema snapshot
   tests add maintenance noise without behavioural signal; SSOT removes the need for them.
5. **Founder-stage economics**: at Redline's current stage, the cost of hunting down
   duplicate copies is paid by a single developer. SSOT is not a nice-to-have; it is a
   productivity constraint.

---

## Consequences

**Positive**
- A change to an authoritative source propagates everywhere at once.
- Reviewers have exactly one place to look to understand a concern.
- The table above is the index; any agent can route to the correct source without
  searching the codebase.
- Derivative ADRs gain a clear parent — they record *where* the SSOT lives for a
  specific concern, not *why* SSOT matters.

**Negative**
- Consumers must import or query the authoritative source rather than embed their own
  copy. This requires a working dependency on the owning module.
- Documentation that renders values (tables in published docs) must be generated rather
  than hand-typed, requiring a build step.
- Adding a new concern to the table requires an explicit decision. This is a feature,
  not a cost: undecided concerns are visible as gaps.

---

## Enforcement Mechanisms

1. **Linting / static checks** — Ruff rules and import-linter contracts prevent
   definitions from leaking across layer boundaries.
2. **Pre-commit hooks** — `hooks/check-banned-words.py` rejects literal copies of
   authoritative values in prohibited locations; `hooks/check-skills-documented.py`
   enforces skill registry coverage; `hooks/fix-doc-sync.py` flags documentation drift.
3. **Generated documentation** — rendered at build time by importing the authoritative
   source; static copies are never committed.
4. **CI gate** — schema validation, import-linter, and contract tests run on every PR.
5. **ADR review** — any new concern that requires an authoritative location is recorded
   as a derivative ADR before implementation.
6. **Quarterly Agent Topology Sync** (Harriet-owned) — the periodic governance ceremony
   that reviews agent-topology SSOTs which static checks cannot validate.

---

## References

- *Clean Architecture* — R. Martin (2017): domain layer isolation, SRP, CCP,
  Connascence of Meaning
- *Domain-Driven Design* — E. Evans (2003): Bounded Contexts, Aggregates,
  Repositories, Ubiquitous Language
- *Fundamentals of Software Architecture* — Ford & Richards (2020): connascence
  taxonomy, Context Objects
- *A Philosophy of Software Design* — Ousterhout (2018): information leakage,
  document-once principle
- *Software Architecture: The Hard Parts* — Ford et al.: Data Sovereignty pattern
- *Continuous Delivery* — Humble & Farley (2010): everything in version control,
  DRY config, configuration drift
- *Software Engineering at Google* — Winters et al. (2020): canonical documents,
  One-Version Rule, version skew failure modes
- *Shape Up* — Singer (2019): Pitch as the canonical scope-definition artifact;
  shaping decisions as architectural decisions
- ADR-002 through ADR-009 — derivative decisions, each establishing the authoritative
  location for a specific concern within this project
