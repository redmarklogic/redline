# AI-Assisted Workflow Expansion Boundaries

**Sub-domain**: contracts-and-risk
**Last verified**: 2026-05-03
**Confidence**: cross-referenced
**Sources**: Geotechnical Engineering Report Workflows and Standard Procedures notebook; Geotechnical Baseline Reports (GBR) notebook; Risk Assessment in Engineering notebook; Engineers' Guide to Technical Communication notebook; Redline prior adjacent-market research.

## Summary

Legal-AI-style workflow expansion is plausible in geotechnical engineering only where the product supports document control, traceability, rule-based pre-review, and human reviewer efficiency. It crosses the professional boundary when it selects design parameters, sets contractual baselines, writes engineering recommendations, certifies compliance, or resolves conflicts between the author and reviewer.

## Key Facts

1. Structured pre-review is professionally plausible where the check is mechanical, rule-based, or evidence-preserving. The Report Workflows notebook describes a Rule Matrix for automated high-speed pre-flight checks covering mandatory sections, cross-reference integrity, numerical table checks, language, syntax, unit consistency, and formatting [Report Workflows, citations 2-8].
2. Firm-specific House Rules are plausible when they encode review standards as checks that a human author or reviewer resolves. The Report Workflows notebook describes Faultless as adding review comments directly in the document and maintaining version control of prompts, while pre-PD prompts support report review before Project Director review [Report Workflows, citations 4-5].
3. Word-native comments and tracked changes are not cosmetic. The Report Workflows notebook states that documents with tracked changes made by Business Integrated Services, Project Director, and Technical Reviewer are retained as evidence that review has been completed; substantive AI outputs, prompts, and enough information to recreate or validate calculations must be saved in the project folder with version control [Report Workflows, citation 3].
4. Technical judgement remains a human responsibility. The Report Workflows notebook separates mechanical pre-flight checks from analytical peer review and says Technical Reviewer work asks whether the report will survive professional peer review [Report Workflows, citations 5-8]. It also states that the Technical Reviewer checks that the right answer has been given to the right question and that component reviewers need knowledge equal to or above the author [Report Workflows, citation 2].
5. Geotechnical Baseline Reports (GBRs) are high-risk because they are contractual risk-allocation documents, not ordinary technical summaries. A GBR contains measurable contractual descriptions of anticipated subsurface conditions and helps administer Differing Site Conditions clauses [GBR, citations 1-5].
6. GBR wording checks are safe as flags, not as autonomous fixes. The GBR notebook says baseline statements must avoid imprecise words such as "may", "can", "might", "up to", "could", "should", "would", "some", "few", and "ranges from...to..."; it also says qualitative adjectives should be quantified or defined, and that baseline statements should use measurable parameters [GBR, citations 6-9].
7. Autonomous baseline setting is unsafe. The GBR notebook states that baseline statements can deviate from factual Geotechnical Data Report data only with engineering judgement and clear explanation, and that unrealistic or overly adverse baselines create unintended consequences [GBR, citations 24-30].
8. Risk-language checking is safe and valuable where it flags wording for human review. The Risk Assessment notebook says absolute words such as "all", "every", "ensure", "guarantee", "certify", or "safe" can elevate the standard of care from negligence to strict liability and may create uninsured warranty exposure [Risk Assessment, citations 1-5].
9. Limitation, standard-of-care, and third-party reliance clauses are suitable for presence and consistency checks, but final wording remains legal and engineering review territory. The Risk Assessment notebook says reports should include standard-of-care language, explain subsurface uncertainty, and restrict third-party reliance; it also warns that blanket disclaimers cannot simply erase reliance risk [Risk Assessment, citations 11-23].
10. Source citation and traceability are core professional controls. The Technical Communication notebook says engineers must cite borrowed information whether quoted, paraphrased, or summarised; reviews and edits are quality-control steps for all documents; and formal reports may require authoritative expert review [Technical Communication, citations 1-14].

## Standards Referenced

- No new engineering standard was interpreted in this assessment.
- Existing Redline architecture remains governed by ADR-006: the Standards Knowledge Store is internal-only and citation-only, storing clause references and applicability mappings rather than full proprietary standards text.

## Open Questions

- I do not know, from the geotechnical notebooks, the detailed product behaviour of Robin AI, Legora, or Microsoft's Word Legal Agent. Those are outside the geotechnical NotebookLM corpus unless separately researched.
- I do not know whether NZ/AU insurers or regulators have a settled position on AI-assisted geotechnical review, because the Risk Assessment notebook did not contain AI-specific professional-liability guidance.
- I do not know the senior-engineer time cost of creating and maintaining firm House Rules. Prior playbook research identified this as an evidence gap.
- I do not know whether the tracked-changes and project-file evidence practice described in the Report Workflows notebook is universal across NZ/AU geotechnical firms; it is strong single-firm workflow evidence, not a cross-industry survey.

## Further Reading

- `docs/research/20260426-legal-ai-adjacent-market-signal.md`
- `docs/research/20260426-playbook-driven-review-geotechnical-adaptation.md`
- `docs/knowledge/geotechnical/ai-gbr-liability-assessment.md`
- `docs/adr/adr-006-standards-knowledge-store-citation-only-internal-architecture.md`
