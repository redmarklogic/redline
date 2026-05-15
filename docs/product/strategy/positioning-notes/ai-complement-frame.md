# Positioning Note — AI Complement Frame

**Status**: Idea capture. Not yet integrated into `positioning.md`.
**Origin**: Founder idea, captured 2026-05-14 via three-voice discussion (Ron, Graeme, John).
**Owner**: Ron.
**Next action**: Promote to `positioning.md` after (a) Founder Memos grounding pass, and (b)
Phase 1 feedback data confirms the "already using Copilot" sub-segment is a real acquisition
pattern.

---

## The Idea

The founder proposes a demo/video concept: Redline reviews an engineering report and produces
Word track-changes-style comments. Those comments are then fed into an AI generation tool
(e.g., Claude for Word, Microsoft 365 Copilot) to action the fixes. The demo shows the
**interface between tools** — Redline as a quality layer that complements AI generation tools
rather than competing with them.

Founder's specific positioning concern: as more engineers use Claude/Copilot to draft or
revise reports, Redline needs to stress *where one tool ends and another begins*, and how
smoothly they interface.

---

## Strategic Assessment (Ron)

### Phase 1 vs Phase 2

The "plays nicely together" narrative is a **Phase 2 trust-and-adoption story**, not a Phase 1
conversion story.

Phase 1 positioning stays focused on: "Redline catches what no general-purpose tool can catch,
because it is trained specifically on NZS, NZGS, and AS for the NZ/AU geotechnical context."
This is a standalone value proposition that does not require the prospect to already use Copilot
or Claude.

Introducing the two-tool workflow at Phase 1 creates a prerequisite assumption (prospect already
uses AI drafting tools) that does not hold across all target firms. Some target firms are
blocked from external AI tools on managed networks (see `enterprise-ai-blocking-risk-assessment.md`).

### Anchor Risk

Positioning against Claude/Copilot's *capability gaps* is a structural trap. A capability-gap
argument invites the follow-up question: "What happens when Claude stops missing it?"

The correct frame is structural, not capability-gap-based:

> "Redline applies jurisdictional engineering knowledge that no general-purpose tool can apply,
> regardless of how good that tool gets at prose."

This argument holds whether Claude improves or not. The defensible asset is the curated NZS/NZGS/AS
corpus, the supersession tracking, and the firm-specific House Rules — not any comparison to
Claude's current limitations.

### Frame Separation

| Frame | Type | Phase | Vehicle |
| --- | --- | --- | --- |
| "Redline catches what jurisdiction-agnostic tools miss" | Conversion hook | Phase 1 | Demo video, LinkedIn, sales email |
| "Redline plays nicely with your existing AI tools" | Trust/adoption device | Phase 2 | Onboarding, partner materials, firm-level sales |

---

## Technical Grounding (Graeme)

The technical claim is defensible with the following precise formulation:

> Claude for Word and Microsoft 365 Copilot are general-purpose language models (LLMs — large
> machine-learning systems trained on broad web and document corpora). They are not trained with
> verified access to current NZS, NZGS, AS/NZS, or AS documents. Clause citations produced by
> these tools are unverifiable and may be fabricated, version-incorrect, or referencing superseded
> editions.

**Three specific failure modes of general-purpose LLMs reviewing a NZ geotechnical report:**

1. **Unverifiable clause citation.** The model cites a standards clause that may not exist,
   reference the wrong version, or describe a requirement that was superseded in a later edition.
   The practitioner cannot verify the citation without independently checking the standard.

2. **Jurisdiction-agnostic review.** The model has no knowledge of regional parameter overlays.
   For example, post-Canterbury earthquake sequence requirements — TC (Technical Category) site
   classifications, EQC Canterbury land damage protocols, and Building Consent-specific
   liquefaction assessment requirements — are not in the model's training data in a reliable,
   clause-level form.

3. **Parameter completeness blindness.** The model cannot check that a report contains all
   parameters required for a specific NZ design type (e.g., TC2 shallow foundations in
   Christchurch). Redline's design-type taxonomy and parameter completeness checking addresses
   this directly.

**Concrete demo example (Graeme-verified):**

A GIR (Geotechnical Interpretive Report) for a new residential subdivision in Christchurch
recommends shallow foundations on a TC2 site without specifying the NZS 1170.5 site class
or completing a liquefaction vulnerability assessment. Claude, asked to review for standards
compliance, might flag "missing liquefaction assessment" (correct) but:
- May phrase the flag in terms of Eurocode 7 (EC7) or ASCE 41, which are not applicable standards in NZ.
- Will not know the TC2-specific depth, bearing, and reinforcing requirements codified through
  Canterbury Geotechnical Register protocols.
- Cannot verify whether the referenced NZGS guidance is the current edition.

Redline flags the specific NZ-applicable requirement, with the correct standard and edition.

**Graeme's condition before the demo is scripted:**

> "I want to see the specific check before the demo is scripted. I will not endorse a demo that
> shows Redline catching a fabricated error."

---

## Marketing Assessment (John)

### Demo Format Assessment

The two-tool demo is a **stronger conversion asset** than the standalone superseded-citation demo.

| Demo format | Mechanism | Strength |
| --- | --- | --- |
| Superseded citation (standalone) | Shows Redline in isolation; viewer must infer the gap | Requires inference |
| Two-tool demo (Claude → Redline) | Shows the gap explicitly, head-to-head | Converts sceptics |

### Feasibility Before Product is Built

A staged concept video is feasible before the product is fully built. The workflow:

1. Screen-recording of a report open in Word.
2. Claude for Word runs a "review" — shown live, output visible.
3. The same document submitted to Redline — output shown as tracked-changes-style comments.
4. Camera freezes on a specific Redline comment that does not appear in Claude's output
   (the Graeme-verified example above).
5. Freeze on the delta. That is the demo.

The Redline output can be mocked to the exact check Graeme verifies. We are demonstrating a
concept, not shipping a QA pass.

### Brand Voice Constraint (AI Language Policy)

The demo sits at the boundary of positioning and discovery content.

- **Not for**: homepage hero, pitch deck cover, tagline (positioning layer — no AI).
- **For**: LinkedIn video, sales email sequence, product explainer (discovery/explanatory layer
  where AI reference is permitted).

The framing copy stays clean: "Redline catches what jurisdiction-agnostic tools miss." No brand
comparison in the headline. Claude and Copilot appear in the video as workflow context, not as
targets.

---

## Next Steps

| Action | Owner | When |
| --- | --- | --- |
| Query Founder Memos to ground AI-complement frame before updating `positioning.md` | Ron | Before Phase 2 positioning refresh |
| Verify the Christchurch TC2 demo example is technically accurate for scripting | Graeme | Before demo is scripted |
| Produce concept video script (staged, pre-product) | John | Phase 1, after Graeme verification |
| Receive this note as context for "already using Copilot" ICP sub-segment | Mark | Before Skeleton Generator onboarding messaging |
