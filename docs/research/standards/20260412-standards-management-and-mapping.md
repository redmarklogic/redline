# Standards Management and Mapping in Engineering Consultancies

**Date**: 2026-04-12
**Research question**: How do engineering consultancies organize, curate, tag, navigate, and maintain their library of standards (including supersession management), and how do they map a specific problem domain (e.g., designing a dam in Christchurch) to relevant standards and clauses?
**Actor**: an intermediate civil engineer building a standards registry for an AI tool.
**Redline domains**: 02-standards-registry, Report Skeleton Generator.

---

## Summary

Engineering consultancies generally lack centralized, digitally tagged, or relational databases for technical standards. Instead, local municipal bodies (like the Christchurch City Council) structure their standards by Asset Type and categorize them into Planning, Design, and Construction. Internally, private consultancies curate their technical requirements through decentralized intranet pages ("Knowledge Shots") and by embedding the latest standards directly into corporate document templates curated by Technical Directors (TDs). Superseded standards are managed via a strict "No Recycling" rule for old reports. Mapping a specific problem domain (e.g., designing a dam in Christchurch) to a list of relevant standards is fundamentally a human-driven process, relying on Subject Matter Experts (SMEs) to navigate fragmented legislative, client, and consenting authority requirements.

## Findings

### Organization, Curation, and Tagging of Standards
Regulatory municipalities, such as the Christchurch City Council (CCC), organize their master rulebook (the Infrastructure Design Standard or IDS) strictly by **Asset Type** (e.g., Part 4: Geotechnical, Part 5: Stormwater) [Source: 2]. Within those parts, standards are tagged into distinct categories: Planning and Policy (e.g., District Plans) [Source: 3], Design (e.g., New Zealand Standards) [Source: 4], and Construction [Source: 5].

Conversely, private engineering firms operate with a "messy reality." They do not maintain a highly tagged database. Instead, standards are organized practically through:
1. **Embedded Project Templates**: Hardcoded into discipline-specific templates via central platforms like Templafy. These contain pre-written prompts natively aligned with current standards [Source: 3, 6, 7].
2. **Knowledge Shots**: Short, targeted internal guidance pages hosted on company intranets with curated referral lists [Source: 4, 5].

### Responsibility for Curation
In municipal organizations, standards are written by Technical Services and asset managers [Source: 6]. Within private consultancies, curation is strictly divided by domain: **Technical Directors (TDs)** and **Centres of Technical Excellence (CoTEs)** continuously update project templates to manage risk and reflect best practices [Source: 3]. On a specific project, identifying and legally formalizing the correct standards (the "Inputs to the Design") is the responsibility of the Geoprofessional or Principal Designer, who signs the Producer Statement [Source: 7, 8, 9, 10].

### Handling Superseded Standards
Contracts legally enforce the "Latest Version" rule, and councils issue Amendment Summaries that explicitly track deleted, updated, or superseded clauses [Source: 11, 13, 14, 15]. 

Because private consultancies lack automated digital registries to flag outdated clauses, they manage supersession risk via strict procedural workflows. Most notably, they enforce a **"No Recycling" rule**, forbidding engineers from copying old reports [Source: 3]. Engineers are forced to generate a new document through Templafy for every project, ensuring they are automatically working from a template that the TDs have updated with the most current, non-superseded standards and legal caveats [Source: 3, 13].

### Mapping a Problem Domain to Relevant Standards
There is no automated digital mapping tool in current practice. Instead, the process is manual and layered:
1. **The Domain Index**: Municipal guidelines effectively act as a mandatory index. For example, to design wastewater infrastructure, the engineer navigates to the relevant IDS Part, which features a "Referenced Documents" section mapping the problem domain to specific AS/NZS standards [Source: 16, 17]. 
2. **Task-to-Standard Checksheets**: Physical tasks on site map to clauses via Contract Quality Plans (CQPs) and Audit & Test Schedules [Source: 20, 21, 22].
3. **The SME Requirement**: Formal Project Management (PM) guidance dictates that to identify exactly which industry, building, and design standards apply to a novel scenario, the engineer must "Check with the subject matter expert [SME] from the relevant discipline to understand these requirements." The standards are heavily fragmented across legislative layers, owner rules (e.g., Waka Kotahi), and consenting authorities [Source: 14].

## Implications for Redline
The current human-led approach is non-scalable, exposing the `02-standards-registry` concept's critical value proposition. To succeed, the AI standards registry must digitize the "SME Requirement" and the "Domain Index". 
- Instead of static templates or intranet generic links, the `skeleton-generator` should dynamically filter Redline’s Standards Registry based on client (e.g., Waka Kotahi vs. CCC), Asset Type, and Location (Christchurch vs. Auckland).
- Redline's AI must replace the "No Recycling" workflow constraint: tracking supersession should happen at the registry level with AI flagging outdated clauses directly in the generated skeleton, thus freeing the human engineer from checking Amendment Summaries sequentially.
- The ontology of the Standards Registry should mimic the municipal tagging approach: `Asset Type`, `Category (Planning/Design/Construction)`, and `Issuing Authority`.

## Open Questions
- How should the AI Standards Registry programmatically trace amendments or superseded versions if national bodies do not offer machine-readable APIs for their code updates?
- Who within the organization acts as the "TD" to approve the AI-generated mappings to the Standards Registry?

## Glossary

| Term | Definition |
|---|---|
| IDS (Infrastructure Design Standard) | A municipal master design rulebook used as the basis of compliance for land development and capital works. |
| Producer Statement | A formal certification signed by an engineer verifying that the design compliance maps to specific standards and codes (Inputs to the Design). |
| CQP (Contract Quality Plan) | QA documentation where engineers use an Audit & Test Schedule to map physical tasks to specific standard references and numerical acceptance criteria. |
| SME (Subject Matter Expert) | An individual with deep, specialized knowledge in a specific technical area (e.g., coastal engineering, structural design). |
| CoTE (Centre of Technical Excellence) | Internal enterprise groups of industry-recognized technical experts and emerging leaders who guide solutions to difficult technical issues. |
| TD (Technical Director) | A senior technical leader responsible for the quality, risk management, and template curation of a specific discipline's outputs. |
| Knowledge Shot | A short, targeted internal guidance page or article hosted on the company intranet curating professional references. |
| Templafy | An enterprise document generation platform that centrally houses all approved corporate templates. |

## Sources Consulted

| Notebook | Queries asked | Citations returned |
|---|---|---|
| Engineering Standards | 1 | [Source: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22] |
| Geotechnical Engineering Report Workflows and Standard Procedures | 1 | [Source: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14] |
