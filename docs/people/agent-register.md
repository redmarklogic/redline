# Agent Register

**Owner:** Harriet  
**Last updated:** 2026-04-20  
**Source of truth for:** agent domains, file authority, notebook access, skills, and maturity level.

> Update this file whenever an agent is hired, promoted, audited, or has their scope changed.

---

## Register

| Agent | Role | Domain | File Authority | Notebooks (scoped) | Key Skills | Maturity |
|---|---|---|---|---|---|---|
| **Ron** | Strategy & GTM Advisor | Vision, OKRs, strategic bets, positioning, GTM motion | `docs/product/strategy/`, `docs/research/`, `specs/` | Founder Memos *(advisory-board)*, Monetizing & Scaling Innovation *(advisory-board)*, Entrepreneurship & Startup Strategy *(advisory-board)* | `pm-product-strategist`, `pm-personas`, `pm-roadmap`, `pm-structural-integrity-auditor`, `miro-mcp` | Autonomous |
| **Mark** | Principal Product Manager | Problem framing, hypotheses, PRDs, decision architecture | `docs/product/`, `specs/`, `docs/research/` | Writing Specs, Product Roadmapping, Entrepreneurship & Startup Strategy *(advisory-board)* | `pm-problem-framer`, `pm-hypothesis-builder`, `pm-prd-builder`, `pm-decision-architect`, `pm-personas`, `pm-roadmap`, `pm-prioritization`, `pm-structural-integrity-auditor`, `miro-mcp` | Autonomous |
| **John** | Head of Marketing | Content marketing, SEO, social selling, brand voice, demand | `docs/product/marketing/`, `docs/research/`, `specs/` (when asked) | Digital Marketing & Social Selling *(advisory-board)*, Entrepreneurship & Startup Strategy *(advisory-board)*, Monetizing & Scaling Innovation *(advisory-board)* | `marketing-content-big-5`, `marketing-product-led-seo`, `marketing-social-selling-linkedin`, `marketing-ai-content-review`, `pm-personas`, `pm-prioritization`, `pm-structural-integrity-auditor`, `miro-mcp`, `qmd-narrative-design` | Autonomous |
| **Graeme** | Principal Geotechnical Engineer | Geotechnical domain expertise, standards, report workflows | `docs/knowledge/geotechnical/`, `docs/research/` | Engineering Standards, Ground Engineering Magazine, Geotechnical Baseline Reports (GBR), Geotechnical Report Workflows, Risk Assessment in Engineering | `notebooklm-mcp`, `redline-research`, `pm-structural-integrity-auditor` | Autonomous |
| **Harriet** | Head of People & Agent Development | Agent hiring, audits, PIPs, skill gap management, org design, agent register | `docs/people/` (direct); `docs/people/drafts/` for agent and skill proposals | Organisational Design & Team Topologies, Product Design & UX *(scoped on demand)* | `hiring-agent-management`, `writing-skills`, `skills-create`, `notebooklm-mcp` | **Draft-first** |
| **Matt** | UI/UX Designer | Interaction design, wireframes, component specs, user flows for the Redline web platform | `docs/product/design/` (write); `specs/`, `docs/product/`, `docs/knowledge/geotechnical/`, `docs/research/` (read) | Product Design & UX, Information Architecture and Knowledge Management; Digital Marketing & Social Selling *(via John)*, Monetizing & Scaling Innovation *(via John)* | `ux-professional-software` *(pending)*, `ux-conversion-design` *(pending)*, `miro-mcp`, `pm-personas`, `pm-structural-integrity-auditor`, `notebooklm-mcp` | **Draft-first** |

---

## SpecKit Agents (engineering workflow)

These are vendor-managed agents from the `specify` CLI. Do not edit their files manually.

| Agent | Role | Invoked by |
|---|---|---|
| `speckit.specify` | Create or update feature spec from natural language | Mark (handoff after PRD) |
| `speckit.clarify` | Identify underspecified areas in a spec | Mark / engineering |
| `speckit.plan` | Generate implementation plan from spec | Engineering |
| `speckit.tasks` | Generate dependency-ordered tasks from plan | Engineering |
| `speckit.implement` | Execute tasks | Engineering |
| `speckit.analyze` | Cross-artifact consistency analysis | Engineering |
| `speckit.checklist` | Generate custom checklist for a feature | Engineering |
| `speckit.constitution` | Create/update project constitution | Engineering |
| `speckit.taskstoissues` | Convert tasks to GitHub issues | Engineering |

---

## Maturity Levels

| Level | Meaning |
|---|---|
| **Draft-first** | All writes to sensitive paths go to `docs/people/drafts/` first. User must approve before promotion to production. |
| **Autonomous** | Agent writes directly to their declared file authority. |

---

## Handoff Chain (canonical)

```
Graeme (domain facts)
    ↓
Ron (vision → bets → OKRs → positioning → GTM)
    ↓
Mark (problem → hypothesis → PRD) ←→ John (content, SEO, social, campaigns)
    ↓                                         ↓Matt (design specs, wireframes)      published assets / channels
    ↓                                         ↓speckit.* (engineering)            published assets / channels
    ↘                             ↙
        Monthly Signal Report → Ron + Mark

Harriet (orthogonal support function)
    → Consults Ron, Mark, John, Graeme on all hires
    → Owns agent register, org chart, skills taxonomy
    → Drafts new agent JDs and skill files for user approval
```
