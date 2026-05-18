# Problem Statement: The Generic AI Absence Detection Gap

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-05-17.
**Strategic bet**: [Bet 1 — The Free Skeleton Wedge](../strategy/strategic-bets.md) +
[Bet 2 — Pre-Review Is the Paid Product Day-1](../strategy/strategic-bets.md)
**Trigger**: Ron's strategic risk assessment (2026-05-17) — generic AI commoditisation
outpacing specialisation value.

---

## Context: Why This Problem Exists Now

Claude can now add inline comments directly into a Word document. Microsoft Copilot is
embedded in the authoring environment. These capabilities were, until recently,
differentiators that Redline could claim. They no longer are.

If an intermediate engineer mentally categorises Redline alongside Claude or Copilot —
as "another AI tool that comments on my document" — the price ceiling collapses from
infrastructure ($200-500/month) to AI tool ($20-50/month). The product's reason to
exist must be demonstrably different from what generic AI already does, and that
difference must be visible in the engineer's first session.

Ron's core question: **What is the smallest demonstrable capability gap between
Claude-on-a-Word-doc and Redline's Pre-Review that an intermediate engineer would
notice in their first session?**

---

## Target User

Intermediate geotechnical engineer (3-7 years post-graduation), working inside a Small
NZ or AU consultancy (5-50 staff) on GBR/GIR work. This engineer has used ChatGPT or
Claude for drafting assistance. They consider generic AI "pretty good" for document work.
They have not yet encountered a tool that checks their document against a jurisdictional
standards framework.

Same target as the [skeleton wedge problem](skeleton-wedge-problem.md), but the pain
here is not "I need help starting a report" — it is "I already have AI tools that
review my documents. Why do I need another one?"

---

## Core Pain — What the Engineer Does Not Know They Are Missing

The intermediate engineer who asks Claude to review a draft GBR receives comments about
sentence clarity, structural organisation, and general technical plausibility. These
comments are useful. They operate entirely on what is present in the text. Claude reacts
to what it can see.

What Claude cannot do — and what defines Redline's reason to exist — is detect what is
absent.

The Claude GBR experiment (2026-05-14, Graeme review against NZ standards from the
NotebookLM notebooks) produced 6 citation errors (3 HIGH severity) and 10
structural/domain issues in a single AI-generated report. None were planted — all are
organic AI failure modes. Every error maps to a Redline rule. Four failure classes
emerged, and they share a single structural cause:

### 1. Missing mandatory standards

Claude generated a GBR for a NZ residential development and omitted NZS 4431 (the
governing earthworks compliance framework) entirely. The standard was not cited
incorrectly — it was not cited at all. No amount of prompted review would catch this
because Claude does not maintain an authoritative model of which NZ standards are
mandatory for a given report type and jurisdiction.

Provenance: [claude-gbr-demo-review.md](../../knowledge/geotechnical/report-writing/claude-gbr-demo-review.md), Error 1.

### 2. Hallucinated standard citations

Claude cited NZS 4407:2015 (a road aggregate standard) for SPT testing. The citation
looks authoritative — correct format, correct year, real standard number. An
intermediate engineer reading the output would not know the standard is irrelevant
because the citation pattern matches what they expect to see. Generic AI cannot
distinguish a valid citation from a plausible-looking but wrong one without a curated
standards registry to check against.

Provenance: [claude-gbr-demo-review.md](../../knowledge/geotechnical/report-writing/claude-gbr-demo-review.md), Error 4.

### 3. Missing protective clauses

The Claude-generated GBR lacked an inferred conditions caveat — the single most
important protective clause in a NZ geotechnical report. It establishes that actual
ground conditions may differ from what the report describes. Without it, a court may
infer the engineer intended the report to be comprehensive. The report also lacked a
temporal validity caveat. Both are mandatory at well-run NZ firms. Claude did not flag
their absence because it has no model of what clauses should be present.

Provenance: [claude-gbr-demo-review.md](../../knowledge/geotechnical/report-writing/claude-gbr-demo-review.md), Issues 2, 3, 5.

### 4. Warranty language masquerading as professional opinion

Claude wrote "the site is considered suitable for conventional shallow foundations" —
language that could function as an express warranty under NZ PI (Professional Indemnity)
insurance. NZ PI policies typically exclude liability for contractual guarantees of
outcome. A senior reviewer would condition this with hedging language. Claude does not
flag warranty-risk language because it has no model of the professional liability
boundary between a qualified opinion and a guarantee of outcome.

