# Org Chart

**Owner:** Harriet  
**Last updated:** 2026-06-10 *(Topology Sync 2026-06-10)*  
**Source of truth for:** agent roles, reporting relationships, collaboration patterns, and handoff dependencies.

> Miro is the canonical medium for visual relational artifacts. This file is the Markdown synthesis layer — it captures structure and decisions but is not the visual source of truth.

---

## Organisation Structure

```text
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
├── Peter — Principal Engineer  [AUTONOMOUS]
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
│     Peer: Brent (infra dependency: Kabilan requests env vars/buckets/DB connections; Brent provisions)
│     Decision models: Circle of Competence, Second-Order Thinking
│
├── Brent — DevOps Engineer (GCP)  [AUTONOMOUS within JD gates]
│     Outputs: Cloud Run deployment, .env.example infra contract, IAM config,
│              CI/CD pipeline, docs/infrastructure/ documentation, infra-ready notes
│     Writes to: deploy/infra/, deploy/docker/, .github/workflows/, .env.example, docs/infrastructure/
│     Reads: docs/adr/, specs/003-platform-website/, src/rl/settings.py (env-consuming files), tests/
│     Constraints: no push to origin without founder instruction,
│                  Tier-1 GCP services require Peter approval (blocking),
│                  no Python application code
│     Peer: Kabilan (infra requests); Escalates to: Peter (Tier-1 GCP, ADR authorship)
│
└── Engineering Workflow (speckit.* agents — vendor-managed)
      speckit.specify → speckit.plan → speckit.tasks → speckit.implement
      speckit.analyze, speckit.clarify, speckit.checklist, speckit.constitution
      speckit.taskstoissues
```

---

## Handoff Chain (delivery flow)

```text
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
| Kabilan | Brent | Env var / secret / bucket / DB connection requests — Kabilan tells Brent what the app needs |
| Brent | Peter | Tier-1 GCP service approval (blocking); ADR review for Cloud SQL connection strategy |
| Brent | Kabilan | Updated .env.example + infra-ready note; OAuth handoff checkpoint (redirect URI, scopes, IAP audience) |
| Brent | Founder | All infra config for review before push; option tables for multi-option decisions |
| Linda | Brent | Cloud/DevOps/SOC-2 source-currency triage and notebook-content decisions for GCP/DevOps notebooks |

---

## Agent Maturity Status

| Agent | Maturity | Promoted on |
|---|---|---|
| Ron | Autonomous | — (founding member) |
| Mark | Autonomous | — (founding member) |
| John | Autonomous | — (founding member) |
| Graeme | Autonomous | — (founding member) |
| Harriet | **Draft-first** | Temporary Autonomous grant 2026-06-07 (Brent hire + BOM fix) reverted to Draft-first same day at founder request — see `topology-sync-2026-06-07.md` correction note |
| Matt | **Draft-first** | Pending — awaiting trust milestone |
| Linda | **Draft-first** | Hired 2026-04-25 |
| Kabilan | Autonomous | Hired 2026-05-22 |
| Brent | Autonomous *(within JD gates)* | Hired 2026-06-07 |

---

## Open Headcount

Roles identified as gaps but not yet filled. Harriet maintains this list.

| Role | Identified by | Priority | Status |
|---|---|---|---|
| *(none — all identified gaps currently have a draft or approved agent)* | | | |

> Linda (Knowledge Infrastructure Operator) was hired 2026-04-25 to fill the cross-domain knowledge infrastructure gap identified during the issue #13 screening process.
> Kabilan (Python Developer) was hired 2026-05-22 to fill the engineering execution gap --- 39 orphaned Python skills now have a named agent consumer.
> Brent (DevOps Engineer, GCP) was hired and promoted live 2026-06-07 to fill the cloud/DevOps execution + cloud-source-currency orphan (blocks Bet 1 Skeleton Generator deploy; underwrites Bets 2/4 SOC 2 controls). JD at `.claude/agents/brent.md`; reciprocal handoffs added to Kabilan, Peter, and Linda.
> Topology Sync 2026-06-10: Brent JD patch drafted (Terraform authorship per ADR-020, `deploy/infra/` paths, SSO/IAP alignment with ADR-022) — **validated by Brent at the same-day live Delta collection (item A-8 closed; two wording amendments applied); pending founder promotion**. No new headcount triggers.
> Live Delta collection 2026-06-10 (A-8): all eight reflecting agents submitted verbatim Delta Statements (`docs/people/drafts/reports/delta-statements-2026-06-10/`). Outcome: John and Matt JD patches drafted from self-reported defects (`docs/people/drafts/agents/john.agent.md`, `matt.agent.md`); Ron, Graeme, Peter, Linda confirmed no JD change; Kabilan no-dispatch per standing rule. No reporting-line, maturity, or collaboration-edge changes — structure above remains current. Still no new headcount triggers (the only new orphan-weight work, Terraform authoring, was absorbed by Brent's validated patch).
