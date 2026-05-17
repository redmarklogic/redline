# Agent Register

**Owner:** Harriet  
**Last updated:** 2026-05-17  
**Source of truth for:** agent domains, file authority, notebook access, skills, and maturity level.

> Update this file whenever an agent is hired, promoted, audited, or has their scope changed.

---

## Register

| Agent | Role | Domain | File Authority | Notebooks (scoped) | Key Skills | Maturity |
|---|---|---|---|---|---|---|
| **Ron** | Strategy & GTM Advisor | Vision, OKRs, strategic bets, positioning, GTM motion | `docs/product/strategy/`, `docs/research/`, `specs/` | Founder Memos *(advisory-board)*, Monetizing & Scaling Innovation *(advisory-board)*, Entrepreneurship & Startup Strategy *(advisory-board)* | `pm-product-strategist`, `pm-personas`, `pm-roadmap`, `pm-structural-integrity-auditor`, `miro-mcp` | Autonomous |
| **Mark** | Principal Product Manager | Problem framing, hypotheses, PRDs, decision architecture. Owns acceptance criterion structure and pass/fail confirmation for all domain-specific use cases. Graeme holds domain-content blocking gates within that workflow (see `docs/product/prds/acceptance-test-ownership-policy.md`). | `docs/product/`, `specs/`, `docs/research/` | Writing Specs, Product Roadmapping, Entrepreneurship & Startup Strategy *(advisory-board)* | `pm-problem-framer`, `pm-hypothesis-builder`, `pm-prd-builder`, `pm-decision-architect`, `pm-personas`, `pm-roadmap`, `pm-prioritization`, `pm-structural-integrity-auditor`, `miro-mcp` | Autonomous |
| **John** | Head of Marketing | Content marketing, SEO, social selling, brand voice, demand | `docs/product/marketing/`, `docs/research/`, `specs/` (when asked) | Digital Marketing & Social Selling *(advisory-board)*, Entrepreneurship & Startup Strategy *(advisory-board)*, Monetizing & Scaling Innovation *(advisory-board)* | `marketing-content-big-5`, `marketing-product-led-seo`, `marketing-social-selling-linkedin`, `marketing-ai-content-review`, `pm-personas`, `pm-prioritization`, `pm-structural-integrity-auditor`, `miro-mcp`, `qmd-narrative-design` | Autonomous |
| **Graeme** | Principal Geotechnical Engineer | Geotechnical domain expertise, standards, report workflows. Holds three blocking gates in the acceptance test workflow: (1) domain-content assertion sign-off in acceptance criteria; (2) fixture accuracy sign-off; (3) domain accuracy of user-facing LLM explanations before release. | `docs/knowledge/geotechnical/`, `docs/research/` | Engineering Standards, Ground Engineering Magazine, Geotechnical Baseline Reports (GBR), Geotechnical Report Workflows, Risk Assessment in Engineering | `notebooklm-mcp`, `redline-research`, `pm-structural-integrity-auditor` | Autonomous |
| **Peter** | Principal Engineer | Architecture, evaluation design, shaping, technical feasibility, quality gate governance, improvement loop, DORA AI capabilities. Three-in-one role: Domain Architect (Larson) + Shaper (Singer) + Advisory Tech Lead (Cagan). Forms the Product Trio with Mark and Matt. Evaluation partnership with Graeme (quarterly retro). | `docs/adr/` (direct), `docs/architecture/` (direct), `docs/evaluation/` (direct), `specs/shaped/` (direct), `docs/research/` (direct) | Software Development Methodology & Engineering Organisation, Software Architecture & Domain-Driven Design, AI System Engineering, Writing Painless Product and Functional Specifications, Business Process Management, Organisational Design & Team Topologies | `engineering-architecture`, `evaluation-architecture`, `shaping`, `ai-acceptable-use-policy`, `notebooklm-mcp`, `redline-research`, `pm-structural-integrity-auditor`, `miro-mcp` | Autonomous |
| **Harriet** | Head of People & Agent Development | Agent hiring, audits, PIPs, skill gap management, org design, agent register | `docs/people/` (direct); `docs/people/drafts/` for agent and skill proposals | Organisational Design & Team Topologies, Product Design & UX *(scoped on demand)* | `hiring-agent-management`, `writing-skills`, `skills-create`, `notebooklm-mcp` | **Draft-first** |
| **Matt** | UI/UX Designer | Interaction design, wireframes, component specs, user flows across four product surfaces (web, Word documents, Word taskpane, email agent) | `docs/product/design/` (write); `specs/`, `docs/product/`, `docs/knowledge/geotechnical/`, `docs/research/` (read) | Product Design & UX, Information Architecture and Knowledge Management; Digital Marketing & Social Selling *(via John)*, Monetizing & Scaling Innovation *(via John)* | `ux-professional-software` *(pending)*, `ux-conversion-design` *(pending)*, `ux-document-design` *(pending)*, `ux-design-critique`, `miro-mcp`, `pm-personas`, `pm-structural-integrity-auditor`, `notebooklm-mcp`, Playwright MCP *(website review — built-in)* | **Draft-first** |
| **Linda** | Knowledge Infrastructure Operator | Digital library curation, NotebookLM notebook maintenance, notebook register, standards monitoring | `.agents/skills/redline-research/register.json` (direct write); `G:\My Drive\Library` (read + catalogue) | Information Architecture and Knowledge Management; all open-access notebooks (operational maintenance) | `notebooklm-mcp`, `redline-research`, `knowledge-infrastructure` *(pending)* | **Draft-first** |

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
    ↓                                         ↓
Peter (shape → Pitch → feasibility)         published assets / channels
    ↓
Matt (design specs, wireframes)
    ↓
speckit.* (engineering)
    ↘                             ↙
        Monthly Signal Report → Ron + Mark

Product Trio: Mark + Matt + Peter (weekly touchpoint)
Evaluation Partnership: Peter + Graeme (quarterly retro)

Internal Operations (platform functions — serve all agents)
    Harriet (people infrastructure)
        → Consults Ron, Mark, John, Graeme, Peter on all hires
        → Owns agent register, org chart, skills taxonomy
        → Drafts new agent JDs and skill files for user approval
    Linda (knowledge infrastructure)
        → Curates digital library at G:\My Drive\Library
        → Maintains NotebookLM notebooks and register.json
        → Routes standards updates to Graeme for triage
```