Provenance: [claude-gbr-demo-review.md](../../knowledge/geotechnical/report-writing/claude-gbr-demo-review.md), Issue 4; [business-of-engineering-quality-layer-problem.md](business-of-engineering-quality-layer-problem.md), warranty language drift section.

### The structural cause

**Generic AI has no authoritative model of what should be in a geotechnical report. It
can only comment on what IS in the document. Redline checks against what SHOULD BE in
the document.**

This is not a difference in quality. It is a difference in kind. Claude is a
text-reaction tool. Redline is an absence-detection engine backed by a jurisdictional
standards framework. The gap is structural, not parametric — it cannot be closed by
prompting Claude differently or by feeding it more context.

---

## The One-Sentence Gap

> **Claude comments on what you wrote. Redline flags what's missing — the standard you
> didn't cite, the clause you didn't include, the scope limitation you didn't state.**

This sentence names the gap, names the product's reason to exist, and names what the
engineer would notice in their first session: flags for things that are not there. This
is exactly what their senior reviewer does and what no generic AI can replicate without
a curated domain model.

---

## The First-Session Test

An intermediate engineer would notice the gap in their first Pre-Review session if
Redline flagged at least one item they had not caught and that Claude would not catch:

- A mandatory NZ standard not cited in the report (rule: CITE-EXIST-01)
- A scope limitation clause missing from the conclusions section (rule: SCOPE-CLAUSE-01)
- Warranty-risk language in a section that should contain hedged professional opinion
  (rule: RISK-LANG-01)

The Claude GBR experiment demonstrates that all three categories appear in a single
AI-generated report, organically, with HIGH severity. The gap is not theoretical. It is
observable, repeatable, and recognisable to any NZ intermediate engineer who has received
senior review markup.

The first-session recognition moment: the engineer sees a Redline flag and thinks "that
is exactly what my senior reviewer would say." Claude never produces that recognition
because Claude's comments are about the text, not about the standards behind the text.

---

## Why Generic AI Cannot Close This Gap

The gap is structural, not parametric:

1. **No standards registry.** Generic AI has no curated, versioned, jurisdictional
   standards corpus. Without one, it cannot detect absence — it cannot know that
   NZS 4431 should be cited for residential earthworks, that NZS 4407 is a roading
   standard, or that NZS 4402 is test methodology rather than a compliance framework.

2. **No rule library.** Generic AI has no domain-specific rules mapping report type,
   jurisdiction, and section type to mandatory content. It cannot know that a
   conclusions section in a GBR requires an inferred conditions caveat, a temporal
   validity statement, and conditioned professional language.

3. **No firm context.** Generic AI has no model of a specific firm's house rules,
   review expectations, or structural conventions. Even if it could detect generic
   absences, it cannot detect firm-specific absences.

4. **Prompting does not solve the problem.** An engineer could prompt Claude with
   "check my report against NZ standards." Claude would produce plausible-sounding
   comments, but it would still not know which standards apply to this report type
   in this jurisdiction, and it would still hallucinate citations with high confidence.
   The failure mode is not insufficient prompting — it is the absence of an
   authoritative domain model.

This structural gap is what the Standards Knowledge Store (Bet 3) defends. The moat is
not AI capability — it is curated domain knowledge that generic AI cannot replicate
without years of the same domain investment.

---

## Measurable Outcome

In the first Pre-Review session, the intermediate engineer receives at least one
HIGH-severity flag that:

- (a) maps to a Redline rule backed by the Standards Knowledge Store,
- (b) the engineer recognises as something their senior reviewer would catch, and
- (c) Claude or Copilot would not have flagged.

**Measurable proxy**: In KR2 discovery conversations with the 10 Phase 1 feedback
partners, ask: "Did Redline flag something in your report that you had missed and that
your existing AI tools would not have caught?" Target: 7 or more of 10 feedback
partners answer yes within their first three sessions.

---

## Strategic Link

This problem links to Bet 1, Bet 2, and Bet 3:

- **Bet 1 (Skeleton Wedge)**: If the engineer believes generic AI is "good enough" for
  report work, the skeleton generator becomes a commodity — one of many AI report
  tools — and the wedge does not convert to paid Pre-Review. The gap must be visible
  before the engineer reaches the paywall.

- **Bet 2 (Pre-Review as paid product)**: The entire value proposition of Pre-Review
  rests on Redline doing something generic AI cannot. If the gap is not nameable and
  demonstrable, Pre-Review has no pricing power above the $20-50/month AI tool ceiling.

