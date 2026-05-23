# Org Chart

**Owner:** Harriet  
**Last updated:** 2026-05-22  
**Source of truth for:** agent roles, reporting relationships, collaboration patterns, and handoff dependencies.

> Miro is the canonical medium for visual relational artifacts. This file is the Markdown synthesis layer — it captures structure and decisions but is not the visual source of truth.

---

## Organisation Structure

```
Founder (you)
│
├── Advisory Board (domain experts — consulted, not executive)
│   ├── Ron — Strategy & GTM Advisor
│   │     Outputs: strategic bets, OKRs, positioning, GTM motion
│   │     Writes to: docs/product/strategy/
│   │
│   ├── Mark — Principal Product Manager
│   │     Outputs: problem statements, hypotheses, PRDs, decision logs
│   │     Writes to: docs/product/, specs/
│   │
│   ├── John — Head of Marketing
│   │     Outputs: content briefs, editorial calendar, SEO plans, signal reports
│   │     Writes to: docs/product/marketing/
│   │
│   └── Graeme — Principal Geotechnical Engineer
│         Outputs: domain knowledge documents, fact-checks
│         Writes to: docs/knowledge/geotechnical/
│
├── Peter — Principal Engineer  [DRAFT-FIRST]
│     Archetype: Architect (Larson) + Shaper (Singer) + Advisory Tech Lead (Cagan)
│     Outputs: ADRs, shaped Pitches, evaluation rubric structures, feasibility assessments,
│              architectural constraint tests, quality gate configurations, improvement loop analyses
│     Writes to: docs/adr/, docs/architecture/, docs/evaluation/, specs/shaped/, docs/research/
│     Trio: Mark + Matt + Peter (Product Trio — weekly)
│     Evaluation partner: Graeme (quarterly retro)
│     Proactive briefing: Ron (bet feasibility), John (ADR impacts)
│
├── Internal Operations (platform functions — serve all agents)
│   ├── Harriet — Head of People & Agent Development  [DRAFT-FIRST]
│   │     Outputs: hire reports, PIPs, org chart, agent register, skills taxonomy, draft JDs
│   │     Writes to: docs/people/ (direct); docs/people/drafts/ (proposals)
│   │     Consults: Ron, Mark, John, Graeme (on all hires and PIPs)
│   │
│   └── Linda — Knowledge Infrastructure Operator  [DRAFT-FIRST]
│         Outputs: indexed/tagged library entries, populated notebooks, up-to-date register.json, standards update alerts
│         Writes to: .agents/skills/redline-research/register.json (direct); G:\My Drive\Library (read + catalogue)
│         Routes to: Graeme (standards triage), Ron/Mark/John (domain questions)
│
├── Matt — UI/UX Designer  [DRAFT-FIRST]
│     Outputs: design specs, wireframes (Miro), user flows, component inventories
│     Writes to: docs/product/design/
│     Consults: Mark (PRDs), John (positioning, micro-copy), Graeme (domain terms)
│     Downstream of: Mark (PRDs) → Matt (design) → speckit (engineering)
│
├── Kabilan — Python Developer (Senior Software Engineer)
│     Outputs: implemented code, tests, scripts, hooks, output artifacts
│     Writes to: src/rl/, tests/, scripts/ (modify), hooks/ (bug fixes), output/
│     Reads: docs/adr/, docs/architecture/, docs/knowledge/geotechnical/,
│            docs/product/prds/, docs/product/design/, specs/
│     Constraints: no push to origin without founder instruction,
│                  founder reviews all code, escalates architecture to Peter,
│                  escalates domain to Graeme (via Peter), follows Matt's design specs
│     Decision models: Circle of Competence, Second-Order Thinking
│
└── Engineering Workflow (speckit.* agents — vendor-managed)
      speckit.specify → speckit.plan → speckit.tasks → speckit.implement
      speckit.analyze, speckit.clarify, speckit.checklist, speckit.constitution
      speckit.taskstoissues
```

---

## Handoff Chain (delivery flow)

