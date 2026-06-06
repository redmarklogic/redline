# 015 — Notebook Design Plan

**Spec**: [015-notebooklm-account-migration](../../specs/015-notebooklm-account-migration/spec.md)
**Produced by**: Linda
**Date**: 2026-06-06
**Based on**: [015-proposed-notebook-manifest.md](015-proposed-notebook-manifest.md) (Founder-approved)
**Status**: Awaiting Founder review

---

## Source Methodology

Library sources were located using `G:\My Drive\Library` and `library-index.xlsx` (1489 indexed entries: 1454 standards, 26 books, 9 guidance notes/technical reports).

**Key finding**: Most book-based notebooks contain a mix of (a) PDFs present in the library and (b) sources uploaded as URLs or web pages in the old account. The old account's notebooks were deleted in Phase 0 — their individual source lists are not recoverable. Where a gap exists between the old source count and library-matched sources, it is flagged as `WARN️ UNLOCATED`. These are not missing files — they are likely URL-sourced entries from the old session that must be re-supplied by the notebook owner in Phase 4.

---

## Notebook Creation Table

### New Notebooks (not in old account)

| # | Notebook ID | Name | Access | Source count | Notes |
|---|---|---|---|---|---|
| 1 | `ground-engineering-magazine-2014-2019` | Ground Engineering Magazine (2014–2019) | open | 65 | **NEW** — split from single notebook per spec |
| 2 | `ground-engineering-magazine-2020-2026` | Ground Engineering Magazine (2020–2026) | open | 63 | **NEW** — split from single notebook per spec |

---

### Geotechnical Domain (Graeme)

---

#### `engineering-standards`

| Field | Value |
|---|---|
| **Name** | Engineering Standards |
| **Access** | open |
| **Old source count** | 74 |
| **Confirmed library sources** | 513 in-scope files across SNZ (241), AS-NZS (257), ASNZS (4), NZS (5), Local Authorities (6) |
| **Target source count** | 74 (preserve prior scope) |
| **Source file list** | WARN️ UNRESOLVABLE — requires Founder/Graeme action |

**Source list note**: The old account's 74 sources were deleted in Phase 0 and cannot be reconstructed. The library contains 513 NZ-scope standards (SNZ + AS-NZS + ASNZS + NZS + Local Authorities). Linda cannot select the correct 74 without domain guidance — the selection is an engineering judgment (which standards are actively referenced in Canterbury/NZ geotechnical practice).

**Founder action required**: Graeme to supply a prioritised list of 74 standards from the in-scope folders, or approve Linda selecting the most recently added/modified 74 files from SNZ + AS-NZS + NZS folders.

