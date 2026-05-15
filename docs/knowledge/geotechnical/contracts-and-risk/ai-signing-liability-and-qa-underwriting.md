# AI Signing Liability and QA as an Underwriting Factor

**Sub-domain**: contracts-and-risk
**Last verified**: 2026-05-14
**Confidence**: cross-referenced
**Sources**: Risk Assessment in Engineering notebook, Geotechnical Report Workflows notebook, CEAS Indemnity Matters Issue 88 (April 2026)

## Summary

When an engineer signs a report containing AI-generated content, their personal liability exposure under PI (Professional Indemnity) insurance is real and potentially unmitigated. QA processes are a confirmed underwriting factor in NZ PI renewals, but the renewal question was designed for commercial-layer failures (scope, conditions, contracts) and was not designed to catch AI-specific technical content failures. These are structurally different failure modes. A systematic, auditable pre-review layer addresses the gap the renewal question cannot reach.

## Key Facts

1. Signing or sealing a document "not actually prepared or checked by the practitioner" constitutes professional misconduct under engineering regulations. The standard of care is: you signed it, you are responsible for its content. [Risk Assessment in Engineering, citations 7-8]

2. An individual engineer can be held personally liable in tort for negligence. To protect signing engineers, firms must ensure their PI policies explicitly cover both the corporate entity and individual employees. [Risk Assessment in Engineering, citations 1-3]

3. If AI-generated text contains "absolute" or "guarantee" language — which AI models naturally produce — it can elevate the standard of care from negligence to strict liability, which is typically excluded from PI policies. This can void coverage even where the engineer was not negligent in the ordinary sense. [Risk Assessment in Engineering, citations 4-5]

4. Insurers assess QA process descriptions as part of premium setting. "It is beneficial to risk management if the insured has procedures to check the quality of its designs." [Risk Assessment in Engineering, citation 11]

5. The QA question on NZ PI renewal forms was designed around commercial-layer failures: signing bespoke conditions, failure to have upfront scope conversations, absence of standard liability caps. Craig Lewis (CAS) confirmed it was introduced 6-8 years ago to drive those disciplines. [CEAS Indemnity Matters Issue 88, Q&A session]

6. The commercial QA layer — scope, conditions, LOE (Letter of Engagement), client conversations — is genuinely how large NZ geotech firms think about QA. "One of our best project management mitigations is to ensure that the scope of services agreed with our client is tight and unambiguous." A tight scope is explicitly relied upon to "defend spurious PI claims." [Geotechnical Report Workflows, citations 10-11]

7. The technical QA layer — checking inputs, arithmetic, methodology, and AI output — is a separate, parallel process managed by a Technical Reviewer and Component Reviewer (an engineer of equal or superior knowledge to the author). [Geotechnical Report Workflows, citation 4]

8. Three PS4 (Producer Statement — Construction Review) practice advisories were issued by CEAS, Engineering NZ, and ACE NZ in the 18 months to October 2025, following Building Consent Authority concerns about altered and inadequate PS4 scope qualifications. This signals a systemic signing-liability problem in the profession that predates AI. [CEAS Indemnity Matters Issue 88, page 3]

9. The "check AI like a graduate's work" framing (Craig Lewis, CAS roadshows 2026) is useful as a cultural prompt but misleading as a legal or practical standard. A graduate's mistakes stay within the domain of plausible engineering. AI can fabricate references to non-existent standards, generate unenforceable baseline language, or conflate ground properties with ground behaviour — failure modes that require independent verification to catch, not just a plausibility read. [Practitioner assessment — not notebook-grounded]

10. In small NZ firms (5-15 staff), the principal is often simultaneously author, reviewer, and signer. The checking standard is materially less rigorous than the three-tier standard documented in large-firm QMS guides. The grad-checking analogy assumes a consistent standard that does not exist across firm sizes. [Practitioner assessment — not notebook-grounded]

## The Structural Gap

The QA renewal question asks: "do you have a QA process?" It was designed to detect firms with no formal review at all.

It was not designed to ask: "can you demonstrate what your AI-assisted QA process actually checked, and when, before the signing engineer signed?"

These are different questions. The first is a process-existence check. The second is an audit trail check. The insurance industry has not yet asked the second question at scale — but the Indemnity Matters newsletter signals the leading edge of that question arriving.

## Standards Referenced

- Professional Engineers Act (Ontario, as cited in Risk Assessment notebook) — seal, sign, and date every final report; misconduct to sign documents not prepared or checked by the practitioner
- CEAS PS4 Practice Advisory (October 2025) — scope of construction monitoring; defining limits of PS4 sign-off
- CEAS Indemnity Matters Issue 88 (April 2026) — QA as underwriting factor; AI cautionary tales for engineering profession

## Open Questions

1. When NZ geotech firms complete the QA section of PI renewal forms, do they describe their actual process or provide boilerplate? No primary research has been conducted with NZ insurers or firms on this specific question. The coffee meeting with Aon (scheduled post-June 2026) is the designed test.

2. Has any NZ insurer yet inserted an explicit AI-use exclusion clause or condition into a PI policy for an engineering firm? Not confirmed as of May 2026.

3. What would a "demonstrable AI-content audit trail" need to contain to satisfy an insurer in a claim where the signer argues they checked the AI output? No industry guidance exists yet.

4. Do NZ-specific CPEng obligations (Engineering NZ) differ materially from the Ontario Professional Engineers Act provisions cited in the Risk Assessment notebook on the personal liability of signing engineers?

## Further Reading

- I have not verified these sources, but they may contain relevant material:
  - CEAS Members' area, Guides and Manuals — PS4 Practice Advisory (October 2025) and prior advisories
  - Engineering NZ Practice Note 19 — Engineers and the Law
  - ACENZ conditions of engagement and liability limiting guidance
