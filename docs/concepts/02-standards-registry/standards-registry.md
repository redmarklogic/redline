# Concept: Standards Registry and Category-Based Rule Dispatch

> **Audience**: Product owners, automation engineers, and domain engineers.
> This document describes a structured registry of engineering standards
> and linting rules, and a dispatch mechanism that feeds the right rules
> to the right pipeline step at the right time.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Vision](#2-vision)
3. [Core Design: Category-Based Rule Dispatch](#3-core-design-category-based-rule-dispatch)
4. [Rule Structure](#4-rule-structure)
5. [Dispatch Mechanism](#5-dispatch-mechanism)
6. [Rule Extraction Pipeline](#6-rule-extraction-pipeline)
7. [Bootstrap Strategy](#7-bootstrap-strategy)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [Architecture Overview](#9-architecture-overview)
10. [Relationship to Other Concepts](#10-relationship-to-other-concepts)
11. [Open Questions](#11-open-questions)

---

## 1. Problem Statement

Engineering reports must comply with a dense web of standards -- national
codes (NZS 3604, NZS 1170.5), local council district plans, and
industry guidelines. Today, knowledge of which standards apply to which
report section lives entirely in the engineer's head. This creates
several problems:

- **Inconsistency**: Different authors apply different standards to
  the same section type.
- **Omission risk**: A relevant standard is missed, creating liability
  exposure.
- **LLM context flooding**: Dumping all standards into an LLM prompt
  produces unfocused output. Semantic search over standards returns
  fuzzy matches when exact rule retrieval is needed.

---

## 2. Vision

A structured, queryable registry of engineering rules extracted from
standards documents. When any pipeline step (e.g., the Skeleton Generator)
processes a specific report section, it queries the registry and receives
a focused batch of 5-15 explicitly mapped rules for that section.

This provides the **precision of modular skills** without the
**unreliability of semantic search**.

### Key properties

- **Deterministic dispatch**: The pipeline knows which rules to load for
  "Foundation Assessment" without asking an LLM to figure it out.
- **Auditable**: Every rule has a traceable source reference (standard,
  section, page).
- **Human-validated**: Rules are reviewed by engineers before entering
  the registry. AI-extracted rules are flagged until validated.
- **Incrementally buildable**: Start with 50-100 manually curated rules;
  scale with automated extraction later.

---

## 3. Core Design: Category-Based Rule Dispatch

### The problem with semantic search

Engineering standards are **prescriptive and discrete**. "NZS 3604
Section 3.1.2 requires X" is a rule, not a vibe. Semantic search returns
ranked results by similarity, but:

- Similar-sounding clauses from different standards may contradict
  each other or apply to different contexts.
- The LLM cannot distinguish between "relevant" and "approximately
  relevant" without domain context.
- Results are non-deterministic -- the same query may return different
  rules on different runs.

### The dispatch model

```
Pipeline Step                   Registry Query              Rules Injected
--------------                  ---------------             ---------------
Section 2.4: Seismic Hazard --> category="seismic_hazard"   --> 8 rules
                                project_type="residential"
                                jurisdiction="NZ"

Section 3.1: Foundation     --> category="foundations"      --> 12 rules
  Options                       project_type="residential"
                                jurisdiction="NZ"
                                soil_conditions=["clay"]
```

Each pipeline invocation receives **only the rules that apply** to the
section it is currently processing. The LLM's context is focused,
not flooded.

---

## 4. Rule Structure

Each rule in the registry has a two-tier structure:

### Tier 1: The rule itself

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `rule_id` | string | Unique identifier | `NZS3604-3.1.2-bearing` |
| `statement` | string | Concise, actionable rule text | "Bearing capacity for shallow foundations on clay must be determined per NZS 3604 Section 3.1.2, with minimum allowable bearing pressure of 100 kPa for Category A sites." |
| `category` | string | Report section category this rule maps to | `foundations` |
| `source_standard` | string | Standard name and version | "NZS 3604:2011" |
| `source_section` | string | Section/clause number | "3.1.2" |
| `source_page` | string (optional) | Page number for quick lookup | "42" |

### Tier 2: Applicability conditions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `project_types` | list[string] | Which project types this rule applies to | `["residential", "light_commercial"]` |
| `jurisdictions` | list[string] | Geographic applicability | `["NZ"]` |
| `infrastructure_types` | list[string] (optional) | Infrastructure categories | `["buildings", "retaining_walls"]` |
| `soil_conditions` | list[string] (optional) | Soil types where the rule is relevant | `["clay", "silt"]` |
| `hazard_types` | list[string] (optional) | Relevant hazards | `["liquefaction", "slope_instability"]` |

### Tier 3: Provenance

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `extraction_method` | string | How the rule was added | `"manual"` or `"ai_extracted"` |
| `validated_by` | string (optional) | Engineer who validated the rule | `"J. Smith, CPEng"` |
| `validated_date` | date (optional) | When the rule was validated | `2026-03-15` |
| `confidence` | string | Trust level | `"validated"` or `"ai_extracted_unvalidated"` |

### Display behaviour

- **Validated rules** appear in the skeleton as direct references:
  *"Per NZS 1170.5 Cl. 3.1.3, determine site subsoil class."*
- **Unvalidated (AI-extracted) rules** appear with a caveat:
  *"[AI-extracted -- verify against source] Per NZS 1170.5 Cl. 3.1.3,
  determine site subsoil class."*

---

## 5. Dispatch Mechanism

### Query interface

```
query_rules(
    category: str,              # e.g., "seismic_hazard"
    project_type: str,          # e.g., "residential"
    jurisdiction: str,          # e.g., "NZ"
    infrastructure_type: str?,  # e.g., "buildings"
    soil_conditions: list?,     # e.g., ["clay", "silt"]
    hazard_types: list?,        # e.g., ["liquefaction"]
) -> list[Rule]                 # 5-15 rules, ordered by relevance
```

### Category taxonomy (initial, for GIR)

| Category | Maps to GIR sections | Example standards |
|----------|---------------------|-------------------|
| `scope_and_introduction` | 1.1-1.3 | LOE/RFP terms |
| `geology_and_faulting` | 2.1, 2.X | GNS Active Faults Database, NZGS guidelines |
| `ground_model` | 2.2 | NZGS Module 2, Eurocode 7 |
| `groundwater` | 2.3 | Regional council guidelines |
| `seismic_hazard` | 2.4 | NZS 1170.5 |
| `liquefaction` | 2.X | MBIE guidance, Boulanger & Idriss |
| `slope_stability` | 2.X | NZGS Module 4, GeoStudio guidelines |
| `foundations` | 3.1-3.2 | NZS 3604, NZS 3603, AS 2159 |
| `ground_improvement` | 3.X | NZGS guidelines |
| `residual_risk` | 4 | IPENZ/Engineering NZ practice notes |
| `applicability` | 6 | Company style guide, legal |
| `reporting_format` | All | Company Style Reference Guide |

---

## 6. Rule Extraction Pipeline

This is the **scaling mechanism** -- not required for MVP but designed
as a separate tool/agent for future use.

### Process

```
  PDF Standard
       |
       v
  +----+-----+
  | PDF Parser|  (extract text, tables, structure)
  +----+-----+
       |
       v
  +----+------+
  | LLM Agent |  (identify discrete rules, classify by category,
  |           |   extract applicability conditions)
  +----+------+
       |
       v
  +----+-------+
  | Human      |  (engineer reviews extracted rules,
  | Review     |   validates or corrects, marks as validated)
  +----+-------+
       |
       v
  +----+-------+
  | Registry   |  (rule is added with provenance metadata)
  +----+-------+
```

### Design principles

- **Extraction and registry are decoupled.** The extraction tool is a
  one-time (or infrequent) operation. The registry is the runtime artifact.
- **Human-in-the-loop is mandatory.** Getting a rule wrong has liability
  implications. AI-extracted rules must be reviewed before being marked
  as validated.
- **Batch extraction.** Process one standard at a time. An engineer
  familiar with that standard reviews the output. Do not mix standards
  in a single extraction session.

---

## 7. Bootstrap Strategy

### Phase 1: Manual curation (MVP)

Manually curate 50-100 rules for the GIR document type from the most
commonly referenced standards:

| Standard | Expected rule count | Priority |
|----------|-------------------|----------|
| NZS 3604:2011 (Timber-framed buildings) | 15-20 | High |
| NZS 1170.5 (Earthquake actions) | 10-15 | High |
| Relevant council district plan (start with one council) | 10-15 | High |
| NZGS guidelines (Modules 1-4) | 10-15 | High |
| Company Style Reference Guide | 10-15 | High |

This gets a working registry in **days, not months**.

### Phase 2: Assisted extraction

Build the extraction pipeline (Section 6) and use it to process
additional standards. Each batch is human-reviewed before entering
the registry.

### Phase 3: Coverage expansion

Extend to other document types (GFR, desktop study), jurisdictions
(Australian standards, Eurocodes), and project types (infrastructure,
commercial).

---

## 8. Acceptance Criteria

| #   | Criterion | Verification |
|-----|-----------|-------------|
| AC1 | Every rule has a traceable source (standard, section, page). | Audit a random sample of rules. |
| AC2 | Rules are dispatched by category, not by semantic search. Dispatch is deterministic. | Same query returns the same rules every time. |
| AC3 | Each dispatch returns 5-15 rules -- focused enough for an LLM context window, comprehensive enough for the section. | Count rules per query across section categories. |
| AC4 | AI-extracted rules are visually distinguishable from validated rules in any output that uses them. | Inspect skeleton output for provenance markers. |
| AC5 | An engineer can add, edit, or remove rules without code changes. | The registry is data, not code. |
| AC6 | The registry supports querying by multiple conditions (category + project type + jurisdiction). | Test compound queries. |

---

## 9. Architecture Overview

```
  +---------------------+         +---------------------+
  | Rule Extraction     |         | Skeleton Generator  |
  | Pipeline            |         | (Concept 01)        |
  | (future)            |         |                     |
  +----------+----------+         +----------+----------+
             |                               |
             | writes                        | queries
             v                               v
  +----------+-------------------------------+----------+
  |                                                     |
  |              Standards Registry                     |
  |                                                     |
  |  +-------+  +-------+  +-------+  +-------+        |
  |  | NZS   |  | NZS   |  | Council|  | Style |       |
  |  | 3604  |  | 1170.5|  | Rules  |  | Guide |       |
  |  +-------+  +-------+  +-------+  +-------+        |
  |                                                     |
  |  Storage: JSON/YAML files or lightweight DB         |
  |  Query: deterministic filter, not semantic search   |
  +-----------------------------------------------------+
```

### Storage format

For the MVP, rules are stored as **YAML or JSON files** grouped by
standard. This keeps them version-controlled, diff-able, and editable
without tooling. A lightweight query layer filters by category and
applicability conditions.

Migration to a database is deferred until the rule count exceeds what
flat files can handle comfortably (likely 500+ rules).

---

## 10. Relationship to Other Concepts

| Concept | Relationship |
|---------|--------------|
| [01-skeleton-generator](../01-skeleton-generator/skeleton-generator.md) | **Consumer.** The skeleton generator queries the registry at Step 6 to insert standards references into each section. The registry does not depend on the skeleton generator. |
| [01-skeleton-generator/incumbent-process.md](../01-skeleton-generator/incumbent-process.md) | **Context.** The incumbent process documents how standards are currently applied (informally, by experience). This concept replaces that with structured dispatch. |

---

## 11. Open Questions

| #  | Question | Impact |
|----|----------|--------|
| Q1 | What is the minimum viable set of standards for bootstrap? Is NZS 3604 + NZS 1170.5 + one council district plan sufficient for a useful MVP? | Determines Phase 1 scope. |
| Q2 | Should the registry store the full clause text or just a summary? Full text is more useful but may have copyright implications. | Affects rule verbosity and legal risk. |
| Q3 | What storage format is best for the MVP? YAML (human-readable, diffable) vs. JSON (programmatic) vs. SQLite (queryable). | Affects developer ergonomics. |
| Q4 | How should rule versioning work when a standard is updated (e.g., NZS 3604:2011 -> NZS 3604:2025)? | Affects long-term maintainability. |
| Q5 | Should rules have severity levels (mandatory vs. recommended vs. informational)? | Affects how the skeleton generator presents them. |
| Q6 | How granular should categories be? Too coarse = too many rules per dispatch. Too fine = complex taxonomy. | Affects dispatch quality. |
