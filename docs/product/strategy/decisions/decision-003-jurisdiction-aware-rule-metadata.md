# Decision 003 — Jurisdiction-Aware Rule Metadata (Rule Toggle Architecture)

**Status**: Decided. **Date**: 2026-05-10. **Deciders**: Founder, Mark, Graeme.

---

## Context

The Pre-Review rule library includes rules sourced from NZ/AU practice (e.g., SCOPE-CLAUSE-01,
SCOPE-CLAUSE-05) and US practice (SCOPE-CLAUSE-02, SCOPE-CLAUSE-04, SCOPE-CLAUSE-06). The
initial framing was to "drop" US-practice rules from the NZ/AU product. As the rule engine
design was discussed, it became clear that "drop" and "off by default for a jurisdiction" are
architecturally different choices with materially different long-term costs.

SCOPE-CLAUSE-02, -04, and -06 are not wrong rules. They are wrong *for NZ/AU*. If Redline
expands to the US market (Bet 5, geographic expansion), they become valid. Hard-coding their
absence creates a silent assumption that must be excavated and undone at expansion time.

## Decision

1. **Rules are jurisdiction-scoped, not dropped.** Every rule in the Pre-Review rule library
   carries explicit metadata:
   - `jurisdiction`: list of applicable markets (`NZ`, `AU`, `US`, or `global`)
   - `enabled_by_default`: boolean — true if the rule executes by default when the document's jurisdiction matches one of the rule's declared jurisdictions; the runner applies this after filtering by jurisdiction, so a rule with `jurisdiction: [US]` never runs in NZ/AU regardless of this field
   - `configurable`: boolean — whether a firm can override the rule via House Rules

2. **The rule runner reads metadata.** Which rules execute for a given document is determined
   by the rule's jurisdiction metadata and the document's declared jurisdiction — not by
   hard-coded lists of included or excluded rules.

3. **Sprint 2-3 implements the rule metadata schema alongside the first rules.** Every rule
   authored in Sprint 2-3 must include all three metadata fields. No rules ship without them.
   Engineering must define and implement the metadata schema before the first rule is authored.

4. **UI deferred.** The toggle surface — letting firms enable or disable rules via the
   House Rules Authoring Console — is a Sprint 4+ concern (Feature K). The data model is
   designed to support it now; the UI is not built now.

5. **US rules ship in the schema, inactive for NZ/AU.** SCOPE-CLAUSE-02, -04, and -06 are
   authored as rules with `jurisdiction: [US]` and `enabled_by_default: false` for NZ/AU.
   They are present, parseable, and future-safe — not absent.

## Options Considered

| Option | Description | Verdict |
|---|---|---|
| A. Drop US rules entirely | Remove SCOPE-CLAUSE-02/04/06 from the rule library for NZ/AU | Rejected — silent assumption, expensive to undo at US expansion, obscures design intent |
| B. Hard-code NZ/AU rule list | Include only NZ/AU rules in the codebase; no jurisdiction metadata | Rejected — same problem as A; no schema to extend; every new jurisdiction requires a code change |
| C. Jurisdiction-scoped metadata | Every rule has explicit jurisdiction and default-on/off metadata; runner reads it | **Adopted** — makes jurisdiction sensitivity explicit, costs very little in Sprint 2-3, positions cleanly for US expansion and firm-level customisation |
| D. UI toggle first | Build the House Rules toggle UI before defining jurisdiction metadata | Rejected — UI before data model is backwards; metadata schema is the prerequisite |

## Rationale

- **Retrofitting is expensive.** Jurisdiction metadata added later requires auditing every rule
  for unstated assumptions. Adding it at authoring time costs one field per rule.
- **"Drop for NZ/AU" IS a toggle, just an untracked one.** Making it explicit in the data
  model transforms an implicit assumption into a configurable, auditable fact.
- **US expansion is a live bet.** Bet 5 (`strategic-bets.md`) excludes a third geography in H2
  but does not permanently close the option. US-practice rules present in the schema cost
  nothing and remove a future rework dependency.
- **Sprint 4+ Business tier.** The House Rules Authoring Console (Feature K) needs a rule
  metadata schema to expose. Building the schema in Sprint 2-3 is the correct dependency order.
- **Domain grounding.** Graeme confirmed that SCOPE-CLAUSE-02, -04, and -06 reflect legitimate
  US ASCE practice and are not erroneous — they are jurisdiction-inappropriate for NZ/AU, not
  technically wrong.

## Consequences

- All Sprint 2-3 rule files must include `jurisdiction`, `enabled_by_default`, and
  `configurable` metadata fields.
- The rule runner must accept jurisdiction as a parameter and filter rules by metadata.
- Engineering must design the rule metadata schema before the first Sprint 2 rule is authored.
- The House Rules UI design (Sprint 4+, Feature K) should be briefed on the metadata
  structure at Sprint 4 kickoff — not designed in isolation from it.

## References

- `docs/product/strategy/strategic-bets.md` (Bet 5 — geographic expansion)
- `docs/product/strategy/feature-backlog.md` (Feature K — House Rules Authoring Console)
- `docs/product/strategy/decisions/parked-decisions.md` P-015 (House Rules authoring console scope)
- `docs/product/strategy/decisions/parked-decisions.md` P-012 (Geographic expansion beyond NZ + AU)
