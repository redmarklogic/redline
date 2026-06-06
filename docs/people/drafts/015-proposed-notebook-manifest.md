# 015 — Proposed Notebook Manifest

**Spec**: [015-notebooklm-account-migration](../../specs/015-notebooklm-account-migration/spec.md)
**Produced by**: Linda
**Date**: 2026-06-06
**Status**: Awaiting Founder review

---

## Consultation Summary

All agents consulted: Graeme, Peter, Mark, Matt, Ron, John, Linda (self).
Three items require Founder resolution before Phase 2 begins — see [Open Items](#open-items-for-founder-resolution).

---

## Proposed Notebooks

### Geotechnical Domain (Graeme — primary owner)

| Field | Value |
|---|---|
| **ID** | `engineering-standards` |
| **Name** | Engineering Standards |
| **Description** | NZ infrastructure design standards (IDS), earthworks and compaction requirements (NZS 4431), geotechnical QA procedures, and subdivision consent documentation for practitioners working in the Canterbury / NZ regulatory context. |
| **Topic area** | Engineering theory & standards |
| **Access** | open |
| **Primary owner** | Graeme |
| **Projected source count** | 74 (no split required at this time) |
| **Notes** | Graeme confirmed Option C: keep at 74, enforce NZ-only inclusion policy going forward. In-scope bodies: SNZ, AS-NZS joint, Local Authorities, NZ Industry Institutes (NZGS, Engineering NZ). Out-of-scope: ASTM, ISO, BSI-CEN, DIN. If count reaches 90, revisit Option A split (NZ-domestic vs international-reference). |

---

| Field | Value |
|---|---|
| **ID** | `ground-engineering-magazine` |
| **Name** | Ground Engineering Magazine |
| **Description** | Issues of Ground Engineering magazine (2014-2026) covering geotechnical industry news, technical papers, and key standards development across piling, foundations, tunnelling, earthworks, and slope stability. |
| **Topic area** | Engineering theory & standards |
| **Access** | open |
| **Primary owner** | Graeme |
| **Projected source count** | Unknown — **BLOCKED** |
| **Notes** | WARN️ **Founder action required.** Notebook was not populated in old account (0 sources in index). Graeme confirmed: skip creation until source files are confirmed present in the library. If files exist and count < 100, create as-is. If ≥ 100, split by date range: `ground-engineering-magazine-2014-2019` and `ground-engineering-magazine-2020-2026`. Graeme approved the date-range split boundary as thematically meaningful (post-Eurocode 7 revision cycle). See [Open Items](#open-items-for-founder-resolution). |

---

| Field | Value |
|---|---|
| **ID** | `geotechnical-baseline-reports` |
| **Name** | Geotechnical Baseline Reports (GBR) |
| **Description** | Industry guidance on preparing and contractually applying GBRs to allocate subsurface construction risk. Covers Differing Site Conditions claims, ASCE guidelines, CIRIA C807, the NZTS guide, and the FIDIC Emerald Book. |
| **Topic area** | Geotechnical domain |
| **Access** | open |
| **Primary owner** | Graeme |
| **Projected source count** | 4 |
| **Notes** | Keep as-is. Graeme flagged for growth: FIDIC guidance, ICC guidance, project-specific GBR examples. |

---

| Field | Value |
|---|---|
| **ID** | `geotechnical-report-workflows` |
| **Name** | Geotechnical Engineering Report Workflows and Standard Procedures |
| **Description** | Professional practice guides, templates, QA checklists, and training materials for geotechnical report structuring, factual/interpretive delineation, and client-centric writing. |
| **Topic area** | Geotechnical domain |
| **Access** | open |
| **Primary owner** | Graeme |
| **Projected source count** | 20 |
| **Notes** | Keep as-is. |

---

| Field | Value |
|---|---|
| **ID** | `risk-assessment-engineering` |
| **Name** | Risk Assessment in Engineering |
| **Description** | Risk management, professional liability, and probabilistic risk assessment in geotechnical engineering. Sources span ASCE, CIRIA, and NZGS guidelines, field manuals, and legal notes covering contracts, NDAs, and professional indemnity insurance. |
| **Topic area** | Geotechnical domain |
| **Access** | open |
| **Primary owner** | Graeme |
| **Projected source count** | 10 |
| **Notes** | Keep as-is. Graeme flagged: scope-check sources before migration to ensure geotechnical-specificity (slope reliability, foundation failure probability, liquefaction risk frameworks). Cull any that have drifted to general engineering risk. |

---

| Field | Value |
|---|---|
| **ID** | `geotechnical-checklists` |
| **Name** | Geotechnical Engineering Checklists |
| **Description** | Geotechnical engineering QC checklists, review guidelines, and submittal checklists from US and NZ sources. Covers FHWA report review, NZ design QC workflow, NZGS ground investigation specifications, and building consent lodgement requirements. |
| **Topic area** | Geotechnical domain |
| **Access** | open |
| **Primary owner** | Graeme |
| **Projected source count** | 10 |
| **Notes** | Keep separate from `geotechnical-report-workflows`. Operational artefacts vs process guidance — different query use case. |

---

### AI & Software Architecture (Peter — primary owner)

| Field | Value |
|---|---|
| **ID** | `ai-system-engineering` |
| **Name** | AI System Engineering |
| **Description** | Generative AI application design and deployment: foundation models, prompt engineering, RAG, multiagent orchestration, FastAPI/Docker serving, MCP, OAuth2, NIST AI Risk Management Framework, EU AI Act, GDPR. |
| **Topic area** | AI & software architecture |
| **Access** | open |
| **Primary owner** | Peter |
| **Projected source count** | 5 (old account) → target 20+ in new account |
| **Notes** | Peter flagged as under-sourced. Phase 2 action: Peter to supply source titles for expansion. Structural role: foundational/architectural AI engineering (not tactics). Do not merge with `llm-token-optimisation-agentic-workflows`. |

---

| Field | Value |
|---|---|
| **ID** | `software-architecture-ddd` |
| **Name** | Software Architecture & Domain-Driven Design |
| **Description** | Canonical books covering DDD strategic/tactical patterns (Bounded Contexts, Ubiquitous Language, Aggregates), architecture styles (Hexagonal, CQRS, Microservices, Event-Driven), SOLID principles, GoF design patterns, EventStorming, Context Mapping, Event Sourcing, and Data Mesh. |
| **Topic area** | AI & software architecture |
| **Access** | open |
| **Primary owner** | Peter |
| **Projected source count** | 13 |
| **Notes** | Keep as-is. |

---

| Field | Value |
|---|---|
| **ID** | `software-dev-methodology-eng-org` |
| **Name** | Software Development Methodology & Engineering Organisation |
| **Description** | 25-source knowledge base spanning software engineering methodology, product discovery, AI/LLM engineering, and engineering leadership. Covers Farley, Mythical Man-Month, Accelerate, Continuous Delivery, INSPIRED/Empowered, LLM Engineering, Age of Invisible Machines, Staff Engineer, Team Topologies, and Working Backwards. |
| **Topic area** | AI & software architecture |
| **Access** | open |
| **Primary owner** | Peter |
| **Projected source count** | 25 |
| **Notes** | Keep as one notebook. Peter confirmed all four sub-areas serve the same consumer and cross-cutting material would fragment poorly. |

---

| Field | Value |
|---|---|
| **ID** | `llm-token-optimisation-agentic-workflows` |
| **Name** | LLM Token Optimisation — Agentic VS Code Copilot Workflows |
| **Description** | Evidence-based strategies for reducing LLM input token consumption in agentic multi-agent VS Code workflows. Covers modular instruction architectures, session length management, model routing, prompt caching, and token cost monitoring. |
| **Topic area** | AI & software architecture |
| **Access** | open |
| **Primary owner** | Peter |
| **Projected source count** | 26 (not in old index — count from register description) |
| **Notes** | Keep separate from `claude-max-20x-developer-workflow-research`. Boundary: token optimisation strategies and techniques ("how") vs. Claude Max rate-limit behaviour and subscription constraints ("what limits apply"). Sources spanning both go here. |

---

| Field | Value |
|---|---|
| **ID** | `claude-max-20x-developer-workflow-research` |
| **Name** | Claude Max 20x — Developer Workflow Adaptation Research |
| **Description** | Evidence-based research on Claude Max 20x subscription usage limits, rate-limit behaviour, and workflow adaptations. Covers first-party vs third-party billing, prompt caching mechanics, sub-agent token consumption, Haiku-as-Scout routing, LiteLLM gateway governance, and the May 2026 compute deal. |
| **Topic area** | AI & software architecture |
| **Access** | open |
| **Primary owner** | Peter |
| **Projected source count** | 8 |
| **Notes** | Keep separate. See boundary note above. |

---

### Process & Product / Strategy (Mark — primary owner)

| Field | Value |
|---|---|
| **ID** | `business-process-management` |
| **Name** | Business Process Management |
| **Description** | BPM methodologies and continuous process improvement tools including Lean, Six Sigma, BPMN, 7FE, PDCA, and DMAIC frameworks. Drawn from expert-authored management books and the BPM CBOK. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Mark |
| **Projected source count** | 3 |
| **Notes** | Keep as-is. |

---

| Field | Value |
|---|---|
| **ID** | `product-roadmapping` |
| **Name** | Product Roadmapping |
| **Description** | Strategic product roadmapping for product leaders: defining vision, prioritising customer opportunities, and achieving stakeholder buy-in. Covers Kano model, MoSCoW prioritisation, ROI scorecards, user journey maps, and opportunity-solution trees. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Mark |
| **Projected source count** | 1 (old account) → target 4-5 in new account |
| **Notes** | Mark confirmed 1 source is a gap. Phase 2 action: Mark to supply 3-4 additional titles (candidates: Torres *Continuous Discovery Habits*, Cagan *Inspired*, OST reference, executive-roadmap-communication). |

---

| Field | Value |
|---|---|
| **ID** | `writing-specs` |
| **Name** | Writing Painless Product and Functional Specifications |
| **Description** | Software product management frameworks and specification writing: PRDs, functional specifications, OKRs, the Shape Up framework, product discovery vs delivery, and alternatives to traditional roadmaps. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Mark |
| **Secondary consumers** | Peter |
| **Projected source count** | 10 |
| **Notes** | Keep as-is. Peter flagged a scoping concern: he needs upstream shaping artefacts (pitch structure, appetite framing, boundary conditions) covered, not just specification document format. Mark confirmed current scope is correct for Peter. If Peter's need is unmet in practice, a separate `shaped-pitches` notebook owned by Peter is the resolution path — not a scope change here. Confirm with Peter in Phase 2. |

---

| Field | Value |
|---|---|
| **ID** | `org-design-team-topologies` |
| **Name** | Organisational Design & Team Topologies |
| **Description** | Books on modern organisational leadership and team design. Team Topologies (stream-aligned, platform, enabling teams), Conway's Law, cognitive load management, and DDD for software teams. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Mark |
| **Secondary consumers** | Peter |
| **Projected source count** | TBD pending Founder decision on split |
| **Notes** | WARN️ **Founder decision required.** Mark proposes splitting into two notebooks: (1) `org-design-team-topologies` retaining Team Topologies, Conway's Law, cognitive load, DDD for software teams; (2) `workforce-capability-development` (new) covering deliberate practice, skills-based organisations, AI/RPA task deconstruction. Peter has not yet been consulted on the split — Mark said confirm with Peter first. Linda cannot create two notebooks until both owners confirm. See [Open Items](#open-items-for-founder-resolution). |

---

| Field | Value |
|---|---|
| **ID** | `professional-services-firm-management` |
| **Name** | Professional Services Firm Management |
| **Description** | Guide to the business, management, and future of professional service firms — engineering, law, and consulting. Career development, firm creation, operations, financial management, A/E/C firm strategy, and technological disruption. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Mark |
| **Projected source count** | 7 |
| **Notes** | WARN️ **Ownership conflict — Founder resolution required.** Mark proposed co-ownership with Graeme (Mark: PM/business side; Graeme: A/E/C-specific content). Graeme declined co-ownership: "I don't need co-ownership — it's professional services operations, not geotechnical domain knowledge." Resolution: Mark retains sole ownership. Linda records this as resolved in Graeme's favour (declination), but flags for Founder confirmation. See [Open Items](#open-items-for-founder-resolution). |

---

| Field | Value |
|---|---|
| **ID** | `govcon-systems-engineering` |
| **Name** | Government Contracting, Proposal Management & Systems Engineering |
| **Description** | Guide to winning government contracts. Requirements engineering, MBSE using UML and SysML, proposal strategy and management, RFP compliance, AI-assisted proposal automation including RAG. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Mark |
| **Projected source count** | 6 |
| **Notes** | Mark flagged as low-priority maintenance. No active GovCon initiative. Recreate as-is; do not add sources unless an active initiative is confirmed. |

---

| Field | Value |
|---|---|
| **ID** | `legal-ai-startup` |
| **Name** | Legal AI Startup |
| **Description** | Leya (leya.law) YC interview and website content. Legal AI product strategy, playbook-driven contract review, Word-native integration, senior-sponsor GTM in professional services, audit trails, and the collapse of point solutions under generative AI. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Mark |
| **Secondary consumers** | Ron (GTM/market-signal framing) |
| **Projected source count** | 2 (old account) → target 6-8 in new account |
| **Notes** | Keep as own notebook; expand. Mark wants: Leya competitor set (Harvey, Ironclad, Spellbook), analyst piece on legal tech adoption curves, a16z/YC writing on vertical AI GTM playbooks. Target 6-8 sources. Ron confirmed Mark's ownership is appropriate. Phase 2 action: Linda to locate/source additional legal AI material. |

---

| Field | Value |
|---|---|
| **ID** | `strategy-competitive-advantage` |
| **Name** | Strategy & Competitive Advantage |
| **Description** | Strategic thinking, competitive positioning, and sustained advantage. Business strategy frameworks (Good Strategy Bad Strategy, Blue Ocean), competitive analysis, resource-based view, strategic inflection points, and building defensible competitive moats. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Mark |
| **Projected source count** | Not in old account index (added recently) |
| **Notes** | Keep as-is. Recently added; let it stabilise before curating further. |

---

### Founder Strategy (Ron — primary owner, advisory-board-only)

| Field | Value |
|---|---|
| **ID** | `founder-memos` |
| **Name** | Redline Founder Memos |
| **Description** | Transcribed voice memos recorded by the Redline founder (April 2026) covering product vision, feature design, GTM strategy, pricing tiers, competitive analysis, UX decisions, and personal reflections on building a niche AI tool for small geotechnical consultancies. |
| **Topic area** | Founder strategy |
| **Access** | advisory-board-only |
| **Primary owner** | Ron |
| **Projected source count** | 9 |
| **Notes** | Keep as-is. |

---

| Field | Value |
|---|---|
| **ID** | `monetizing-scaling-innovation` |
| **Name** | Monetizing & Scaling Innovation |
| **Description** | Monetizing Innovation and Scaling Innovation by Madhavan Ramanujam et al. Willingness-to-pay discovery, pricing models, packaging and bundling, behavioural pricing tactics, the four monetisation failure patterns, and scaling strategies covering churn prevention, wallet-share growth, and price negotiation discipline. |
| **Topic area** | Founder strategy |
| **Access** | advisory-board-only |
| **Primary owner** | Ron |
| **Projected source count** | 2 |
| **Notes** | Keep as-is. |

---

| Field | Value |
|---|---|
| **ID** | `entrepreneurship-startup-strategy` |
| **Name** | Entrepreneurship & Startup Strategy |
| **Description** | Entrepreneurial management, strategic growth, and corporate innovation. Disruptive innovation, Lean Startup (MVP, Build-Measure-Learn), customer development, JTBD, product-market fit, Crossing the Chasm, B2B sales tactics, Business Model Canvas. |
| **Topic area** | Founder strategy |
| **Access** | advisory-board-only |
| **Primary owner** | Ron |
| **Projected source count** | 20 |
| **Notes** | Keep as-is. |

---

### UX & Design (Matt — primary owner)

| Field | Value |
|---|---|
| **ID** | `product-design-ux` |
| **Name** | Product Design & UX |
| **Description** | Four canonical texts on human-centred design and usability: The Design of Everyday Things (Norman), Don't Make Me Think Revisited (Krug), Designing with Data, and Forms that Work. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Matt |
| **Projected source count** | 7 |
| **Notes** | Keep as-is. |

---

### Marketing (John — primary owner)

| Field | Value |
|---|---|
| **ID** | `digital-marketing-social-selling` |
| **Name** | Digital Marketing & Social Selling |
| **Description** | Modern digital marketing, online sales, and personal branding. Content marketing (They Ask, You Answer / The Big 5), SEO and Product-Led SEO, LinkedIn social selling, ICP targeting, and Generative AI tools for marketing. |
| **Topic area** | Founder strategy |
| **Access** | advisory-board-only |
| **Primary owner** | John |
| **Projected source count** | 9 |
| **Notes** | Keep as-is. John flagged potential future addition: category creation source (e.g., Play Bigger) if Redline moves toward category design. Not for this migration cycle. |

---

### Knowledge Infrastructure (Linda — primary owner)

| Field | Value |
|---|---|
| **ID** | `information-architecture-km` |
| **Name** | Information Architecture and Knowledge Management |
| **Description** | Strategic design and management of information systems to make organisational knowledge assets findable, understandable, and actionable. Covers foundational Information Architecture, Knowledge Architectures, and Knowledge Management. |
| **Topic area** | Process & product |
| **Access** | open |
| **Primary owner** | Linda |
| **Projected source count** | 3 |
| **Notes** | Keep as-is. Linda self-flagged as under-sourced. Candidates for next intake: Morville & Rosenfeld (*Information Architecture for the Web and Beyond*), Davenport (*Working Knowledge*). Not a Phase 4 action — this is a future curation item. |

---

| Field | Value |
|---|---|
| **ID** | `technical-communication` |
| **Name** | Engineers' Guide to Technical Communication |
| **Description** | Technical writing and editing best practices for engineering and scientific audiences: document design, audience analysis, ethics, citation standards (Chicago Manual of Style), and structure for reports, proposals, laboratory studies, specifications, and business correspondence. |
| **Topic area** | Communication & documentation |
| **Access** | open |
| **Primary owner** | Linda |
| **Projected source count** | 8 |
| **Notes** | Keep as-is. |

---

## Notebook-to-Agent Access Table

| Notebook ID | Access | Primary Owner | Secondary Consumers |
|---|---|---|---|
| engineering-standards | open | Graeme | — |
| ground-engineering-magazine | open | Graeme | — |
| geotechnical-baseline-reports | open | Graeme | — |
| geotechnical-report-workflows | open | Graeme | — |
| risk-assessment-engineering | open | Graeme | — |
| geotechnical-checklists | open | Graeme | — |
| ai-system-engineering | open | Peter | Kabilan |
| software-architecture-ddd | open | Peter | Kabilan |
| software-dev-methodology-eng-org | open | Peter | Kabilan |
| llm-token-optimisation-agentic-workflows | open | Peter | Kabilan |
| claude-max-20x-developer-workflow-research | open | Peter | Kabilan |
| business-process-management | open | Mark | — |
| product-roadmapping | open | Mark | — |
| writing-specs | open | Mark | Peter |
| org-design-team-topologies | open | Mark | Peter |
| professional-services-firm-management | open | Mark | — |
| govcon-systems-engineering | open | Mark | — |
| legal-ai-startup | open | Mark | Ron |
| strategy-competitive-advantage | open | Mark | Ron |
| founder-memos | advisory-board-only | Ron | — |
| monetizing-scaling-innovation | advisory-board-only | Ron | — |
| entrepreneurship-startup-strategy | advisory-board-only | Ron | — |
| product-design-ux | open | Matt | — |
| digital-marketing-social-selling | advisory-board-only | John | — |
| information-architecture-km | open | Linda | — |
| technical-communication | open | Linda | — |

---

## Source Count Risk Summary

| Notebook | Old source count | Status |
|---|---|---|
| engineering-standards | 74 | Within limit. NZ-only inclusion policy enforced going forward. |
| software-dev-methodology-eng-org | 25 | OK |
| llm-token-optimisation-agentic-workflows | ~26 (from description) | OK |
| geotechnical-report-workflows | 20 | OK |
| entrepreneurship-startup-strategy | 20 | OK |
| **ground-engineering-magazine** | **0** | **WARN️ BLOCKED — file existence unconfirmed** |
| All others | ≤13 | OK |

---

## Open Items for Founder Resolution

### OI-1: ground-engineering-magazine — File Existence (BLOCKING for notebook creation)

**Issue**: The notebook had 0 sources in the old account. Graeme confirmed: do not recreate the notebook unless source files are confirmed present in `G:\My Drive\Library`.

**Founder action**: Confirm whether Ground Engineering magazine PDFs (issues 2014-2026) are in the library. If yes: confirm file count and whether a date-range split (2014-2019 / 2020-2026) is needed. If no: notebook is not recreated in this migration.

---

### OI-2: org-design-team-topologies — Split Decision (BLOCKING for notebook creation)

**Issue**: Mark proposes splitting into:
- `org-design-team-topologies` (retain): Team Topologies, Conway's Law, cognitive load, DDD for software teams
- `workforce-capability-development` (new): deliberate practice, skills-based organisations, AI/RPA task deconstruction

Mark said to confirm with Peter before splitting. Peter was not directly consulted on this split (he flagged interest in the first cluster, not the second).

**Founder action**: Confirm split or keep as single notebook. If split approved, `workforce-capability-development` is a new register entry with Mark as primary owner.

---

### OI-3: professional-services-firm-management — Ownership Conflict (Non-blocking; Linda's recommendation included)

**Issue**: Mark proposed co-ownership with Graeme. Graeme declined ("it's professional services operations, not geotechnical domain knowledge"). 

**Linda's recommendation**: Mark retains sole ownership. Graeme's declination is clear.

**Founder action**: Confirm Linda's recommendation or override.

---

## Phase 1 Exit Checklist

- [x] Linda has consulted every agent in the schedule
- [x] Each agent has confirmed their notebook structure (subject to OI-2 resolution)
- [x] All source-limit risks assessed — no split required except ground-engineering-magazine (if files exist, split by date range)
- [x] Shared-notebook ownership flagged (OI-2, OI-3)
- [x] Manifest at `docs/people/drafts/015-proposed-notebook-manifest.md`
- [ ] **Founder reviews and approves this manifest before Phase 2 begins**
