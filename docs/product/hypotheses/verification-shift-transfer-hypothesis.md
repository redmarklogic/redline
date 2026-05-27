# Hypothesis: The Verification Shift Transfers from Software to Civil Engineering

**Status**: In-testing. **Owner**: Mark. **Date**: 2026-05-27.
**Strategic link**: [Bet 2 — Pre-Review Mode Is the Paid Product Day-1](../strategy/strategic-bets.md), proposed Bet 7 — The Verification Shift.
**Related problem**: [AI Verification Bottleneck in Civil Engineering](../problems/ai-verification-bottleneck-civil-engineering.md)
**Related research**: [docs/research/software-development/20260526-accelerate-problem-diagnosis-ai-era.md](../../research/software-development/20260526-accelerate-problem-diagnosis-ai-era.md)
**Domain evidence**: [docs/knowledge/geotechnical/report-writing/ai-verification-shift-evidence.md](../../knowledge/geotechnical/report-writing/ai-verification-shift-evidence.md)

---

## Hypothesis Statement

Civil engineering firms that adopt AI writing tools for report generation without proportionally investing in verification infrastructure will experience the same quality degradation documented by DORA (2024-2026) in software development. Specifically: increased throughput paired with decreased stability, reviewer cognitive overload, and accelerated technical debt in the form of report quality erosion.

The transfer mechanism is structural, not analogical. In both domains, AI removes the generation bottleneck without modifying the verification architecture. The result is a growing mismatch between the volume and complexity of output that reaches human reviewers and the reviewers' capacity to verify it.

---

## What Would Disprove This

Within 12 months of consistent AI adoption at a civil engineering firm, the following signals should be observable if the hypothesis is true. Absence of these signals would disprove it:

1. **Average TR/PD review time per report increases** (not decreases) relative to pre-AI baseline. If AI adoption genuinely reduces reviewer burden without verification investment, review time per report should decrease. If it increases, the verification bottleneck is real.

2. **Client query rate or RFI rate on issued reports increases.** This is the change failure rate equivalent. If AI-generated reports contain errors at a higher rate than human-written reports, the downstream signal is more queries and more rework requests.

3. **Senior engineers report higher cognitive load during review.** Self-reported reviewer strain is a leading indicator. If senior engineers describe AI-generated reports as harder to review -- not easier -- the trust-model disruption is confirmed.

4. **Firms with weak pre-existing QA culture show quality degradation faster than firms with strong QA culture.** This is the amplifier effect. If AI adoption amplifies existing QA weaknesses rather than creating new ones, the pattern should be more severe in firms that were already struggling with review discipline. Quality-committed firms (per `docs/product/problems/quality-committed-firm-segment.md`) should degrade more slowly.

---

## Leading Indicators (Observable Now)

These signals are already confirmed and indicate the hypothesis is directionally correct before longitudinal data is available:

| Indicator | Status | Source |
|---|---|---|
| Industry press publishes concerns about AI report quality | Confirmed | Ground Engineering, March 2026 -- names "intelligent editor" role shift and junior training gap |
| PI insurers ask about AI use in reports | Confirmed | CEAS Indemnity Matters Issue 88, April 2026 -- Aon directly asks NZ consulting engineers about AI disclosure and report accuracy |
| Firms begin building or buying pre-review tools | Confirmed | Leading NZ consultancy building "Faultless" -- an AI pre-review tool -- confirming market-driven demand |
| Software engineering research documents the pattern | Confirmed | DORA 2024-2026 -- AI adoption increases throughput while degrading stability across surveyed teams |

Three of four leading indicators are confirmed from within the civil engineering domain. The fourth (DORA) is confirmed in the adjacent software engineering domain. The hypothesis is in-testing with strong directional support.

---

## If True

Redline's Pre-Review product has a compounding value story. The "without Redline" baseline worsens as AI adoption increases, making Redline's delta larger over time. This is not a one-time efficiency gain -- it is a widening gap between firms with verification infrastructure and firms without it.

Thought leadership positioning at the intersection of software engineering verification research (DORA/Accelerate) and civil engineering practice is defensible and timely. No competitor in the geotechnical AI space is making this connection explicitly.

The Pre-Review product roadmap gains urgency: the longer firms adopt AI without verification infrastructure, the deeper the quality debt accumulates. Early movers in verification tooling capture the market before the problem becomes normalised.

---

## If False

The civil engineering domain has structural differences that prevent the software pattern from transferring. Plausible structural differences include:

- **Regulatory review gates.** Council and insurer review may catch errors that, in software, would reach production undetected. If external reviewers function as an effective safety net, the internal verification bottleneck may not produce observable quality degradation.
- **Professional liability.** Personal liability for the signing engineer may create sufficient individual incentive to maintain review rigour regardless of AI adoption pressure. Software engineers do not carry personal professional liability for code defects.
- **Smaller document volumes relative to code.** A civil engineering firm produces hundreds of reports per year, not millions of deployments. The statistical signal may be too weak to detect at the firm level.

If false, Redline's value proposition remains valid -- Pre-Review still saves reviewer time on compliance mechanics. But the compounding story (the "without Redline" baseline worsens over time) and the thought leadership angle (DORA transfer) do not hold. The positioning reverts to a static efficiency gain rather than a widening gap.

---

## References

- `docs/research/software-development/20260526-accelerate-problem-diagnosis-ai-era.md`
- `docs/knowledge/geotechnical/report-writing/ai-verification-shift-evidence.md`
- `docs/product/strategy/strategic-bets.md` (Bet 2, proposed Bet 7)
- `docs/product/problems/quality-committed-firm-segment.md` (amplifier effect -- quality-committed vs. throughput firms)
- `docs/product/problems/ai-verification-bottleneck-civil-engineering.md`

---

## Next Step

Ron should assess whether the Verification Shift warrants a standalone Bet 7 in `strategic-bets.md` or whether it extends the existing Bet 2 framing. The evidence base is strong enough to formalise the bet; the question is whether it changes the kill criteria or adds new ones.
