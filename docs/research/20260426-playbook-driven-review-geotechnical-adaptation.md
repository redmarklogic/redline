# Playbook-Driven Review: Geotechnical Engineering Adaptation

**Author**: Graeme (Principal Geotechnical Engineer)
**Date**: 2026-04-26
**Confidence**: cross-referenced (4 notebooks queried, 6 queries total)
**Sources**: Legal AI Startup notebook, Geotechnical Report Workflows notebook, GBR notebook, Risk Assessment in Engineering notebook

## Context

This research explores whether Leya's (leya.law; note: original notebook source
transcribed name as "Legora" — corrected 2026-04-27) "playbook-driven review" concept
— a legal-AI product pattern where firm-specific rules drive automated document markup
— can be adapted for geotechnical engineering report review. The research was triggered
by the advisory board's analysis of Leya (legal AI, $675M valuation, YC W24)
documented in `docs/research/20260426-legal-ai-adjacent-market-signal.md`.

---

## 1. What is Leya's Playbook Concept?

### Definition

In Leya, a **playbook** is a collection of rules used to approve or disapprove specific language within a document [Legal AI, citation 1, 2]. It is created by an organisation's core legal team [Legal AI, citation 3].

### What a playbook contains

- **Rules**: Specific criteria that define what language is acceptable or unacceptable.
- **Example language**: The firm's approved standard wording — what the clause *should* say.
- **Fallbacks**: Alternative, pre-approved text to use if the primary language is rejected by the opposing party. Playbooks support multiple fallback tiers (e.g., fallback one, fallback two) [Legal AI, citation 3].
- **Starting positions**: The firm's overarching negotiation stance for a document type [Legal AI, citation 4].
- A single playbook can consist of 20 different procedural steps [Legal AI, citation 4].

### How the AI uses the playbook

1. **Creation**: The legal team builds the playbook, defining rules, example text, and fallback positions. This establishes a firm-wide standard [Legal AI, citation 3].
2. **Execution**: A user opens a document in Leya (integrated as a Microsoft Word add-in), selects the relevant playbook, and presses "play" [Legal AI, citation 3, 5, 6].
3. **Automated review**: The AI processes the document rule-by-rule, identifies non-conforming text, and marks up the file with the approved alternative language. This is called **redlining** — the process of comparing, tracking, and marking up document revisions [Legal AI, citation 3, 6].
4. **Final approval**: The human user remains entirely in control. They review the AI's suggested markups and decide what edits are ultimately approved and applied [Legal AI, citation 7].

### Strategic role of playbooks

Playbooks serve as a mechanism for **firm-specific knowledge capture**. The organisation's legal experts create the playbook by inputting their own specific rules, preferred wording, and acceptable fallback positions. This effectively captures the firm's specialised knowledge and turns it into a reusable standard for the whole company [Legal AI, citation 1, 2].

Playbooks also enable **horizontal scaling** across departments. At Leya itself, every sales rep uses Leya to negotiate NDAs (Non-Disclosure Agreements) before sending them to the legal team. At one large Nordic bank, adoption spread from legal to compliance to risk to sales [Legal AI, citation 2, 3].

### Competitive dynamics

The CEO explicitly notes that professional firms avoid being locked into long-term vendor contracts — firms prefer one- or two-year agreements, forcing the software provider to constantly prove its value [Legal AI, citation 6, 7]. Leya's moat strategy involves building domain-specific adaptations — engineering the AI to write complex clauses exactly as an expert professional would, rather than simply generating the most statistically probable text [Legal AI, citation 4, 5].

The sources do not describe playbooks as an explicit "lock-in mechanism." However, my inference is clear: once a firm has invested significant senior-engineer time encoding their standards into playbooks, the cost of recreating that configuration in a competitor's tool creates a natural switching cost.

---

## 2. Geotechnical Playbook Adoption — How It Maps

The cross-referencing with the Geotechnical Report Workflows notebook reveals that large geotechnical firms already operate a system remarkably similar to Leya's playbook concept — they just do it manually and call it something different.

### What a "geotechnical playbook" would contain

Based on the notebook evidence, a geotechnical playbook would contain four layers of rules:

