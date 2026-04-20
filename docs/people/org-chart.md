# Org Chart

**Owner:** Harriet  
**Last updated:** 2026-04-20  
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
├── Harriet — Head of People & Agent Development  [DRAFT-FIRST]
│     Outputs: hire reports, PIPs, org chart, agent register, skills taxonomy, draft JDs
│     Writes to: docs/people/ (direct); docs/people/drafts/ (proposals)
│     Consults: Ron, Mark, John, Graeme (on all hires and PIPs)
│
├── Matt — UI/UX Designer  [DRAFT-FIRST]
│     Outputs: design specs, wireframes (Miro), user flows, component inventories
│     Writes to: docs/product/design/
│     Consults: Mark (PRDs), John (positioning, micro-copy), Graeme (domain terms)
│     Downstream of: Mark (PRDs) → Matt (design) → speckit (engineering)
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
          speckit.specify
          speckit.plan
          speckit.tasks
          speckit.implement
         (engineering delivery)
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
| John | Mark | Persona sign-off; hands marketing briefs to Mark (never writes PRDs herself) |
| Harriet | Ron | Strategic fit before recommending a hire |
| Harriet | Mark | Product scope definition for new agent roles |
| Harriet | John | Input on marketing/content agent roles |
| Harriet | Graeme | Input on domain-specific agent roles |
| Harriet | Agent under review | Root cause during a PIP session |
| Matt | Mark | PRD before starting any design work |
| Matt | John | Positioning alignment, micro-copy review on conversion surfaces |
| Matt | Graeme | Domain terminology verification on geotechnical designs |
| Matt | Ron | Strategic fit confirmation (on demand) |

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

---

## Open Headcount

Roles identified as gaps but not yet filled. Harriet maintains this list.

| Role | Identified by | Priority | Status |
|---|---|---|---|
| *(none — all identified gaps currently have a draft or approved agent)* | | | |
