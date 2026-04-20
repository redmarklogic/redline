# Competitor Profile: Archie (Soil & Rock Consultants / SupaHuman)

**Last updated**: April 20, 2026
**Purpose**: Inform Redline product roadmap and competitive positioning

All claims tagged: `[Vendor]`, `[Independent]`, or `[First-person]`.

---

## What Is Archie?

**Archie** is a bespoke AI co-pilot for drafting geotechnical reports, built by
**SupaHuman** (an NZ AI integration agency) for **Soil & Rock Consultants** (NZ
geotechnical firm, ~50–100 employees, Auckland and Northland, est. 1987, CEO: Simon
Cupples). It is a custom configuration of SupaHuman's "AI Workspace" platform — not a
standalone product you can purchase. It integrates with Microsoft SharePoint and Teams.

Headline marketing claim: report preparation reduced from ~10 hours to ~20 minutes (24x
speed increase).

---

## Part 1 — Product Profile

### Features and Capabilities

Archie is a RAG-based drafting co-pilot embedded in a firm's Microsoft 365 environment.
It ingests raw field data and historical documents, then generates a report draft
section-by-section using custom prompts tuned to the firm's templates and standards.

| Feature | Description | Evidence quality |
|---------|-------------|-----------------|
| Input: field data and analysis results | Ingests structured/unstructured site investigation data (borehole logs, lab results, CPT/SPT outputs) | `[Vendor]` |
| Input: site photos and historic reports | Processes visual data and legacy text documents for historical site context | `[Vendor]` |
| Output: section-by-section draft | Generates the report in sequential sections, not a single monolithic pass | `[Vendor]` |
| Output: formatted client-ready report | Mirrors the firm's tone, engineering standards, and branding | `[First-person]` |
| Human step: review and sign-off | Engineers review the draft; senior staff focus on analysis and liability sign-off (claimed only) | `[Vendor]` |
| Integration: Microsoft SharePoint and Teams | Embeds into the firm's existing document management and comms ecosystem | `[Vendor]` |
| Integration: design and engineering software | Works within workflows including AutoCAD, Bluebeam, Civil 3D, BIM360, Excel | `[Vendor]` |
| Templates: universal standardisation | Enforces consistent branding and eliminates formatting inconsistency across projects | `[Vendor]` |

**Key observation**: The section-by-section drafting approach reduces hallucination risk by
decomposing the report into scoped sub-tasks. There is no demonstration of how the system
handles anomalous or contradictory field data — precisely where engineering judgment matters.

---

### Target Audience and Deployment

The tool targets mid-size engineering consultancies with sufficient report volume to justify
a bespoke integration build. Primary operators are junior-to-mid-level engineers; senior
engineers shift to a pure review and sign-off role.

| Audience dimension | Finding | Source |
|--------------------|---------|--------|
| Primary user role | Engineering staff responsible for data entry and initial drafting | `[Vendor]` |
| Reviewer role | Senior engineers focused on compliance, analysis, and liability sign-off | `[Vendor]` |
| Firm size | 50–100 employees, Auckland and Northland | `[Independent]` |
| Report volume / cadence | Not found | — |
| Onboarding / training | Deployed and delivering results "within weeks"; described as growing smarter over time | `[Vendor]` |

**Key observation**: The "weeks" deployment claim implies the platform is highly configurable
via prompt engineering, not significant back-end development. This is a thin technical moat.

---

### Value Proposition — Is the 24x Claim Credible?

The 10 hours → 20 minutes claim comes exclusively from vendor marketing and the firm's CEO.
No independent time-motion study exists. The 20-minute figure almost certainly refers only
to compute and prompt execution time, excluding pre-ingestion data structuring and the
mandatory post-generation professional review.

| Value claim | Claimed metric | Substantiated? | Source |
|-------------|----------------|----------------|--------|
| Speed improvement | 10h → 20min (24x) | No | `[Vendor]` |
| Tasks automated | Data ingestion, formatting, section-by-section narrative drafting | Partial | `[Vendor]` |
| Cost saving | Not found | — | — |
| Quality impact | "Council-ready" and "client-ready" outputs | No | `[Vendor]` |

**What the vendor claims**: Archie eliminates the 8–10 hour manual drafting process by
automating data ingestion, document formatting, and narrative generation.

**What independent sources confirm**: AI tools can materially accelerate document preparation
in engineering contexts, but no external party has audited this specific claim.

**What remains unverified**: The 20-minute figure, output quality and accuracy, and total
workflow time inclusive of pre- and post-AI human effort.

---