**Layer 1 — Mechanical/formatting rules (already codified)**
- Font: Calibri 11pt body text [Report Workflows, citation 9, 17]
- Headings: Sentence case, capitalise first word only (except proper nouns) [Report Workflows, citation 9, 17]
- Document naming convention: `Project job number - Document Type - Discipline - Element - Unique Reference Number` (e.g., `1001234.1-RPT-GT-NRT-001`) [Report Workflows, citation 9, 16]
- Numbering flush left, no indentation [Report Workflows, citation 18]
- Reports over 20 pages: each section begins on a new page [Report Workflows, citation 9]
- No ampersand in place of "and" unless a company name [Report Workflows, citation 18]
- English spelling, not American [Report Workflows, citation 17]

**Layer 2 — Structural/quality rules (partially codified)**
- The "20 Checkpoints in 90 Seconds" self-review checklist: professional presentation, logical flow, tone, accuracy of measurements and figures [Report Workflows, citation 5, 6, 7]
- Section B Review Checklist: calculations checked using multiple methods, data tables accurate, technical review complete, all drawings signed and stamped [Report Workflows, citation 10, 11, 12]
- Stability Analysis Review Checklist: model geometry, material parameters, groundwater conditions, slip surface definitions, seismic accelerations [Report Workflows, citation 13]

**Layer 3 — Linguistic/liability rules (codified in guidance, often tacit in application)**
- **Taboo words to flag**: "all", "every", "always", "never", "complete", "ensure", "guarantee", "certify", "safe" — these elevate standard of care to strict liability [Risk Assessment, citation 5, 13-16]
- **Required conditional alternatives**: "generally", "typically", "substantially complete", "strive to", "review for general conformance", "in accordance with industry standards" [Risk Assessment, citation 13-15, 17, 18]
- **Banned subjective phrases**: "these results undoubtedly show", "fit for purpose", "due diligence" [Risk Assessment, citation 1, 21-23]
- **Mandatory disclaimer clauses**: Inferred conditions caveat, temporal boundaries, changed conditions notification, third-party reliance restriction, standard of care clause, liability cap clause [Risk Assessment, citations 25-36]

**Layer 4 — Technical validity rules (mostly tacit, being codified)**
- Methodology soundness, data quality, and technical defensibility [Report Workflows, citation 29, 32]
- The firm is actively developing "Pre-review prompts" (the "T+T Writing Coach Model") drafted by senior engineers to codify this layer [Report Workflows, citation 30, 31]

### Who would create the playbook?

The firm's existing review hierarchy maps directly to playbook authorship:

| Playbook layer | Author equivalent | Current role |
|---|---|---|
| Mechanical/formatting | BIS / PC (Business Integrated Services / Project Controllers) | Administrative support staff [Report Workflows, citation 9, 8] |
| Structural/quality | Technical Reviewer (TR) | Independent specialist with knowledge equal to or above the author [Report Workflows, citation 4, 5, 8] |
| Linguistic/liability | Project Director (PD) + Insurance and Contracts Team | PD acts as client proxy; ICT owns legal caveats [Report Workflows, citation 3, 8; Risk Assessment, citation 12] |
| Technical validity | Subject Matter Expert (SME) / Centre of Technical Excellence (CoTE) | Industry-recognised technical experts [Report Workflows, citation 6, 7, 8] |

### What the AI would do with it

The AI would check a draft GIR (Geotechnical Interpretive Report) or GBR against the playbook and flag deviations — exactly as Leya does with contracts. Specifically:

1. **Scan for taboo words** that elevate standard of care (mechanical, fully automatable)
2. **Verify mandatory sections exist** — limitations clause, third-party reliance, standard of care, changed conditions notification (structural, fully automatable)
3. **Check formatting compliance** — font, headings, naming convention, numbering (mechanical, fully automatable)
4. **Flag ambiguous baseline language** in GBRs — "may", "could", "up to", "ranges from...to..." without definitive values (linguistic, automatable with pattern matching)
5. **Cross-reference against specifications** — flag GBR text that duplicates or contradicts technical specifications (structural, requires document-pair analysis)
6. **Interrogate technical defensibility** — are conclusions supported by the data presented? (analytical, requires LLM judgment)

### What firm-specific knowledge could be encoded?

