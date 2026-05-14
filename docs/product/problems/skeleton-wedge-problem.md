# Problem Statement: The Skeleton Wedge

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-04-20.
**Strategic bet**: [Bet 1 — The Free Skeleton Wedge Beats Paid Acquisition](../strategy/strategic-bets.md)

## Target User

Intermediate civil/geotechnical engineer (3-7 years post-graduation), working inside a
Small NZ or AU consultancy (5-50 person firm) on residential or light-commercial GBR/GIR
work. These firms lack the budget, engineering bench, or innovation mandate to build
bespoke AI tooling. They must buy or go without.

Large firms (Tonkin + Taylor, WSP, Beca) build their own AI internally. Small firms
are the addressable market.

**Secondary user (Phase 2)**: the senior engineer who is the current knowledge bottleneck. The skeleton serves as a knowledge externalisation tool — capturing what the senior engineer holds in memory (applicable standards, mandatory clauses, jurisdiction-specific requirements) so that the firm is not dependent on any one person. This framing is particularly acute when a senior engineer is approaching retirement.

## Core Pain

When an intermediate engineer sits down to draft a Geotechnical Baseline Report (GBR) or
Geotechnical Interpretive Report (GIR), the first 2-4 hours are spent assembling the
document skeleton: section headings, placeholder content, standard clause references,
and structural scaffolding that varies by jurisdiction, client scope, and report type.
This work is repetitive, error-prone, and produces no engineering value. The engineer
knows roughly what the skeleton should contain but lacks confidence that nothing has been
missed, and the firm's internal templates are stale, partial, or tribal knowledge held by
senior staff who are bottlenecked on other reviews.

The job-to-be-done (per [jtbd.md](../strategy/jtbd.md)): the engineer wants a quality
layer that flags what a senior reviewer would mark up, so they can ship a draft that
survives review in fewer rounds.

## Extended Framing — Three Functions of the Skeleton

Today's advisory board discussion (Ron + Graeme, 2026-05-14) established that the skeleton
generator is not simply a "document structure template" tool. It performs three distinct
functions during the design phase:

1. **Standards nomination** — identifies which standards are mandatory for the project type
   (jurisdiction, report type, site conditions). This function is deterministic: standards are
   drawn from the Standards Registry by rule. **LLM inference of applicable standards is
   prohibited.** The output must be auditable and traceable to the registry.

2. **Design-phase checklist** — items the engineer must address during site investigation and
   design before writing begins. This externalises the senior reviewer's pre-drafting mental
   model and gives the intermediate engineer a structured prompt to work from.

3. **Report structure** — section headings, placeholders, mandatory clauses, and jurisdiction-
   specific scaffolding that varies by report type.

The three functions are separable but delivered together. A user who only receives the
report structure without the standards nomination and design checklist gets a formatting
tool, not a quality layer.

## Current Alternatives and Their Friction

| Alternative | Friction |
|---|---|
| **Manual drafting from memory or firm templates** | Templates are stale and incomplete. Tribal knowledge is bottlenecked in senior staff. Intermediate engineers miss sections they don't know to include. |
| **SupaHuman / Archie (bespoke AI build)** | $50k+ engagement, 6-month delivery, enterprise sales process. Inaccessible to Small firms. SupaHuman is a generalist RAG agency (same architecture does travel RFPs and geotech reports) with one engineering client. Thin technical moat, no domain IP. |
| **ChatGPT or generic AI assistant** | No jurisdictional grounding (NZS, AS, NZGS). No firm context. No audit trail. Partner will not allow it. Output is plausible but unreliable for professional-grade reports. |
| **Do nothing** | Engineer submits an incomplete draft, absorbs 3x markup from senior reviewer, rebuilds the document over evenings, loses morale. Senior reviewer wastes time on structural issues instead of engineering substance. |

## Competitive Validation

The Archie competitive intelligence session (2026-04-20) confirms that demand exists.
Soil & Rock Consultants (NZ) commissioned a bespoke AI report-drafting co-pilot from
SupaHuman. This validates the market pain but the delivery model is inaccessible to
Small firms: bespoke builds at $50k+ with a generalist agency are not a scalable solution for
5-50 person firms.

Beca built Frankly.AI in-house, launched it commercially via Microsoft Teams globally, and has
since discontinued it, confirming that engineering consultancies lack the DNA to sustain AI
product commercialisation. The tool-building opportunity belongs to a dedicated vendor.

## Measurable Outcome

Per Bet 1's kill criterion: within 90 days of launch (by 2026-09-01), the Free Skeleton
Generator must achieve 50 or more verified-email signups AND 5% or more outbound response
rate from quota-exhausted users. Failure on either metric kills the wedge without revival.

## Constraints

- NZ + AU geography only (Bet 5 beachhead doctrine).
- SSO-gated — verified work email required.
- Free tier only — no revenue from skeleton; revenue comes from downstream Pre-Review
  conversion (Bet 2).
- Audit trail must ship with the skeleton tool, not as a Phase-2 add-on (see
  [audit-trail-day1-requirement.md](../prds/audit-trail-day1-requirement.md)).
- Switzerland-neutral positioning: the skeleton is a structural scaffold, not an
  engineering opinion (per [positioning.md](../strategy/positioning.md) and
  [non-goals.md](../strategy/non-goals.md)).

## Next Step

This problem statement feeds into the PRD for the Free Skeleton Tool:
[skeleton-generator-prd.md](../prds/skeleton-generator-prd.md).