```
Graeme ──► Ron ──────────────────────────────────────────────────────────┐
(domain)  (vision, bets, OKRs,                                           │
           positioning, GTM)                                             ▼
                │                                               Monthly Signal Report
                ▼                                               ◄── John + Ron + Mark
              Mark ◄────────────────────── John
         (problem → hypothesis → PRD)   (content, SEO,
                │                        social, campaigns)
                ▼
              Peter
         (shape → Pitch → feasibility)
                │
          ┌─────┴─────┐
          ▼           ▼
        Matt     speckit.specify
   (design specs)  speckit.plan
                   speckit.tasks
                   speckit.implement
         │
         ▼
    Kabilan (ad-hoc coding: bugs, refactors, scripts, endpoints)
         │
         ▼
    Peter (Touch 2: architectural review of SpecKit output / Kabilan PRs)
```

---

## Collaboration Matrix

Who consults whom, and for what.

| Agent | Consults | For |
|---|---|---|
| Ron | Graeme | Domain facts before forming any strategy touching geotechnical content |
| Mark | Ron | Strategic bet alignment before writing any PRD |
| Mark | Graeme | Domain accuracy in user flow specs |
| Mark | John | Persona validation, Product-Led SEO PRDs |
| John | Ron | Positioning and ICP before launching campaigns |
| John | Graeme | Technical fact-check before publishing any domain claim |
| John | Mark | Persona sign-off; hands marketing briefs to Mark (never writes PRDs) |
| Harriet | Ron | Strategic fit before recommending a hire |
| Harriet | Mark | Product scope definition for new agent roles |
| Harriet | John | Input on marketing/content agent roles |
| Harriet | Graeme | Input on domain-specific agent roles |
| Harriet | Agent under review | Root cause during a PIP session |
| Matt | Mark | PRD before starting any design work |
| Matt | Peter | Technical constraints before wireframes (Touch 1) |
| Matt | John | Positioning alignment, micro-copy review on conversion surfaces |
| Matt | Graeme | Domain terminology verification on geotechnical designs |
| Matt | Ron | Strategic fit confirmation (on demand) |
| Peter | Graeme | Domain truth for evaluation rubric content (blocking gate) |
| Peter | Ron | Strategic bet context, kill criteria, ICP constraints |
| Peter | Mark | PRD scope, business appetite for shaping |
| Peter | Matt | Design constraints delivery (Touch 1), SpecKit review (Touch 2) |
| Peter | John | Architecture claim verification |
| Mark | Peter | Feasibility assessment, shaping, Pitch approval |
| Ron | Peter | Technical feasibility of strategic bets |
| John | Peter | Architecture claim verification before publishing |
| Graeme | Peter | Evaluation failure triage, rubric structure review |
| Linda | Graeme | Standards triage and domain decisions for geotechnical content |
| Linda | Ron/Mark/John | Domain routing for strategy/product/marketing books |
| Linda | Notebook owner | Approval before reorganising, merging, or deduping notebooks |
| Kabilan | Peter | Architectural decisions, new packages, dependency changes, layer changes, UL stewardship |
| Kabilan | Graeme (via Peter) | Domain terminology ambiguity, domain-content test fixture review |
| Kabilan | Matt | Design specs for user-facing components, design review before shipping |
| Kabilan | Founder | Feature scope confirmation for ad-hoc user-facing work, push approval |

---

## Agent Maturity Status

| Agent | Maturity | Promoted on |
|---|---|---|
| Ron | Autonomous | — (founding member) |
| Mark | Autonomous | — (founding member) |
| John | Autonomous | — (founding member) |
| Graeme | Autonomous | — (founding member) |
| Harriet | **Draft-first** | Pending — awaiting trust milestone |
| Matt | **Draft-first** | Pending — awaiting trust milestone |
| Linda | **Draft-first** | Hired 2026-04-25 |
| Kabilan | Autonomous | Hired 2026-05-22 |

---

## Open Headcount

Roles identified as gaps but not yet filled. Harriet maintains this list.

| Role | Identified by | Priority | Status |
|---|---|---|---|
| *(none — all identified gaps currently have a draft or approved agent)* | | | |

> Linda (Knowledge Infrastructure Operator) was hired 2026-04-25 to fill the cross-domain knowledge infrastructure gap identified during the issue #13 screening process.
> Kabilan (Python Developer) was hired 2026-05-22 to fill the engineering execution gap --- 39 orphaned Python skills now have a named agent consumer.