- The firm's preferred wording for limitation clauses (every firm has slightly different standard text)
- The firm's approved fallback positions for contractual caveats
- Firm-specific style rules beyond industry standards
- Project Director preferences for how conclusions should reference data
- The firm's risk appetite — how conservative or aggressive their standard baseline language should be
- Client-specific requirements (e.g., certain clients require specific clause structures)

### Prior-art convergence — the founder's Faultless concept

The Geotechnical Report Workflows notebook describes a document review concept called
**"Faultless"** that splits review into exactly these two layers [Report Workflows,
citation 26]:

- A **"Rule Matrix"** for high-speed automated "pre-flight" checks covering syntax,
  formatting, and compliance [Report Workflows, citation 25, 27, 28]
- **"Pre-review prompts"** drafted by senior engineers to interrogate methodology
  soundness, data quality, and technical defensibility [Report Workflows, citation 30,
  31, 32]

**"Faultless" was the founder's own prior working name for what is now Redline.** This
is not independent external validation of the concept — it is founder-conviction
evidence. The playbook architecture was conceived and partially built before
encountering Leya's framing. The Geotechnical Report Workflows notebook sources this
concept from the founder's prior work.

---

## 3. GBR-Specific Playbook Rules

Based on the GBR notebook, the following specific rules could be directly encoded into a GBR playbook:

### Taboo wording rules (flag and replace)

| Rule | Flag pattern | Replacement guidance |
|---|---|---|
| GBR-LANG-01 | Words: "may", "can", "might", "up to", "could", "should", "would", "some", "few", "ranges from...to..." | Replace with definitive terms: "is", "will", "are" [GBR, citation 8] |
| GBR-LANG-02 | Unquantified adjectives: "large", "significant", "local", "many", "intermittent", "continuous", "minor" | Flag unless strictly quantified or defined in a GBR glossary [GBR, citation 9] |
| GBR-LANG-03 | The word "shall" in baseline statements | Flag — GBR is not a specification; "shall" implies contractual obligation [GBR, citation 9] |
| GBR-LANG-04 | Dangerous conjunctions: multiple conditions joined by "and" in a single baseline statement | Flag — split into separate simple bullet points to prevent partial-DSC claims [GBR, citation 10] |
| GBR-LANG-05 | Shorthand geological names (e.g., "London Clay") | Flag — replace with formal strata names (e.g., "London Clay Formation") to avoid material assumptions [GBR, citation 11] |

### Baseline quality rules (structural checks)

| Rule | Check | Rationale |
|---|---|---|
| GBR-BASE-01 | Flag any baseline that presents a data range without a definitive average or percentage distribution | "Soft baselines" with only min-max ranges are ambiguous and favour DSC claims [GBR, citation 12, 13, 14] |
| GBR-BASE-02 | Flag any baseline statement that does not specify how and where the parameter will be measured during construction | Unmeasurable baselines cannot prove or disprove a DSC claim [GBR, citation 15, 16] |
| GBR-BASE-03 | Flag requirements for tests impossible to perform during the specified construction method | E.g., requiring triaxial lab testing on soil excavated by a TBM (Tunnel Boring Machine) [GBR, citation 17, 18] |
| GBR-BASE-04 | Flag exact continuous lines drawn for strata boundaries on geological profiles | Exact lines imply perfect prediction — boundaries should be tabulated as ranges [GBR, citation 19] |

### Structural deficiency rules

| Rule | Check | Rationale |
|---|---|---|
| GBR-STRUCT-01 | Flag GBRs exceeding 30-50 pages | Excessive length dilutes baselines and creates confusion [GBR, citation 21, 22] |
| GBR-STRUCT-02 | Flag text that repeats or paraphrases technical specifications | "Say it once, and say it well" — contradictions between GBR and specs trigger disputes [GBR, citation 24, 25] |
| GBR-STRUCT-03 | Flag any section labelled "for information only" or "non-binding" | Parsing into binding vs non-binding creates contradictory standards within a single document [GBR, citation 26, 27, 28] |
| GBR-STRUCT-04 | Flag silence on man-made obstructions | GBR must state either a specific number of obstructions or that none are anticipated [GBR, citation 23, 29] |
| GBR-STRUCT-05 | Flag sections that list physical properties without describing anticipated ground behaviour | GBR must describe behaviour in response to the contractor's expected construction methods [GBR, citation 30, 31] |

---

## 4. Risk Mitigation Playbook Rules

