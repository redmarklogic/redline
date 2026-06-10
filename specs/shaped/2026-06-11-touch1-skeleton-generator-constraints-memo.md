# Touch 1 Constraints Memo — Skeleton Generator (Feature A)

**From**: Peter (Principal Engineer) · **To**: Matt (UI/UX Designer)
**Date**: 2026-06-11 · **Sync item**: A-19 (time-critical)
**PRD**: `docs/product/prds/skeleton-generator-prd.md` (Draft v1 + EnggNZ/NZGS amendment, 2026-06-09)
**Two-Touch position**: This is Touch 1. After this memo I am absent until Touch 2
(architectural compliance review of SpecKit output). I will not review wireframes,
interaction patterns, or component specs. Design freedom inside these constraints is yours.

This memo is deliberately rough and breadboard-level (places, affordances, connections).
It contains no wireframes and prescribes no solutions.

---

## Diagnosis

- **(a) Stage**: Pre-launch walking skeleton. Deploy chain shipped 2026-06-10 (staging +
  prod Cloud Run services live, per ADR-022/ADR-023). Skeleton Generator must ship by
  **2026-06-30**. Bet 1's kill clock (50 verified signups in 90 days) starts at launch.
- **(b) Binding constraints now**: engineer trust (conformance to the EnggNZ/NZGS 2023
  guideline is the minimum credibility bar — Mark's amendment, Graeme-validated);
  time-to-value (under 60 seconds signup-to-first-download); one design pass — Matt
  works independently this week so build can start immediately after; founder attention
  is the scarcest resource.
- **(c) Theoretical-only constraints**: AU jurisdiction, complex/commercial project
  types, paid tier, mobile, Word task pane. None binds this sprint. Nothing in the
  design should spend effort accommodating them.

**Surviving the Round**: every constraint below is justified at the short-runway horizon
(3–6 months) — they are all Sprint 1 ship requirements or kill-criterion mechanics.
Anything justified only long-runway has been moved to the No-Design list.

---

## Assumptions taken about the PRD (Mark is confirming readiness in parallel)

I am not waiting on Mark's confirmation. If any assumption fails, this memo is revised
— flag the conflict, do not design around it silently.

1. **A1**: The PRD as amended 2026-06-09 is the binding scope. The amendment's
   acceptance criteria AC2a–AC2g replace the original AC2.
2. **A2**: The quota cap (3 vs 5 documents — PRD Open Question 1) is unresolved.
   Treat the cap as a **configurable displayed value**, not a hard-coded number in copy
   or layout.
3. **A3**: Conditional-section logic beyond the keyword rules (CL-G5, CL-G6, CL-G7a,
   CL-G7b) is **blocked pending my shaping** of the input model (PRD hard design gate,
   AC2f). Assumption: v1 ships with safe defaults and keyword rules only. Therefore the
   UI must **not** depend on any user-facing input model for conditional sections (no
   project-type pickers, no site-condition questionnaires).
4. **A4**: The only report type in v1 is the **Geotechnical Assessment Report** (the
   PRD treats "GIR" as equivalent; GBR is out of scope — gap GBR-STRUCT-01 closed).
   Assumption: no report-type selector is needed in v1. If the flow surfaces report
   type at all, it is the extracted value from the LOE, not a user choice.
5. **A5**: Multi-discipline refusal behaviour (PRD Open Question 4) is undecided.
   Design a boundary/refusal **place** in the flow; its copy and exact trigger are
   Mark's to resolve. Do not invent the policy.

---

## The flow (breadboard)

Places and affordances only. Connections between places are yours to design.

| Place | Must afford | Notes |
| --- | --- | --- |
| P1 Sign-up / verify | Verified **work email** SSO; no anonymous path | No generation reachable before verification |
| P2 Upload | One-click LOE upload; pre-loaded demo LOE ("No LOE? Try our example") | No manual parameter form exists anywhere |
| P3 Progress | Live progress through real pipeline stages (extract → build sections → apply standards) | Indicator reflects actual stages — it must not fake progress |
| P4 Result | .docx download | Editing happens in Word, not in the product |
| P5 Quota exhausted | Blocked generation + CTA to Pre-Review trial | This place IS the Bet 1 outbound trigger — it is a conversion surface, not an error state |
| P6 Boundary warning | Surface the guideline scope boundary when the LOE indicates a non-residential or complex project | Must not silently generate; must not author engineering opinion |

---

## Hard constraints (each is testable)

1. **SSO gate**: no skeleton generation without a verified work email (PRD AC7).
2. **No form, no fallback form**: LOE upload is the only input path. If extraction
   cannot populate a field, the skeleton generates with that field blank and the user
   edits in Word (founder decision 2026-04-22; PRD AC8). Do not design a metadata
   review/correction step — that decision is already made and closed.
3. **Latency envelope**: generation completes within 30 seconds of upload (AC1);
   signup-to-first-download under 60 seconds (PLG activation target). The progress
   place must hold attention across a real 10–30 second wait.
4. **Output**: downloadable .docx with proper heading hierarchy (AC4). No in-browser
   document editing in v1.
5. **Quota**: 3–5 documents (configurable, non-renewable). Exhaustion blocks generation
   and presents the Pre-Review trial CTA (AC6).
6. **Boundary surfacing**: a non-residential/complex-project LOE must produce a visible
   boundary message — silent generation of a structurally insufficient skeleton is
   prohibited (PRD Out of Scope + Graeme's domain note 3).
7. **Switzerland-neutral**: nothing in the UI may present the product as authoring
   engineering opinions or recommendations (PRD AC9). The skeleton is scaffolding.
8. **Terminology gate**: all geotechnical terms in the design (Geotechnical Assessment
   Report, LOE, Geotechnical Model Table, clause names) pass through Graeme before
   SpecKit handoff — blocking, per the dispatch table. The UL table in
   `docs/architecture/domain-model.md` is the reference.

## Opportunities (not constraints — your call)

- The progress indicator doubles as positioning copy ("Extracting metadata… Building
  sections… Applying standards…") — John's assessment, embedded in the PRD Decision Log.
- Showing what was extracted vs left blank makes the Day-1 audit trail tangible
  ("Your AI wrote it. Who checked it?"). If you use this, it must stay read-only —
  constraint 2 still forbids an editing step.

## Rabbit holes — identified and removed

- **Conditional-section picker / project-type questionnaire**: out. Blocked on my
  shaping of the input model (AC2f). Designing it now would be thrown away.
- **Editable extraction-review step**: out. Decided and closed 2026-04-22.
- **In-browser .docx preview/rendering**: out of appetite for Sprint 1.
- **Multi-discipline refusal policy**: place exists (P6 can host it); policy and copy
  await Mark's answer to PRD Open Question 4. Do not block on it.
- **Quota top-up / renewal mechanics**: out — quota is non-renewable in free tier.

## No-Design list (explicitly excluded from v1)

AU jurisdiction toggle · GBR option · report-type selector · paid tier / billing ·
mobile client · Word task pane · House Rules configuration · Pre-Review annotation UI.

---

## Appetite

Design appetite: wireframes this week (week of 2026-06-08). Build appetite: ship by
2026-06-30. If a constraint above makes the design appetite unreachable, flag it to
Mark and me immediately — we descope, we do not extend.

## Next

Matt designs independently from here. Output goes to Graeme (terminology gate), then
SpecKit. I return at Touch 2 for architectural compliance of the SpecKit output only.
In parallel, I owe the conditional-logic input-model Pitch (AC2f gate) — that is a
separate shaping session and does not block wireframes under assumption A3.
