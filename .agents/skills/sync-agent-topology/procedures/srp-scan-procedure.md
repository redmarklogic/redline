# SRP Scan Procedure — Standalone Reusable Reference

**Purpose:** Detect Single Responsibility Principle (SRP) violations in skill `name:` and
`description:` frontmatter fields. Used during the mandatory SRP Compliance Pass in
`procedures/run-topology-sync.md`.

---

## Scan Algorithm

```
FOR EACH file matching .agents/skills/*/SKILL.md:

  1. Read frontmatter fields: name, description
  2. Check name field:
     a. Does it contain " and " (space-and-space)?
     b. If yes → candidate violation; proceed to classification
  3. Check description field:
     a. Does it contain " and " linking two distinct concerns (see Pattern Definitions)?
     b. If yes → candidate violation; proceed to classification
  4. Classify each candidate:
     a. Check skill name against the Known Exception Skip-List (below)
     b. If listed → disposition = known-exception
     c. If pattern matches false-positive rules → disposition = false-positive
     d. Otherwise → disposition = new-violation
  5. Record in violations-list.md:
     skill name | field flagged | pattern matched | disposition
```

---

## "and" Pattern Definitions

Three categories of "and" appear in skill names and descriptions. Only Category A is a
violation.

### Category A — Structural Conjunction (VIOLATION)

An "and" that joins two *independently completable* concerns. Each concern could stand
alone as its own skill without losing meaning.

**Signals:**
- Removing one side of the "and" leaves a coherent, complete skill.
- The two sides have different inputs, outputs, or triggering conditions.
- The combined name implies two separate phases of work.

**Examples (violations):**
- `hiring-and-assessment` — hiring and assessment are independent concerns.
- `find-and-fix` (as in `sonarqube-find-and-fix`) — finding issues and fixing them are
  separate concerns; however, this skill is approved as a known exception
  (`justified-orchestrator`) — all steps serve one end-to-end quality-gate concern.
- `marketing-social-selling-linkedin` — marketing strategy and social selling tactics
  are separable; `linkedin-social-selling` is the correct form.

### Category B — Grammatical "and" (NOT a violation)

An "and" used as natural language within a single unified concern. Removing it would
damage the meaning without separating independent work.

**Signals:**
- The phrase describes one outcome, not two parallel outcomes.
- The "and" appears in a description clause, not as a structural conjunction in the name.

**Examples (not violations):**
- "structures and documents" in a single documentation-concern description.
- "reads and validates" as two steps of one pipeline phase.
- "policy document and rationale" as parts of one output artifact.

### Category C — Domain Compound Noun (NOT a violation)

An "and" that is part of an industry-standard term or established phrase where splitting
would destroy the meaning or produce non-standard terminology.

**Signals:**
- The phrase matches a known industry term (check the UI Terminology Glossary at
  `docs/knowledge/geotechnical/report-writing/ui-terminology-glossary.md`).
- Both sides refer to the same domain object, not two different work products.

**Examples (not violations):**
- `linkedin-social-selling` — "social selling" is a domain compound noun; "linkedin" is
  the platform qualifier. No "and" present; listed here as reference.
- Any geotechnical compound term confirmed in the UI Terminology Glossary.

---

## Domain Compound Noun Allowlist

Skills in this list match the "and" pattern but are confirmed domain compound nouns or
grammatical connectives. Treat as false-positive during scan.

| Skill Name | Justification |
|---|---|
| `mcp-cce` | No "and" in name; "and session continuity" in description is grammatical — one concern |
| `pm-product-strategist` | "JTBD analysis, OST tree, OKR alignment" are sequential steps; no structural "and" in name |

Add to this table when a new false-positive is confirmed by the scan facilitator.

---

## Known Exception Skip-List

Skills pre-approved as `known-exception`. No file lookup required — this table is the
authoritative record. To add a new exception, extend this table directly.

| Skill | Exception Category | Rationale |
|---|---|---|
| `resolving-pr-issues` | `justified-pipeline` | Sequential PR resolution steps; splitting destroys end-to-end coherence |
| `spec-kit` | `justified-orchestrator` | Single concern: specification-driven development; Layer 0 vendor-managed |
| `mcp-cce` | `justified-coherent-interface` | All tools serve one concern — codebase discovery and session continuity |
| `ceremony-monthly-editorial-session` | `justified-pipeline` | Single trigger (new issue), single output concern |
| `pm-product-strategist` | `justified-pipeline` | JTBD/OST/OKR are sequential steps of one strategy synthesis concern |
| `library-management` | `justified-pipeline` | All operations serve one concern — digital library maintenance |
| `linkedin-social-selling` | `domain-compound-noun` | "social selling" is a domain compound noun; "linkedin" is the platform qualifier |
| `sync-agent-topology` | `justified-orchestrator` | Single concern: topology synchronisation |
| `sonarqube-find-and-fix` | `justified-orchestrator` | All steps serve one concern — end-to-end SonarQube quality gate |

---

## Output Format — violations-list.md

Publish to `docs/people/drafts/reports/violations-list.md`.

```markdown
# SRP Violations List — Topology Sync YYYY-MM-DD

| Skill Name | Field Flagged | Pattern Matched | Disposition |
|---|---|---|---|
| example-skill | name | "find-and-fix" | new-violation |
| spec-kit | description | "plan and implement" | known-exception |
| linkedin-social-selling | name | n/a | false-positive |
```

Disposition key:
- `new-violation` — requires resolution before next sync
- `known-exception` — skill is in the Known Exception Skip-List in `srp-scan-procedure.md`
- `false-positive` — grammatical "and" or domain compound noun; no action required