Based on the Risk Assessment in Engineering notebook, the following rules would protect the firm from professional liability exposure:

### Linguistic liability rules

| Rule | Check | Rationale |
|---|---|---|
| RISK-LANG-01 | Flag absolute words: "all", "every", "always", "never", "complete", "ensure", "guarantee", "certify", "safe" | These elevate standard of care from negligence to strict liability, which is typically excluded from professional indemnity insurance [Risk Assessment, citation 1, 5, 13-16] |
| RISK-LANG-02 | Flag subjective phrases: "these results undoubtedly show", "fit for purpose", "due diligence" | Broadens scope or implies unrealistic precision [Risk Assessment, citation 1, 21-23] |
| RISK-LANG-03 | Flag excessive unrequested factual data | Opposing lawyers can exploit minor discrepancies between texts and logs [Risk Assessment, citation 7, 19, 20] |

### Mandatory clause presence rules

| Rule | Check required | Example clause wording |
|---|---|---|
| RISK-CLAUSE-01 | Inferred conditions caveat present | "Subsurface conditions between boreholes are inferred and may vary significantly from conditions encountered at the borings" [Risk Assessment, citation 25, 26] |
| RISK-CLAUSE-02 | Temporal boundaries caveat present | "The soils and rock conditions described in this report are those observed at the time of the study" [Risk Assessment, citation 26] |
| RISK-CLAUSE-03 | Groundwater temporal caveat present | "Groundwater conditions described in this report refer only to those observed at the place and time of observation noted in the report" [Risk Assessment, citation 26] |
| RISK-CLAUSE-04 | Changed conditions notification clause present | Must require the firm to be notified if site conditions differ from report, and to be given opportunity to review recommendations [Risk Assessment, citation 27] |
| RISK-CLAUSE-05 | Third-party reliance restriction present | "This report has been prepared for the exclusive use of our client [name]...may not be relied upon...by any person other than our client, without our prior written agreement" [Risk Assessment, citation 34] |
| RISK-CLAUSE-06 | Standard of care clause present | "Services performed by [name of firm] for this report are conducted in a manner consistent with that level of skill and care ordinarily exercised by members of the profession currently practicing under similar conditions" [Risk Assessment, citation 4] |
| RISK-CLAUSE-07 | Third-party data reliance disclaimer present (if applicable) | "We have relied upon, and presumed accurate, the information in the report produced by [other consultant]...We have not attempted to verify the accuracy or completeness of the Existing Information" [Risk Assessment, citation 28, 29] |
| RISK-CLAUSE-08 | Liability cap referenced in contract/proposal | Cap amount commensurate with scale and nature of services [Risk Assessment, citation 12, 31] |

---

## 5. Evidence Gaps

The following questions remain unanswered by the notebooks:

1. **How do other geotechnical firms structure their review checklists?** The Report Workflows notebook is based on a single firm's (T+T's) processes. I do not have comparative data from other large consultancies (AECOM, WSP, Jacobs, Mott MacDonald) to know if their approaches differ materially.

2. **What is the actual error rate in GBRs?** The GBR notebook describes *types* of errors but does not quantify how frequently they occur. Knowing the base rate would help prioritise which playbook rules deliver the most value.

3. **How do playbooks handle jurisdiction-specific requirements?** Geotechnical practice varies by jurisdiction (NZ, Australia, UK, US). The notebooks do not address how a playbook system would handle multi-jurisdictional rule sets — a firm operating in both NZ and Australia would need different liability clause wording.

4. **What is the cost of playbook creation?** Neither the legal nor engineering notebooks quantify how much senior-expert time is required to build and maintain a playbook. This is critical for the business case.

5. **How does the playbook concept handle novel or unusual projects?** The GBR notebook notes that every project is unique. Standard playbook rules may not cover unusual ground conditions, novel construction methods, or first-of-kind infrastructure. The boundary between "checkable by playbook" and "requires expert judgment" needs definition.

6. **Leya's switching cost mechanism is not explicitly stated in the notebook sources.** The switching cost argument is an inference, not a stated fact from the CEO.

---

## 6. Graeme's Assessment

### Is the playbook concept viable for geotechnical engineering?

**Yes — emphatically.** In fact, the evidence suggests that geotechnical engineering may be an *even better* fit for playbook-driven review than legal contract review. Here is my reasoning:

**The review process is already structured for it.** Large geotechnical firms already operate a multi-tier review system with codified checklists (20 Checkpoints in 90 Seconds, Section B Review Checklist, Stability Analysis Review Checklist) and explicit role separation (Author, TR, PD, BIS). The playbook concept does not require inventing a new workflow — it automates an existing one.

**The liability rules are more deterministic than legal rules.** In law, whether a clause is "acceptable" often depends on negotiation context, jurisdiction, and the opposing party's position. In geotechnical engineering, many of the rules are binary: either the limitations clause is present or it is not. Either the word "ensure" appears (bad) or it does not. Either the baseline has a definitive value or it has a range without one. This determinism makes automated checking more reliable.

**The consequences of failure are severe and measurable.** A GBR with ambiguous baseline language can trigger a DSC claim worth millions. A report missing a third-party reliance restriction can expose the firm to unlimited liability. The playbook directly reduces the probability of these high-cost events.

**The concept was already being built — by the founder.** "Faultless" (the former
working name for Redline) already incorporated a Rule Matrix for automated pre-flight
checks and a Writing Coach Model for technical defensibility. This is founder-conviction
evidence, not independent external validation. The Leya framing clarifies the
vocabulary; the geotechnical engineering implementation was already in progress.

### What are the adoption barriers?

1. **Tacit knowledge codification is hard.** The mechanical rules (formatting, taboo words, clause presence) are straightforward to encode. The analytical rules (Is the methodology sound? Does the conclusion follow from the data?) are much harder. The firm's Report Workflows notebook explicitly identifies this as a "Functional Gap" [Report Workflows, citation 29].

2. **Engineer resistance to automated review.** Senior engineers may resist the implication that their judgment can be reduced to rules. The playbook must be positioned as a "pre-flight check" that catches mechanical errors before the human reviewer sees the document — not as a replacement for professional judgment.

3. **Playbook maintenance burden.** Standards change, firm preferences evolve, new project types emerge. Someone must maintain the playbook. In law, this is the legal team's job. In engineering, it would fall to the Quality Manager or a senior Technical Reviewer — roles that are already stretched.

4. **Multi-jurisdictional complexity.** A firm operating in NZ, Australia, and the UK would need jurisdiction-specific rule sets for liability clauses, standards references, and even spelling conventions (English vs American). The playbook system must support rule inheritance and overrides.

### What makes geotechnical engineering different from law?

The critical difference is the **nature of the document being reviewed**.

In law, a contract is a **negotiated** document. The playbook checks whether the firm's preferred language is present, but the final wording is a compromise between two parties. The AI suggests; the lawyer negotiates.

In geotechnical engineering, a report is a **unilateral** document. The firm writes it, the firm signs it, the firm bears the liability. There is no "opposing party" whose language must be accommodated. This means:

- **No fallback positions needed.** Unlike Leya, where the playbook contains fallback
  language for when the opposing party rejects the preferred wording, a geotechnical
  playbook has a single approved wording for each clause. The firm is not negotiating
  — it is writing.
- **The stakes are different.** A lawyer who misses a clause in a contract may cost the client money. A geotechnical engineer who misses a limitations clause may expose the firm to personal professional liability and PI (Professional Indemnity) insurance claims.
- **The document is more structured.** Geotechnical reports follow a predictable section structure (introduction, scope, site description, ground model, design parameters, conclusions, limitations). Contracts are more variable. This structural predictability makes automated checking easier.

The bottom line: the playbook concept is not just viable — it is arguably more natural for geotechnical engineering than for law. The challenge is not "can it work?" but "how far up the analytical ladder can the playbook reach?"

---

## Notebooks Queried

| Notebook | ID | Queries |
|---|---|---|
| Legal AI Startup | `0d7a9a9d-0f9d-4cba-9191-f6e29a7e158a` | 2 |
| Geotechnical Report Workflows | `ee83806c-ff73-436d-ad0b-ca319818e553` | 2 |
| Geotechnical Baseline Reports (GBR) | `8eab0bf9-090d-4b1e-975f-00dbd96342af` | 1 |
| Risk Assessment in Engineering | `0b726429-82bc-43f7-9225-ba06f71046c3` | 1 |
