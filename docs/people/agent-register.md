# Agent Register

**Owner:** Harriet  
**Last updated:** 2026-06-10 *(Topology Sync 2026-06-10 — see `docs/people/drafts/reports/topology-sync-2026-06-10.md`; second pass same day after the live Delta collection closed item A-8 — all eight reflecting agents' statements at `docs/people/drafts/reports/delta-statements-2026-06-10/`)*  
**Source of truth for:** agent domains, file authority, skills, and maturity level.

> Update this file whenever an agent is hired, promoted, audited, or has their scope changed.

---

## Register

> **Notebook access:** See `.agents/skills/redline-research/register.json` (`owner` / `consumers` fields). The "Notebook access" column below contains pointers only — `register.json` is the SSOT per ADR-001.

| Agent | Role | Domain | File Authority | Notebook access | Key Skills | Maturity |
|---|---|---|---|---|---|---|
| **Ron** | Strategy & GTM Advisor | Vision, OKRs, strategic bets, positioning, GTM motion | `docs/product/strategy/`, `docs/research/`, `specs/` | See `register.json` | `pm-product-strategist`, `pm-personas`, `pm-roadmap`, `pm-structural-integrity-auditor`, `miro-mcp` | Autonomous |
| **Mark** | Principal Product Manager | Problem framing, hypotheses, PRDs, decision architecture. Owns acceptance criterion structure and pass/fail confirmation for all domain-specific use cases. Graeme holds domain-content blocking gates within that workflow (see `docs/product/prds/acceptance-test-ownership-policy.md`). | `docs/product/`, `specs/`, `docs/research/` | See `register.json` | `pm-problem-framer`, `pm-hypothesis-builder`, `pm-prd-builder`, `pm-decision-architect`, `pm-personas`, `pm-roadmap`, `pm-prioritization`, `pm-structural-integrity-auditor`, `agile-sprint-planning` *(steward; `agile-daily-standup` is founder-invoked via `/standup`, PM-stewarded)*, `miro-mcp` | Autonomous |
| **John** | Head of Marketing | Content marketing, SEO, social selling, brand voice, demand | `docs/product/marketing/`, `docs/research/`, `specs/` (when asked) | See `register.json` | `marketing-content-big-5`, `marketing-product-led-seo`, `linkedin-social-selling`, `marketing-ai-content-review`, `pm-personas`, `pm-prioritization`, `pm-structural-integrity-auditor`, `miro-mcp`, `qmd-narrative-design` | Autonomous |
| **Graeme** | Principal Geotechnical Engineer | Geotechnical domain expertise, standards, report workflows. Holds three blocking gates in the acceptance test workflow: (1) domain-content assertion sign-off in acceptance criteria; (2) fixture accuracy sign-off; (3) domain accuracy of user-facing LLM explanations before release. | `docs/knowledge/geotechnical/`, `docs/research/` | See `register.json` | `notebooklm-cli`, `redline-research`, `rag-prompting`, `pm-structural-integrity-auditor` | Autonomous |
| **Peter** | Principal Engineer | Architecture, evaluation design, shaping, technical feasibility, quality gate governance, improvement loop, DORA AI capabilities. Three-in-one role: Domain Architect (Larson) + Shaper (Singer) + Advisory Tech Lead (Cagan). Forms the Product Trio with Mark and Matt. Evaluation partnership with Graeme (quarterly retro). | `docs/adr/` (direct), `docs/architecture/` (direct), `docs/evaluation/` (direct), `specs/shaped/` (direct), `docs/research/` (direct) | See `register.json` | `ddd-strategic`, `engineering-architecture`, `create-adr`, `adr-constitution-sync`, `design-eval-rubric`, `design-eval-pipeline`, `define-ai-policy`, `enforce-ai-batch-discipline`, `shaping`, `notebooklm-cli`, `redline-research`, `pm-structural-integrity-auditor`, `miro-mcp` | Autonomous |
| **Harriet** | Head of People & Agent Development | Agent hiring, audits, PIPs, skill gap management, org design, agent register | `docs/people/` (direct); `docs/people/drafts/` for agent and skill proposals | See `register.json` | `hr-hire-agent`, `hr-audit-agent`, `hr-maintain-agent-registry`, `hr-sync-agent-topology`, `writing-skills`, `customization-mechanism-triage`, `notebooklm-cli` | **Draft-first** |
| **Matt** | UI/UX Designer | Interaction design, wireframes, component specs, user flows across four product surfaces (web, Word documents, Word taskpane, email agent) | `docs/product/design/` (write); `specs/`, `docs/product/`, `docs/knowledge/geotechnical/`, `docs/research/` (read) | See `register.json` | `ux-professional-software` *(pending)*, `ux-conversion-design` *(pending)*, `ux-document-design` *(pending)*, `ux-design-critique`, `miro-mcp`, `pm-personas`, `pm-structural-integrity-auditor`, `notebooklm-cli`, Playwright MCP *(website review — built-in)* | **Draft-first** |
| **Linda** | Knowledge Infrastructure Operator | Digital library curation, NotebookLM notebook maintenance, notebook register, standards monitoring | `.agents/skills/redline-research/register.json` (direct write); `G:\My Drive\Library` (read + catalogue) | See `register.json` | `notebooklm-cli`, `notebooklm-index`, `library-management`, `redline-research`, `knowledge-infrastructure` *(pending)* | **Draft-first** |
| **Kabilan** | Python Developer (Senior Software Engineer) | Full-stack Python engineering: implementation, testing, debugging, data pipelines, scripts, application-level infrastructure (cloud/deployment infra is Brent's). No architectural, product, domain, or design decisions. All code subject to founder review. No push to origin without explicit founder instruction. | `src/rl/`, `tests/`, `scripts/` (modify only), `hooks/` (bug fixes only), `output/` (write); `docs/adr/`, `docs/architecture/`, `docs/knowledge/geotechnical/`, `docs/product/prds/`, `docs/product/hypotheses/`, `docs/product/problems/`, `docs/product/design/`, `specs/` (read) | See `register.json` | All 39 Python/engineering skills (loaded on demand): `python-style`, `python-patterns`, `python-typing`, `python-linting`, `python-testing-unit`, `python-testing-api`, `test-driven-development`, `python-static-checks`, `systematic-debugging`, `verification-before-completion`, + 29 others | Autonomous |
| **Brent** | DevOps Engineer (GCP) | Cloud infrastructure provisioning, GCP deployment (Cloud Run), SSO/OAuth (IAP) wiring, CI/CD, IAM/RBAC least-privilege, Cloud SQL, observability, cost controls, SOC 2 technical controls. Does not write Python application code. Cloud/DevOps source-currency triage (routed via Linda). | `deploy/infra/`, `deploy/docker/`, `.github/workflows/`, `.env.example`, `docs/infrastructure/` (write) *(paths relocated from `infra/` 2026-06-10, commit `09d6d8f`; JD patch validated by Brent 2026-06-10 — pending founder promotion)*; `docs/adr/`, `specs/003-platform-website/`, `src/rl/settings.py` + env-consuming files, `tests/` (read) | See `register.json` | Cloud Run/`gcloud`, GitHub Actions CI/CD, IAM least-privilege, infra-boundary-contract, IAP/OAuth, Cloud SQL, observability, cost controls, container tuning, WIF, multi-tenancy, Secret Manager, Terraform IaC *(13 pending — ground from notebooks; `terraform-iac` added per ADR-020)*; `tool-selection`, `git-push-batched`, `session-handover`, `mcp-cce` | Live *(promoted to `.claude/agents/brent.md` 2026-06-07; Autonomous within JD review gates — infra config founder-reviewed before push, Tier-1 GCP needs Peter approval)* |

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

```text
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
