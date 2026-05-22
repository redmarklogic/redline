# Pre-Review UX — Domain Perspective on Review Workflow Patterns

**Sub-domain**: report-writing
**Last verified**: 2026-05-22
**Confidence**: practitioner-grounded
**Sources**: 25+ years in a large civil engineering consultancy; cross-referenced with
playbook-driven review research, engineering-reports-vs-legal-documents research,
positioning-language memo, parameter-completeness-checking research

## Summary

Domain review of Matt's Pre-Review UX design reference note
(docs/product/design/pre-review-ux-references.md). Documents how senior geotechnical
reviewers actually work, the finding taxonomy they use, the disposition workflow they
need, and four workflow patterns missing from the initial design reference.

## Key Facts

### 1. Review is multi-pass, not linear

1. Senior reviewers perform at minimum three passes at different levels of abstraction:
   structural scan (are all sections present?), technical coherence (do conclusions follow
   from data?), and detailed checking (specific values, clause references, liability
   language).

2. Different reviewer roles (BIS/PC, Technical Reviewer, Project Director, SME/CoTE) see
   different subsets of findings. The UX must support filtering by concern type.

3. A GIR review is a session lasting 2-4 hours, not a one-shot read. Progress tracking
   ("7 of 12 sections reviewed, 4 findings undispositioned") is essential.

### 2. Finding taxonomy is category-first, not severity-first

4. Four finding categories by consequence:
   - **Liability exposure**: language or missing clauses affecting legal position
     (e.g., missing limitation clause, absolute language like "ensure", "guarantee")
   - **Technical defensibility**: engineering substance affecting whether conclusions
     are supported (e.g., unsupported conclusions, missing design-type-specific parameters)
   - **Standards compliance**: superseded, withdrawn, or incorrect standard references
   - **Mechanical/formatting**: style, structure, presentation issues

5. These categories are not severity levels — they are fundamentally different concern
   types. Primary grouping should be by category; colour (RAG) is a secondary visual cue
   within categories, not the primary taxonomy.

### 3. Disposition workflow requires six options

6. Required disposition options:
   - **Agree**: finding valid, report will be amended
   - **Disagree**: false positive, tool got it wrong
   - **Not Applicable**: correct in general but does not apply to this project
   - **Accepted Risk**: deviation is intentional and documented — distinct from Disagree
     (tool is wrong) and Not Applicable (rule does not apply). Has PI implications.
   - **Requires Discussion**: cannot be resolved by one reviewer; needs dialogue
   - **Deferred**: acknowledged, will be addressed in later revision

7. "Accepted Risk" is the most important addition because engineering practice commonly
   and legitimately deviates from standards with documented justification. The system
   must distinguish informed deviation from false positive.

8. Every disposition needs a free-text annotation field for the reviewer's justification
   or commentary. These annotations form part of the QA record and must be exportable.

### 4. Four missing workflow patterns

9. **Section-anchored findings**: findings must be grouped by report section as the
   primary view, not presented as a flat list sorted by severity. Reviewers read reports
   section by section.

10. **Progress tracking**: review is a session; the tool must track which sections have
    been reviewed and how many findings remain undispositioned.

11. **Finding confidence/provenance**: reviewers must know whether a finding comes from
    deterministic rule checking (high confidence) or LLM judgment (lower confidence).
    Attention calibration differs for each.

12. **Exportable review record**: dispositions, annotations, and findings must be
    exportable as a structured document (PDF, DOCX, or CSV) to attach to the project QA
    file. If findings live only in a web interface, they are disconnected from actual
    workflow.

### 5. Citation model needs a third type

13. Two citation types identified by Matt are correct:
    - Source citation (links to standard/rule that triggered the finding)
    - Location citation (links to where in the report the issue was found)

14. Third type missing: **cross-reference citation** linking two locations within the
    user's report where an internal inconsistency was found. Internal consistency
    checking is a major part of GIR/GBR review.

15. All standard citations must include the edition year (e.g., "NZS 4431:2022" not
    "NZS 4431"). Standards get superseded; the year disambiguates.

### 6. Accept All must be killed or heavily gated

16. "Accept All" in engineering review defeats the purpose of human oversight. Recommend
    removing it entirely. If retained, gate behind a confirmation that lists every
    finding being accepted — forcing the reviewer to read what they are accepting.

### 7. Tool boundary: completeness vs correctness

17. The tool should check "is this item present?" (legitimate completeness check) but
    must not check "is this item correct?" (engineering judgment). Example: "No Factor
    of Safety stated" is legitimate. "Factor of Safety = 1.2 may be insufficient" is
    overstepping.

18. High false positive rate is the primary adoption killer. Precision matters more than
    recall for senior reviewer time. A reviewer who must dismiss 30 false alarms to find
    3 real issues will stop using the tool after the second report.

## Standards Referenced

None directly. This document addresses review workflow UX patterns, not specific
standards compliance.

## Open Questions

1. How should the export format integrate with existing firm QA systems? Different firms
   use different project management and document control platforms (Aconex, ProjectWise,
   SharePoint). The export must be format-agnostic enough to attach to any system.

2. Should the section-anchored view use the document's actual section numbering (which
   varies by firm template) or a normalised structure? This has architecture implications.

3. How does the confidence/provenance indicator interact with the finding taxonomy? Are
   all mechanical findings inherently high-confidence? Can LLM judgment findings be
   high-confidence in some cases?

## Further Reading

- [Playbook-driven review research](../../research/20260426-playbook-driven-review-geotechnical-adaptation.md) — full mapping of legal playbook concept to geotechnical review
- [Engineering reports vs legal documents](engineering-reports-vs-legal-documents-domain-distinctiveness.md) — why geotechnical review is fundamentally different from legal-document review
- [Positioning language memo](memo-positioning-language-reviewer-sensitivity.md) — why framing matters for reviewer adoption