- **Bet 3 (Standards Knowledge Store)**: The absence-detection capability depends
  entirely on the curated standards corpus. Without it, Redline degenerates to
  "another LLM wrapper" — the exact commoditisation risk Ron identified.

The gap also activates the compounding value story from Bet 2: as AI-generated report
volume increases, the absence-detection problem worsens — not stays constant. More
AI-written reports means more fabricated citations, more missing standards, more
confident warranty language that passes surface review. Redline's value grows with AI
adoption because the "without Redline" baseline deteriorates.

---

## Constraints

1. **Demonstrable, not argued.** The engineer must see the gap in their first session,
   not read about it in marketing copy. The Pre-Review rule library must include at
   least the four absence-detection categories (missing standard, hallucinated
   citation, missing protective clause, warranty language) from Sprint 1.

2. **The engineer does not need to know what they are missing.** The engineer who does
   not know NZS 4431 exists cannot be told to "check for NZS 4431." Redline must
   surface the absence without the engineer asking.

3. **Every flag must be source-traceable.** Each flag traces to a standards entry in
   the Knowledge Store or a rule in the Pre-Review library. "Redline thinks you should
   add X" is not defensible. "NZS 4431:2022 requires X for this report type in this
   jurisdiction" is.

4. **Switzerland-neutral.** Redline flags the gap; the engineer resolves it. Redline
   does not add the missing standard or rewrite the clause. Per
   [positioning.md](../strategy/positioning.md): "We surface; the human resolves."

5. **The first-session test depends on the Claude GBR experiment remaining valid.** If
   a future Claude version reliably cites NZ standards and detects missing clauses,
   the gap narrows and the positioning must be re-evaluated. The structural dependency
   on the Standards Knowledge Store remains — but the marketing framing would need to
   shift from "Claude cannot do this" to "Claude gets it wrong unpredictably."

---

## Clarity Check

| Check | Status | Detail |
|---|---|---|
| Target user | Identified | Intermediate engineer, 3-7 years, Small NZ/AU firm, GBR/GIR work, already using generic AI |
| Core pain | Identified | Engineer believes generic AI is "good enough" — cannot see the absence-detection gap until Redline shows it |
| Desired outcome | Measurable | 7+ of 10 feedback partners confirm Redline flagged something their existing AI tools would not have caught, within first 3 sessions |
| Strategic link | Linked | Bet 1 (commodity risk), Bet 2 (pricing power), Bet 3 (moat) |
| Constraints | Stated | Demonstrable in first session, source-traceable, Switzerland-neutral |

---

## Open Questions

1. **Ron's transition gate challenge.** Ron challenged the Phase 1 to Phase 2 gate
   (7/10 unprompted repeat use in 30 days) as potentially aspirational. Does the
   absence-detection gap produce enough "must-have" recognition to drive unprompted
   return? Or does the skeleton generator's single-player nature (no network effects,
   no collaboration) structurally limit retention regardless of how good the gap
   demonstration is? This question must be tested empirically with the 10 feedback
   partners — it cannot be answered analytically.

2. **Is the one-sentence gap for internal clarity or external communication?** "Claude
   comments on what you wrote; Redline flags what's missing" is effective as a team
   north star. It may be too direct for external positioning — engineers who use Claude
   may hear it as dismissive of their current workflow. John should adapt the external
   messaging. The internal sentence should be locked now.

3. **Skeleton-level visibility.** This problem statement scopes to Pre-Review per
   Ron's question. But the engineer's first product contact is the free Skeleton
   Generator (Bet 1). Does the skeleton itself need to demonstrate the
   absence-detection gap — for example, by nominating standards the engineer would
   not have known to include? If the skeleton looks like something Claude could have
   generated, the engineer may never reach Pre-Review to see the gap. This may
   warrant a separate problem statement.

---

## Next Step

1. **Hypothesis** — Formalise as a testable hypothesis: "Intermediate engineers who
   see Redline flag a HIGH-severity absence in their first Pre-Review session are
   significantly more likely to return unprompted than those who see only style or
   formatting flags." Route to `pm-hypothesis-builder`.

2. **Ron** — Confirm whether the one-sentence gap ("Claude comments on what you wrote;
   Redline flags what's missing") is locked as the internal north star. Confirm
   whether the skeleton must also demonstrate the gap before the engineer reaches
   Pre-Review (Open Question 3).
