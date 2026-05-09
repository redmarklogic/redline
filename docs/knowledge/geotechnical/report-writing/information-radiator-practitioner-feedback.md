# Information Radiator — Practitioner Feedback on Pre-Review Summary Design

**Sub-domain**: report-writing
**Last verified**: 2026-05-06
**Confidence**: practitioner-grounded
**Sources**: 25+ years in a large civil engineering consultancy; cross-referenced with playbook-driven review research (2026-04-26)

## Summary

Mark proposed three candidate designs for an "information radiator" — a quick-glance summary showing what Redline has checked and what state the report is in before section-level review begins. Graeme's practitioner feedback strongly favours Candidate B (Enhanced Document Control Page on page 2 of the .docx) because it matches existing reviewer behaviour, works in all delivery formats, and requires zero workflow change.

## Key Facts

1. Senior reviewers open the document first, every time. A web summary page before the document (Candidate A) will be skipped. The summary must be inside the document.
2. Page 2 (document control) is already the reviewer's first substantive stop — cover page, then page 2 for provenance. Adding coverage summary extends provenance rather than introducing a new concept.
3. Page 2 has a strong practical convention of being one page. If coverage summary pushes it to two pages, move the summary to a standalone page 3 between document control and table of contents. Do not displace revision history or signature block.
4. "Not checked — engineering judgment required" is the correct framing for sections outside Redline's rule library. Do not soften to "Outside Redline's current scope" — that sounds like a product apology. The honest status indicator builds trust.
5. Coverage table should use top-level sections only. Sub-section detail belongs in Word comments (Level 3 of the information hierarchy). Exception: if fewer than 6 top-level sections, go one level deeper.
6. Flag severity labels should be "Fix" / "Check" / "Note" — these map to how reviewers actually mark up documents, not system-centric labels like "critical / advisory / informational."
7. The coverage summary should appear in draft-under-review versions only, not in issued reports. "4 sections not checked" in a contractual document creates litigation exposure.
8. Senior reviewers never review sequentially. They read conclusions first, then jump to high-risk sections. The coverage table's value is highest when it highlights where to look first (flag severity ordering or visual distinction).
9. Web overlay panels (Candidate C) require web-based review, which conflicts with current practice (Word/PDF/print). Progress bars (5/8 flags resolved) risk implying review is a task-completion exercise rather than an engineering judgment exercise.

## Missing Elements Mark Should Address

- **Reviewer's note field**: A column for the reviewer to record their own status after reviewing each section (turns the radiator from read-only to a working tool).
- **Scope of checking statement**: One-line header stating what rules/standards Redline checked against (e.g., "Checked against: Firm X Template v3.2 + NZS 3604:2011").
- **Revision context**: For Revision B+ reports, indicate what changed since the previous revision so the reviewer can focus on deltas.
- **Trust calibration**: Flag accuracy feedback mechanism (agreed/dismissed) to support the first 3-5 reports where reviewers manually verify every flag.
- **Rule ID suppression**: Individual rule IDs (e.g., "GBR-LANG-01") should be hidden from the coverage summary (Level 4 audit trail only, not Level 2).

## Additional Observations

- The "structural orientation" vs "state orientation" distinction Mark draws is exactly correct. Templates save 30-40% of review time through structural familiarity alone. The radiator adds state orientation on top.
- The radiator is used twice: once at the start of review (orientation) and repeatedly during review (progress reference). Design must support easy navigation back to page 2 (bookmark, hyperlink from TOC).
- Candidate B is the strongest option for KR2 interview testing because it can be tested with a static mockup placed in front of a reviewer alongside a standard page 2 (status quo comparison).

## Open Questions

- How compact can the coverage table be made while retaining the summary line, section-by-section status, flag counts, and scope-of-checking statement — all on one page?
- Should the coverage table be ordered by section number or by flag severity? (Practitioner preference: flag severity, with "Fix" items at top.)
- What is the appropriate mechanism for stripping the coverage summary from the issued version? (Manual removal vs automated template macro.)

## Further Reading

- Playbook-driven review research: `docs/research/20260426-playbook-driven-review-geotechnical-adaptation.md`
- Positioning language memo: `docs/knowledge/geotechnical/report-writing/memo-positioning-language-reviewer-sensitivity.md`
