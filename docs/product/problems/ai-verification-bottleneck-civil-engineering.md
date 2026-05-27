# Problem Statement: The AI Verification Bottleneck in Civil Engineering

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-05-27.
**Strategic bet**: [Bet 2 — Pre-Review Mode Is the Paid Product Day-1](../strategy/strategic-bets.md), proposed [Bet 7 — The Verification Shift](../strategy/strategic-bets.md)

---

## Context: Why This Problem Exists Now

AI writing tools -- ChatGPT, Claude, Microsoft Copilot, and firm-specific tools like EMMA and ProjectGPT -- have dramatically increased report generation speed for civil engineering consultancies. Junior and intermediate engineers can now produce first drafts in hours rather than days.

Verification capacity has not scaled proportionally. The senior engineers who review reports (Technical Reviewers and Project Directors) are the same people who reviewed reports before AI adoption. Their numbers have not grown. Their cognitive bandwidth has not expanded. What has changed is the volume, size, and difficulty of what reaches their desk.

DORA 2024-2026 research documents the identical pattern in software engineering: AI adoption increases throughput while degrading stability. The civil engineering domain is experiencing the same dynamic, with the added complication that professional liability attaches personally to the signing engineer.

---

## Target User

Senior geotechnical engineer in a Technical Reviewer (TR) or Project Director (PD) role at a civil engineering consultancy adopting AI tools for report generation. These engineers are typically 15-30 years post-graduation, carry professional indemnity responsibility, and are the scarcest, most expensive people in the firm. They review reports before submission to councils, insurers, and clients.

The user segment spans firm sizes -- Small (5-50 staff), Medium (50-200), and Large (200+) -- because the verification bottleneck is structural, not organisational. Larger firms may have more reviewers, but they also have more authors generating AI-assisted output.

---

## Core Pain

Three forces compound simultaneously when a firm adopts AI writing tools:

1. **Higher volume of reports to review.** AI-assisted authors produce drafts faster, increasing the throughput that reaches the review queue. The reviewer's calendar has not expanded.

2. **Longer reports per deliverable.** AI tools generate verbose, comprehensive-looking text. Reports that were previously 30 pages arrive at 50. Every additional page costs reviewer attention.

3. **Higher cognitive load per page.** This is the non-obvious multiplier. When a senior engineer reviews a report written by a known human author, they apply a trust model built over time. They know where that author is strong, where they tend to cut corners, and where to focus attention. With AI-generated text, that trust model does not exist. Errors are not correlated with style, confidence, or fluency. The reviewer cannot skim. Every sentence is, in effect, from an unknown author with no track record.

The compound effect is multiplicative, not additive: Volume x Size x Cognitive-load-per-page. A reviewer who previously reviewed 3 reports per week at 30 pages each with a known-author trust model now faces 5 reports per week at 50 pages each with no trust model. The total review burden has not doubled -- it has increased by an order of magnitude in effective cognitive demand.

This creates unsustainable strain on the scarcest, most expensive people in the firm.

---

## AI-Specific Error Classes

AI-generated text introduces error types that differ from human errors and require different reviewer attention patterns:

- **Fabricated citations that look authoritative.** An AI tool might cite NZS 4407:2015 for SPT testing -- a roading standard, not a geotechnical one. The citation format is correct. The standard number is real. The application is wrong.
- **Correct-range-but-wrong values.** A plausible SPT N-value attributed to the wrong borehole. The number passes a sniff test. The provenance is fabricated.
- **Method-correct but context-wrong.** A valid design method applied to the wrong soil classification. The methodology section reads well. The input assumptions are unsupported by the site data.
- **Fluent interpolation beyond the data.** Ground conditions between investigation points stated as fact rather than inference. AI generates confident prose about what lies between boreholes because it does not distinguish observation from interpretation.

These errors are specifically difficult to catch because they are embedded in fluent, well-structured prose. Human errors tend to correlate with writing quality -- a sloppy draft signals low confidence. AI errors do not correlate with writing quality at all.

---

## What Makes This Hard

The verification burden increases non-linearly with AI adoption. Each additional AI-assisted author in the firm increases the review queue without adding any review capacity. The compounding is structural: more reports, each longer, each harder per page.

The people who bear the cost (senior engineers) are not the people who benefit from the generation speed (junior engineers and authors). The author experiences AI as a productivity gain. The reviewer experiences AI as a workload increase with higher stakes per page.

Traditional QA processes -- TR/PD review gates with a single senior sign-off -- were designed for human-authored, human-paced report production. The implicit assumption was that report volume would be constrained by author capacity. AI removes that constraint without modifying the review architecture.

The problem is invisible in productivity metrics. If the firm tracks "reports issued per month," AI adoption looks like a success. The quality signal -- reports that generate client queries, RFIs, or require reinterpretation -- lags by weeks or months. By the time the signal surfaces, the firm has normalised a higher error rate.

---

## Evidence

The following evidence sources ground this problem statement:

1. **DORA 2024-2026 research** documents the identical pattern in software development: AI adoption increases throughput while degrading stability. The mechanism is the same -- faster generation without proportional verification investment. DORA's AI-specific findings confirm that teams using AI without verification infrastructure show higher change failure rates.

2. **Ground Engineering magazine (March 2026)** names the "intelligent editor" role shift and the junior engineer training gap. Industry press is already articulating the problem, which indicates it is not a theoretical concern.

3. **Leading NZ consultancy internal QA documentation** confirms the pre-existing bottleneck before AI adoption: "reviewers are meant to be safety nets, but if the author doesn't contribute a solid foundation, the reviewer is forced to pick up the pieces." AI tools amplify this dynamic because the author's draft looks polished regardless of whether the engineering foundation is solid.

4. **The same NZ consultancy is building "Faultless"** -- an AI pre-review tool -- confirming that market participants have independently identified this bottleneck and are investing in solutions. This is demand validation from inside the industry.

5. **CEAS Indemnity Matters Issue 88 (April 2026)** documents PI insurers asking NZ consulting engineers about AI use in reports. The insurance industry is actively probing for the quality risk this problem describes.

---

## The Asymmetry That Creates the Opportunity

The firms most vulnerable to this bottleneck are the same firms Redline targets: firms that care about report quality but lack the resources to build internal verification infrastructure.

Large firms (Tonkin + Taylor, WSP, Beca) can build internal tools like Faultless. Small and medium firms cannot. They will either accept higher error rates, overload their senior engineers until they leave, or buy a verification layer from an external vendor.

Redline's Pre-Review product addresses this bottleneck by shifting AI-powered quality checks to the author side, reducing the compliance burden that reaches the reviewer. The reviewer still reviews -- but the reports that reach them have already been checked for the compliance mechanics that consume 55% of current review time (per Graeme's benchmark, 2026-05-14).

---

## Measurable Outcome

**Primary metric**: Senior engineer review time per report deliverable. A successful intervention reduces the time a TR/PD spends per report by shifting compliance verification to the author side.

**Change failure rate equivalent**: Reports issued that generate client queries, RFIs (Requests for Information), or require reinterpretation after submission. This is the quality signal that lags behind the throughput increase. A firm experiencing the verification bottleneck will see this rate increase as AI adoption grows -- unless verification infrastructure is added.

---

## Next Step

This problem statement grounds the proposed Bet 7 (The Verification Shift) and strengthens the existing Bet 2 (Pre-Review as paid product). The hypothesis that this software-engineering pattern transfers to civil engineering is formalised in `docs/product/hypotheses/verification-shift-transfer-hypothesis.md`. Ron should review whether this warrants a new strategic bet or an extension of Bet 2.