**Source folders** (in-scope per Graeme's Phase 1 policy):
```
G:\My Drive\Library\Engineering Standards\SNZ\          (241 files)
G:\My Drive\Library\Engineering Standards\AS-NZS\       (257 files)
G:\My Drive\Library\Engineering Standards\ASNZS\        (4 files)
G:\My Drive\Library\Engineering Standards\NZS\          (5 files)
G:\My Drive\Library\Engineering Standards\Local Authorities\ (6 files)
```
Out of scope (Graeme confirmed): ASTM, ISO, BSI-CEN, DIN, BS.

---

#### `ground-engineering-magazine-2014-2019` *(new notebook)*

| Field | Value |
|---|---|
| **Name** | Ground Engineering Magazine (2014–2019) |
| **Access** | open |
| **Source count** | 65 |
| **Source folder** | `G:\My Drive\Library\T - Technology\TA700-712 - Foundation and Geotechnical Engineering\Serials & Periodicals\Ground Engineering Magazine\` |
| **Source file pattern** | `2014-*.pdf`, `2015-*.pdf`, `2016-*.pdf`, `2017-*.pdf`, `2018-*.pdf`, `2019-*.pdf` |
| **All sources located** | OK Yes |

---

#### `ground-engineering-magazine-2020-2026` *(new notebook)*

| Field | Value |
|---|---|
| **Name** | Ground Engineering Magazine (2020–2026) |
| **Access** | open |
| **Source count** | 63 |
| **Source folder** | `G:\My Drive\Library\T - Technology\TA700-712 - Foundation and Geotechnical Engineering\Serials & Periodicals\Ground Engineering Magazine\` |
| **Source file pattern** | `2020-*.pdf`, `2021-*.pdf`, `2022-*.pdf`, `2023-*.pdf`, `2024-*.pdf`, `2025-*.pdf`, `2026-*.pdf` |
| **All sources located** | OK Yes |

---

#### `geotechnical-baseline-reports`

| Field | Value |
|---|---|
| **Name** | Geotechnical Baseline Reports (GBR) |
| **Access** | open |
| **Old source count** | 4 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 4 UNLOCATED — all 4 sources were likely PDFs or URLs not in library index |

**Graeme to re-supply in Phase 4** (ASCE guidelines, CIRIA C807, NZTS guide, FIDIC Emerald Book — likely URL sources from their publishers or CIRIA/FIDIC portals).

---

#### `geotechnical-report-workflows`

| Field | Value |
|---|---|
| **Name** | Geotechnical Engineering Report Workflows and Standard Procedures |
| **Access** | open |
| **Old source count** | 20 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 20 UNLOCATED |

**Note**: Register description states sources come from "a leading NZ geotechnical consultancy's internal knowledge base." These are likely proprietary internal documents not held in `G:\My Drive\Library`. Graeme to confirm source origin and re-supply method in Phase 4.

---

#### `risk-assessment-engineering`

| Field | Value |
|---|---|
| **Name** | Risk Assessment in Engineering |
| **Access** | open |
| **Old source count** | 10 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 10 UNLOCATED — likely ASCE, CIRIA, NZGS guidance documents; URL-sourced or not indexed |

**Graeme to re-supply in Phase 4.** Graeme also flagged: scope-check before migrating — cull any sources that have drifted to general engineering risk rather than geotechnical-specific frameworks.

---

#### `geotechnical-checklists`

| Field | Value |
|---|---|
| **Name** | Geotechnical Engineering Checklists |
| **Access** | open |
| **Old source count** | 10 |
| **Confirmed library sources** | 9 |
| **Source file list** | OK 9 confirmed; WARN️ 1 UNLOCATED |

**Confirmed source files** (all at `G:\My Drive\Library\T - Technology\TA700-712 - Foundation and Geotechnical Engineering\checklists\`):

| File | Description |
|---|---|
| `Geotechnical-Investigations_USACE_2001.pdf` | USACE Engineering Manual EM 1110-1-1804 |
| `Checklist-and-Guidelines-for-Review-of-Geotechnical-Reports_FHWA_1988-alt.pdf` | FHWA review checklist (alt edition) |
| `Checklist-and-Guidelines-for-Review-of-Geotechnical-Reports_FHWA_1988.pdf` | FHWA review checklist |
| `Lodgement-Checklist-Commercial_Unknown_2025.pdf` | Building consent lodgement checklist (commercial) |
| `Guide-for-Geotechnical-Report_CERT_2009.pdf` | Development code: Cert 10a guide |
| `Geotechnical-Report-Submittal-Checklist_MasonCounty_YEAR.pdf` | Mason County submittal checklist |
| `Earthquake-Geotechnical-Engineering-Practice-Module-2_NZGS_2016.pdf` | NZGS Module 2 — Earthquake geotechnical investigations |
| `Geotechnical-Checklist-for-Public-Works-Construction_Unknown_2024.pdf` | Engineering geotechnical checklist for public works |
| `Geotechnical-Design-QC-Checklists_Unknown_2025.pdf` | Design QC checklists (1GT2, 2GT1, 2GT2, 4GT1) |

**Unlocated** (1): One source from old account not in library. Graeme to identify in Phase 4.

---

### AI & Software Architecture (Peter)

---

#### `ai-system-engineering`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 5 |
| **Target source count** | 20+ (Peter's Phase 1 decision) |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ All 5 old sources UNLOCATED; 15+ expansion sources needed |

**Peter to supply full source list in Phase 4.** Old sources were likely URL-based (FastAPI docs, Docker docs, MCP spec, OAuth2 spec, NIST AI RMF). Expansion sources: Peter committed to supplying 15+ titles; none currently in library index.

---

#### `software-architecture-ddd`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 13 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 13 UNLOCATED |

**Note**: Register description cites Evans, Vernon, Khononov, Ford, Ousterhout, GoF and others. None of these are in `library-index.xlsx`. Sources were likely PDFs held elsewhere or URL-based. Peter to re-supply in Phase 4.

---

#### `software-dev-methodology-eng-org`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 25 |
| **Confirmed library sources** | 13 |
| **Source file list** | OK 13 confirmed; WARN️ 12 UNLOCATED |

**Confirmed library sources** (all PDFs; paths relative to `G:\My Drive\Library\`):

| File | Notebook relevance |
|---|---|
| `Q - Science\QA75-76...\Co-Intelligence_Mollick_2024.pdf` | AI/LLM engineering |
| `Q - Science\QA75-76...\Age-of-Invisible-Machines_Wilson_2022.pdf` | AI/LLM engineering |
| `Q - Science\QA75-76...\Designing-Multi-Agent-Systems_Dibia_2025.pdf` | AI/LLM engineering |
| `Q - Science\QA75-76...\Modern-Software-Engineering_Farley_2021.pdf` | Engineering methodology |
| `Q - Science\QA75-76...\LLM-Engineers-Handbook_Iusztin_2024.pdf` | AI/LLM engineering |
| `H - Social Sciences\HD...\Staff-Engineer_Larson_2021.pdf` | Engineering leadership |
| `H - Social Sciences\HD...\Continuous-Discovery-Habits_Torres_2021.pdf` | Product discovery |
| `H - Social Sciences\HD...\Working-Backwards_Bryar_2021.pdf` | Engineering org / Amazon |
| `H - Social Sciences\HD...\Shape-Up_Singer_2019.pdf` | Engineering methodology |
| `H - Social Sciences\HD...\INSPIRED_Cagan_2017.pdf` | Product discovery |
| `H - Social Sciences\HD...\Empowered_Cagan_2020.pdf` | Product discovery |
| `H - Social Sciences\HD...\Product-Led-Growth_Bush_2019.pdf` | Product methodology |
| `H - Social Sciences\HD...\Running-Lean_Maurya_2022.pdf` | Product methodology |

**Unlocated** (12): Mythical Man-Month, Accelerate (Forsgren), Continuous Delivery, Extreme Programming, Clean Agile, Sprint, Lean Product Playbook, Project to Product, Building Applications with AI Agents, Building Generative AI Services with FastAPI, Prompt Engineering for LLMs, Building Generative AI Applications. Peter to re-supply in Phase 4.

---

#### `llm-token-optimisation-agentic-workflows`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | ~26 (from register description; not in old account index) |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ All sources UNLOCATED — 26 blog posts, technical guides, papers, documentation |

**Peter to re-supply in Phase 4** (all sources were URL-based per register description).

---

#### `claude-max-20x-developer-workflow-research`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 8 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 8 UNLOCATED — all sources were URL-based (official docs, community discussions, blog posts) |

**Peter to re-supply in Phase 4.**

---

### Process & Product / Strategy (Mark)

---

#### `business-process-management`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 3 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 3 UNLOCATED |

**Mark to re-supply in Phase 4** (BPM CBOK and methodology books not in library index).

---

#### `product-roadmapping`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 1; target 4-5 (Mark's Phase 1 decision) |
| **Confirmed library sources** | 2 (INSPIRED + Continuous Discovery Habits — also used in software-dev-methodology-eng-org) |
| **Source file list** | WARN️ 1 old source UNLOCATED; Mark to supply 3-4 additional titles |

**Note**: INSPIRED and Continuous Discovery Habits are in the library and can be sourced here. Mark to supply: product-roadmapping-specific titles (Kano reference, MoSCoW reference, OKR/roadmap communication book).

---

#### `writing-specs`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 10 |
| **Confirmed library sources** | 1 |
| **Source file list** | OK 1 confirmed; WARN️ 9 UNLOCATED |

**Confirmed**: `H - Social Sciences\HD...\Shape-Up_Singer_2019.pdf`

**Unlocated** (9): Joel Spolsky specifications book, OKR references, PRD frameworks, discovery vs delivery texts. Mark to re-supply in Phase 4.

---

#### `org-design-team-topologies`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 7 |
| **Confirmed library sources** | 1 |
| **Source file list** | OK 1 confirmed; WARN️ 6 UNLOCATED |

**Confirmed**: `H - Social Sciences\HD...\Staff-Engineer_Larson_2021.pdf` (cross-listed with software-dev-methodology-eng-org)

**Unlocated** (6): Team Topologies book, Conway's Law reference, cognitive load management text, AI/RPA deconstruction text, deliberate practice text, skills-based org text. Mark to re-supply in Phase 4.

**Note**: Org-design split (into `workforce-capability-development`) is **not applied** — awaiting Founder confirmation (OI-2 from manifest).

---

#### `professional-services-firm-management`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 7 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 7 UNLOCATED |

**Mark to re-supply in Phase 4** (A/E/C management books, Innovator's Dilemma, career development texts not in library index).

---

#### `govcon-systems-engineering`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 6 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 6 UNLOCATED |

**Mark to re-supply in Phase 4** (Shipley Proposal Guide and MBSE/SysML texts; Shipley was in old account under a different notebook name).

---

#### `legal-ai-startup`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 2; target 6-8 (Mark's Phase 1 decision) |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 2 old sources UNLOCATED (YC interview transcript, Leya website — URL-based); 4-6 expansion sources needed |

**Mark to supply**: Leya competitor sources (Harvey, Ironclad, Spellbook), legal tech adoption analyst piece, vertical AI GTM writing (a16z/YC). All are URL-based; no library files expected.

---

#### `strategy-competitive-advantage`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | Not in old account index (recently added) |
| **Confirmed library sources** | 2 |
| **Source file list** | WARN️ Source count from old account unknown; library matches may not cover all sources |

**Confirmed library sources**:
- `H - Social Sciences\HD...\The-Art-of-Strategy_Dixit_2008.pdf`
- `H - Social Sciences\HD...\The-Decision-Book_Krogerus_2017.pdf`

**Mark to verify full source list and re-supply any unlocated in Phase 4.**

---

### Founder Strategy (Ron — advisory-board-only)

---

#### `founder-memos`

| Field | Value |
|---|---|
| **Access** | advisory-board-only |
| **Old source count** | 9 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 9 UNLOCATED — voice memo transcripts; not in library |

**Ron/Founder to re-supply in Phase 4** (transcribed voice memos — likely stored outside the library or as Google Docs).

---

#### `monetizing-scaling-innovation`

| Field | Value |
|---|---|
| **Access** | advisory-board-only |
| **Old source count** | 2 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 2 UNLOCATED |

**Ron to re-supply in Phase 4** (Monetizing Innovation + Scaling Innovation books not in library index).

---

#### `entrepreneurship-startup-strategy`

| Field | Value |
|---|---|
| **Access** | advisory-board-only |
| **Old source count** | 20 |
| **Confirmed library sources** | 4 |
| **Source file list** | OK 4 confirmed; WARN️ 16 UNLOCATED |

**Confirmed library sources**:
- `H - Social Sciences\HD...\Running-Lean_Maurya_2022.pdf`
- `H - Social Sciences\HD...\Empowered_Cagan_2020.pdf`
- `H - Social Sciences\HD...\INSPIRED_Cagan_2017.pdf`
- `H - Social Sciences\HD...\Product-Led-Growth_Bush_2019.pdf`

**Unlocated** (16): Crossing the Chasm, Business Model Canvas, Lean Startup (Ries), JTBD texts, B2B sales titles, disruptive innovation texts, corporate innovation frameworks. Ron to re-supply in Phase 4.

---

### UX & Design (Matt)

---

#### `product-design-ux`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 7 |
| **Confirmed library sources** | 3 |
| **Source file list** | OK 3 confirmed; WARN️ 4 UNLOCATED |

**Confirmed library sources**:
- `Q - Science\QA76.9...\Refactoring-UI_Wathan_2018.pdf`
- `Q - Science\QA76.9...\Laws-of-UX_Yablonski_2020.pdf`
- `Q - Science\QA76.9...\About-Face-The-Essentials-of-Interaction-Design_Cooper_2014.pdf`

**Unlocated** (4): The Design of Everyday Things (Norman), Don't Make Me Think Revisited (Krug), Designing with Data, Forms that Work. Matt to re-supply in Phase 4 (likely PDFs or URLs not in library).

---

### Marketing (John — advisory-board-only)

---

#### `digital-marketing-social-selling`

| Field | Value |
|---|---|
| **Access** | advisory-board-only |
| **Old source count** | 9 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 9 UNLOCATED |

**John to re-supply in Phase 4** (marketing books and SEO guides not in library index).

---

### Knowledge Infrastructure (Linda)

---

#### `information-architecture-km`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 3 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 3 UNLOCATED |

**Linda to re-supply in Phase 4** (IA/KM books not in library index).

---

#### `technical-communication`

| Field | Value |
|---|---|
| **Access** | open |
| **Old source count** | 8 |
| **Confirmed library sources** | 0 |
| **Source file list** | WARN️ 8 UNLOCATED |

**Linda to re-supply in Phase 4** (technical writing books not in library index).

---

## Notebook-to-Agent Mapping Table

| Notebook ID | Notebook Name | Access | Primary Agent | Secondary Agents |
|---|---|---|---|---|
| engineering-standards | Engineering Standards | open | Graeme | — |
| ground-engineering-magazine-2014-2019 | Ground Engineering Magazine (2014–2019) | open | Graeme | — |
| ground-engineering-magazine-2020-2026 | Ground Engineering Magazine (2020–2026) | open | Graeme | — |
| geotechnical-baseline-reports | Geotechnical Baseline Reports (GBR) | open | Graeme | — |
| geotechnical-report-workflows | Geotechnical Engineering Report Workflows | open | Graeme | — |
| risk-assessment-engineering | Risk Assessment in Engineering | open | Graeme | — |
| geotechnical-checklists | Geotechnical Engineering Checklists | open | Graeme | — |
| ai-system-engineering | AI System Engineering | open | Peter | Kabilan |
| software-architecture-ddd | Software Architecture & DDD | open | Peter | Kabilan |
| software-dev-methodology-eng-org | Software Development Methodology & Engineering Org | open | Peter | Kabilan |
| llm-token-optimisation-agentic-workflows | LLM Token Optimisation | open | Peter | Kabilan |
| claude-max-20x-developer-workflow-research | Claude Max 20x Developer Workflow Research | open | Peter | Kabilan |
| business-process-management | Business Process Management | open | Mark | — |
| product-roadmapping | Product Roadmapping | open | Mark | — |
| writing-specs | Writing Painless Product and Functional Specifications | open | Mark | Peter |
| org-design-team-topologies | Organisational Design & Team Topologies | open | Mark | Peter |
| professional-services-firm-management | Professional Services Firm Management | open | Mark | — |
| govcon-systems-engineering | Government Contracting, Proposal Management & Systems Engineering | open | Mark | — |
| legal-ai-startup | Legal AI Startup | open | Mark | Ron |
| strategy-competitive-advantage | Strategy & Competitive Advantage | open | Mark | Ron |
| founder-memos | Redline Founder Memos | advisory-board-only | Ron | — |
| monetizing-scaling-innovation | Monetizing & Scaling Innovation | advisory-board-only | Ron | — |
| entrepreneurship-startup-strategy | Entrepreneurship & Startup Strategy | advisory-board-only | Ron | — |
| product-design-ux | Product Design & UX | open | Matt | — |
| digital-marketing-social-selling | Digital Marketing & Social Selling | advisory-board-only | John | — |
| information-architecture-km | Information Architecture and Knowledge Management | open | Linda | — |
| technical-communication | Engineers' Guide to Technical Communication | open | Linda | — |

**Total: 27 notebooks** (26 from register + 1 net new: ground-engineering-magazine split into 2, replacing original 1)

---

## Source Gaps Summary

| Status | Count | Description |
|---|---|---|
| OK Fully located | 2 notebooks | geotechnical-checklists (9/10), ground-engineering-magazine splits (128/128) |
| WARN️ Partially located | 5 notebooks | software-dev-methodology-eng-org, entrepreneurship-startup-strategy, product-design-ux, writing-specs, org-design-team-topologies |
| WARN️ Not located | 18 notebooks | Sources were URL-based or from unindexed files; owners must re-supply |
| ❌ Source list unknown | 1 notebook | engineering-standards (74 sources deleted; fresh selection required from Graeme) |

**This is expected**: the majority of NotebookLM sources in the old account were web URLs (official documentation, publisher pages, online articles). These cannot be located in `G:\My Drive\Library` by design — they are web-sourced. Phase 4 requires each notebook owner to re-supply their URL-based sources.

---

## Open Items for Founder Review

### OI-A: engineering-standards source selection (BLOCKING for Phase 4)

Graeme must supply a prioritised list of 74 standards from the in-scope folders, or confirm that Linda should select the 74 most recently modified files from SNZ + AS-NZS + NZS. The folders contain 513 eligible files; selection requires domain judgment.

### OI-B: Phase 4 owner actions required

Each notebook owner must re-supply their URL-based sources during Phase 4. Linda will notify each owner when their notebook creation is complete (Phase 3) and their population session is due. Owners do not need to act before Phase 3.

---

## Phase 2 Exit Checklist

- [x] All notebooks have a confirmed source file list or a documented gap with resolution path
- [x] No notebook's confirmed source list exceeds 100 files (engineering-standards target ≤74; GEM split: 65+63)
- [x] Missing sources flagged with resolution path (owner re-supply in Phase 4)
- [x] Notebook-to-agent mapping table complete
- [x] Design plan at `docs/people/drafts/015-notebook-design-plan.md`
- [ ] **Founder approves this design plan before notebook creation begins**
