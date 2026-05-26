# Report Drafting Initiation Workflow

**Date**: 2026-04-12
**Research question**: At what point in the typical geotechnical workflow does the engineer start writing the report (e.g., the GIR)? Is it before the desktop study, or after? If it is before, is it because the document skeleton contains comments or prompts (like from standards) on what needs to be included?
**Actor**: an intermediate civil engineer analyzing the workflow for writing a Geotechnical Interpretive Report (GIR).
**Redline domains**: Document Generation, Document Process (from project context).

---

## Summary

In the standard geotechnical workflow, the engineer nominally starts "writing" the report—specifically, building the document skeleton—**before** the desktop study and before any fieldwork begins. This initial drafting is not substantive engineering content, but rather the construction of a highly structured template populated with guidance notes, placeholders, and mandatory checklists that dictate the required research and fieldwork.

## Findings

### Early Skeleton Generation
In the official workflow, the engineer starts "writing" the report before the desktop study and before any fieldwork begins [Source: Geotechnical Engineering Report Workflows and Standard Procedures]. However, they are not writing the substantive engineering content yet. Instead, they are building the report skeleton. Internal training explicitly warns engineers to "pause before you start typing" and strictly mandates planning the document's structure before opening a blank Word document. The workflow dictates that the author must read the LOE/RFP, understand the client's scope, and immediately generate the report skeleton.

### Purpose of Early Skeletonization
We build the skeleton early because the corporate report templates are highly structured and contain built-in guidance notes, placeholders, and mandatory checklists that dictate what the engineer must do:

1. **Establishing the "Touchstone"**: The very first step in generating the skeleton is completing a section called "What is the client seeking? (scope of works)". This acts as the report's "touchstone"—a master checklist detailing the client's exact requirements, pain points, mitigations, and deliverables. By writing this before the desktop study, the engineer ensures that all subsequent research and fieldwork are tightly focused on answering the client's specific questions.
2. **Inserting Placeholders and Prompts**: The template actively guides the engineer by providing instructional prompts (e.g., "Guidance Note: Text describing a soil profile can be very difficult to read. Table to describe soil profile recommended"). The skeleton is populated with empty tables and bolded placeholder questions for interpretive content (like design parameters or hazard assessments). These placeholders act as a roadmap, telling the engineer exactly what data they need to hunt for during the desktop study and site investigations.
3. **The "Sense Check" Quality Gate**: Before the engineer is allowed to heavily draft the desktop study findings or factual data, they must submit this skeleton to the PM or PD for a "sense check". The PD/PM reviews the customized sub-headings to verify that all the client's points from the LOE have been captured. This prevents the "formatting nightmares" and massive structural rework that happens when an engineer dives straight into writing without a plan.

Once the skeleton and placeholders are approved, the engineer proceeds to conduct the desktop study and fieldwork, returning to the document to replace the prompts with factual observations and interpretive engineering analysis.

## Implications for Redline
This reinforces the Redline tool's `01-skeleton-generator` concept. The prompt-driven, comment-laden skeleton is structurally intended to guide the human engineer’s desktop study and site investigation. Thus, the Redline skeleton generator must inject contextual prompts based on the project scope (e.g., specific clauses from standards) *before* factual data is populated, replicating this "touchstone" and "Sense Check" gate digitally.

## Open Questions
- How should the AI dynamically adapt the placeholders and prompts based on variations in the RFP or LOE?

## Glossary

| Term | Definition |
|---|---|
| GIR (Geotechnical Interpretive Report) | A technical document that applies professional engineering judgement to interpret subsurface data (like soils and groundwater) and assess ground hazards to support structural design decisions. |
| Desktop Study | An early phase of a project where engineers review existing, published geological information and historical records before any physical fieldwork or drilling begins. |
| LOE (Letter of Engagement) / RFP (Request for Proposal) | The legal, contractual documents that outline the project's scope, budget, and required deliverables. |
| PM (Project Manager) & PD (Project Director) | The senior staff responsible for managing the project delivery (PM) and acting as the commercial/legal safeguard for the company (PD). |

## Sources Consulted

| Notebook | Queries asked | Citations returned |
|---|---|---|
| Geotechnical Engineering Report Workflows and Standard Procedures | 1 | [Source: 1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16] |