### Independent and Regulatory Reactions

No commentary specifically targeting Archie or Soil & Rock's methodology has been located
from councils, competing firms, or trade press. NZ's regulatory stance is technology-agnostic:
liability sits with the signing engineer, not the drafting method.

| Source | Author / Publisher | Stance | Key point | URL |
|--------|-------------------|--------|-----------|-----|
| AI in Professional Practice | Engineering New Zealand | Neutral | AI is permitted as a drafting assistant; it cannot make engineering judgments, ensure code compliance, or sign off work. The human engineer retains full liability. | [engineeringnz.org](https://www.engineeringnz.org/programmes/engineering-and-ai/ai-in-professional-practice/) |
| Resource consent guidelines | Auckland Council / NZ Government | Neutral | Geotechnical reports assessed on technical merit and Producer Statement credentials; no mechanism to flag AI-drafted text. | [fasttrack.govt.nz](https://www.fasttrack.govt.nz/__data/assets/word_doc/0019/17632/Appendix-A-Draft-Conditions-of-Consent-17-December-2025.docx) |
| Professional guidance | NZ Geotechnical Society (NZGS) | Not found | No public statement on automated report drafting tools located as of April 20, 2026. | — |

**Key observation**: Engineering NZ explicitly promotes structured prompting (RTF: Role,
Task, Format) and has an active AI Advisory Committee. The profession is monitoring, not
banning. The regulatory gap is both an opportunity and a future liability risk.

---

### Global Competitive Landscape

No direct competitor combines upstream data extraction with downstream narrative drafting
in a single multi-tenant product. Archie's bespoke agency approach is atypical.

| Tool | Company | Geography | Approach | Key differentiator vs Archie | URL |
|------|---------|-----------|----------|------------------------------|-----|
| Civils.ai | Civils.ai | Global | SaaS | Extracts and structures data from PDFs into AGS/Excel/GIS and 3D models; does not generate narrative reports | [civils.ai](https://civils.ai/blog/how-to-extract-data-for-geological-modeling/) |
| Groundhog | Open source | Global | Open (Python) | Automates geotechnical calculations and parameter validation; no language generation | [github.com/snakesonabrain/groundhog](https://github.com/snakesonabrain/groundhog) |
| Geoverse | Viridien | Global | SaaS | Regional-scale subsurface imaging and mineral exploration — entirely different use case | [viridiengroup.com](https://www.viridiengroup.com/expertise/satellite-mapping/balanced-cross-section-geology-validation-and-analysis) |

**Key observation**: No tool in the current landscape combines Civils.ai-style upstream data
extraction with Archie-style downstream narrative drafting. This is the gap.

---

## Part 2 — Strategic Follow-Up

### Pricing — What Does a SupaHuman Build Actually Cost?

No pricing figures are published, but the commercial model is confirmed: a base
organisational licence fee plus per-user charges — not a pure one-off bespoke build.
Clients pay ongoing platform costs on top of whatever the initial integration work costs.

| Pricing signal | Value or range | Source |
|----------------|---------------|--------|
| Published price | Per-user licensing plus a base organisational licence fee; exact figures unpublished | `[Vendor]` [AI Workspace service description](https://www.supahuman.com/legals/ai-workspace-service-description) |
| Contract value mentioned | Not found | — |
| Comparable agency rate | Not found | — |
| SupaHuman headcount | Exact number unpublished; led by three founders with a team of PhD-level AI engineers | `[Vendor]` [AI Forum NZ launch](https://aiforum.org.nz/2024/01/17/supahuman-ai-launches-in-new-zealand-ushering-a-new-era-in-ai-solutions/) |
| Published client case studies | 11 named; broader claim of 100+ AI projects delivered across ANZ | `[Vendor]` [aotearoaai.nz](https://www.aotearoaai.nz/programme/) |

**Most defensible estimate**: Hybrid of a base organisational licence fee plus per-seat
costs — not a one-off build fee. A firm pays ongoing per-user charges, not just upfront
capital expenditure. The base fee and per-seat rate remain entirely unpublished.

**What remains unknown**: Dollar value of the base licence, per-user monthly rate, and
the split between initial implementation cost and recurring licence cost.

---

### SupaHuman Deployments — Any Other NZ/AU Engineering Clients?

SupaHuman has published only one named engineering case study as of April 20, 2026.
Their broader portfolio is horizontal: education, retail, healthcare, and tourism — not AEC.

| Client | Sector | Geography | Use case | Source |
|--------|--------|-----------|----------|--------|
| Soil & Rock Consultants | Geotechnical engineering | NZ | Automated report drafting | `[Vendor]` [case study](https://www.supahuman.com/use-cases/from-10-hours-to-20-minutes-how-soil-rock-transformed-geotechnical-reporting-with-intelligence) |
| Mast Academy | Education | NZ | Automated NZQA course and assessment documentation | `[Vendor]` [case study](https://www.supahuman.com/use-cases/from-6-weeks-to-6-minutes-how-mast-academy-transformed-course-creation) |
| Jani-King | Commercial cleaning | NZ / AU | Prospect research: 20 min → 90 sec | `[Vendor]` [case study](https://www.supahuman.com/use-cases/prospect-research-from-20-minutes-to-90-seconds) |
| Carpet Court | Retail | AU / NZ | Warranty claims assessment automation | `[Vendor]` [case study](https://www.supahuman.com/use-cases/carpet-court-transforming-warranty-claims-with-generative-ai) |
| All Health Medical | Healthcare | NZ | AI diagnostics for remote patient access | `[Vendor]` [supahuman.com](https://www.supahuman.com/case-studies) |
| House of Travel | Tourism | NZ | Corporate travel RFP response generation | `[Vendor]` [case study](https://www.supahuman.com/use-cases/revolutionising-corporate-travel-rfp-responses-with-ai) |

**Key observation**: SupaHuman's core IP is generic RAG orchestration on top of Microsoft
365, not geotechnical domain knowledge. The same architecture that drafts geotech reports
generates travel itineraries. This is a thin technical moat.

---

### Network Effects — Has Archie Shifted the NZ Geotech Conversation?

No. The only independent mention in a professional publication is a single line in the
AI Forum NZ Productivity Report (August 2025). No competing firm has publicly responded,
no debate is visible, no conference presentations located.

| Source | Author / org | Stance | Key observation | Date | URL |
|--------|-------------|--------|-----------------|------|-----|
| AI Forum NZ Productivity Report | AI Forum NZ | Neutral | Mentions Soil & Rock as a "practical impact" case study | Aug 2025 | [aiforum.org.nz](https://aiforum.org.nz/wp-content/uploads/2025/08/AI-Forum-Productivity-Report_Website_Aug-2025.pdf) |
| NZ geotech professional community | Not found | — | No LinkedIn threads, Reddit posts, or event presentations located | — | — |
| Competing firm principals | Not found | — | No public commentary from T+T, Beca, WSP NZ, or any other firm referencing Archie | — | — |

**Conclusion**: Archie remains a single-firm curiosity. One industry report mention, no
visible ripple effect across the NZ geotech profession.

---

### GBR Liability — What Does NZ Law Say About AI-Drafted High-Stakes Reports?

> **Scope boundary**: This section records published regulatory facts only. Professional
> interpretation of GBR liability exposure belongs to Graeme, not this document.

NZ's regulatory framework is technology-agnostic on drafting method but unambiguous on
liability: the signing CPEng is fully and personally responsible regardless of how the
document was generated. Insurers are beginning to bifurcate coverage.

| Regulatory / legal dimension | Current position | Source |
|------------------------------|-----------------|--------|
| CPEng liability when AI drafts the report | Full personal and professional liability remains with the human engineer; AI cannot make engineering judgments or ensure code compliance | `[Independent]` [Engineering NZ](https://www.engineeringnz.org/programmes/engineering-and-ai/ai-in-professional-practice/) |
| Producer Statement validity (PS1/PS4) with AI input | Valid, provided the signing engineer rigorously verifies all outputs; AI cannot sign off work under any circumstances | `[Independent]` [Engineering NZ](https://www.engineeringnz.org/programmes/engineering-and-ai/ai-in-professional-practice/) |
| GBR legal status vs. consent report in NZ | A GBR is a contractual risk-allocation instrument (owner vs. contractor), not a regulatory submission — governs financial compensation for unforeseen ground conditions | `[Independent]` [Scribd — GBR Fundamentals](https://www.scribd.com/document/332902406/GBR-Fundamentals-Past-Practices-and-Lessons-Learned-by-Randall-Essex-pdf) |
| Professional indemnity insurer guidance on AI drafting | Insurers warn AI distances staff from fundamental reasoning; affirmative AI policies and absolute AI exclusion clauses are both emerging in specialty lines | `[Independent]` [Marsh PI Market Update](https://www.marsh.com/en/services/financial-professional-liability/insights/professional-indemnity-market-update-part-two-four-key-risk-issues.html) |
| Engineering NZ on liability and producer statements | Strict liability for improperly signed producer statements; relying solely on AI for safety assessments or code compliance is explicitly prohibited | `[Independent]` [Engineering NZ](https://www.engineeringnz.org/news-insights/please-read-carefully/) |

**All five rows contain verified published positions.**

**Flag for Graeme**: The table above describes the legal framework. What it does not answer
is: given no structured quality layer between AI output and CPEng sign-off, what is the
realistic exposure profile when an AI-drafted GBR contains a hallucinated baseline parameter
in a tunneling contract? That is an engineering judgment call, not a regulatory lookup.

---

### Competitor Sentiment — Are NZ Geotech Firms Inspired or Moving?

The top-tier firms (T+T, Beca, WSP) are moving — building internal AI capabilities or
commercialising their own tools, not reacting to Archie specifically. Beca is the most
advanced: commercialising "Frankly.AI" via Microsoft Teams globally.

| Organisation | Person / role | Observable signal | Interpretation | Source |
|--------------|--------------|-------------------|----------------|--------|
| Tonkin + Taylor | Santosh Dixit / Digital Strategy | Digital transformation initiative with AWS; building a "digitally savvy organisation" | Internalising cloud and AI rather than buying bespoke agency builds | [peritossolutions.com](https://www.peritossolutions.com/about-us/) |
| Beca | Matt Ensor / CEO Frankly.AI | Commercialising in-house AI project "Frankly.AI" globally via Microsoft Teams | Has crossed from AI adopter to AI vendor; potential direct competitor to any SaaS entrant | [reseller.co.nz](https://www.reseller.co.nz/article/1300785/beca-takes-its-franklyai-teams-tool-global-via-microsoft.html) |
| WSP NZ | Rudi Roux / Head of Digital | AMDS Network Model — structured data harmonisation as AI foundation | Treating data standardisation as a prerequisite before deploying narrative generation | [wsp.com](https://www.wsp.com/en-gl/projects/nzta-amds-network-model) |
| Douglas Partners NZ | Yosafat Sinaga / Geotechnical Engineer | Conference case study: AI-driven automation of geotechnical analysis | Smaller firms experimenting with AI for predictive modelling, not report drafting | [geomechanics.org.au](https://geomechanics.org.au/meetings/ags-sydney-young-geomechanical-professionals-night/) |
| Golder NZ | — | No public signal located | — | — |
| Opus | — | No public signal located | — | — |
| Stantec NZ | — | No public signal located | — | — |

**Key observation**: The competitive risk is not that firms are reacting to Archie — they
are not. The risk is that Beca is already building and commercialising a general AI platform
for the AEC sector. A SaaS entrant needs a deeper geotechnical vertical than Beca's
horizontal tool to justify the differentiation.

---

## Strategic Summary

**What Archie actually does (verified)**
Integrates with Microsoft 365 to ingest raw field data and historical documents, then
generates section-by-section report drafts using custom prompts tuned to the firm's
templates, tone, and formatting standards.

**What it claims to do (unverified)**
Reduces end-to-end report preparation from 10 hours to 20 minutes, producing outputs
accurate enough to be immediately council-ready without significant human correction.

**Primary user**
Junior to mid-level engineering staff; senior engineers shift to reviewer and sign-off roles.

**Core value delivered**
Eliminates manual transcription and formatting work, increasing firm throughput without
expanding headcount.

**Biggest gap between claim and evidence**
The 24x speed claim ignores data structuring effort before ingestion and the legally
mandatory professional review after generation — both unquantified.

**Confidence in the 24x speed claim**
**Low** — the metric originates entirely from vendor marketing with no independent
time-motion analysis and no transparent accounting of what the 20 minutes actually includes.

---

| Strategic question | What the evidence shows |
|--------------------|------------------------|
| Does SupaHuman's pricing model validate a SaaS opportunity? | Yes. Base licence + per-user ongoing fees leave the mid-to-lower market completely unserved by a simpler, lower-cost alternative. |
| Is SupaHuman a specialist or a generalist? | Generalist. The same RAG architecture handles travel RFPs, warranty claims, and geotech reports. No geotechnical domain IP. |
| Has Archie created market-level urgency? | No. One industry report mention, zero peer commentary, zero competitive responses to Archie specifically. |
| Is the GBR liability gap a product requirement or a marketing angle? | Product requirement. Insurer exclusion clauses and CPEng strict liability together demand immutable audit trails and human review gates. |
| Are competitors moving, or is Soil & Rock still alone? | Top-tier firms are moving on internal AI. Beca is commercialising. The geotechnical-specific report drafting niche remains open. |
