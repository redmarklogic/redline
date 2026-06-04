# Work Order: Recreate NotebookLM Notebooks — New Google Account Migration

**To:** Linda
**From:** Mark
**Date:** 2026-06-04
**Priority:** High
**Due:** Before 2026-06-20 (Sprint 1 knowledge infrastructure gate)

---

## Context

Redline migrated to a new Google account. The new account has no NotebookLM notebooks.
The old notebooks are no longer accessible. `register.json` retains the canonical notebook
definitions (names, descriptions, topics, access levels) but all URLs are now stale.

Linda must recreate every notebook in the new account, repopulate each one from the digital
library, and update `register.json` with the new URLs.

---

## Prerequisite (Founder Action — Blocking)

**Install the NotebookLM MCP CLI before Linda begins.**

Linda's `mcp-notebooklm` skill requires the NotebookLM MCP tool to be installed and
authenticated against the new Google account. Linda cannot create or populate notebooks
without this tool. Founder must complete this step and confirm before Linda is invoked.

- [ ] **Founder:** Install the NotebookLM MCP CLI and authenticate against the new Google account
- [ ] **Founder:** Confirm to Linda that `mcp-notebooklm` is operational in the new account

---

## Task

Once the MCP CLI is operational:

1. **Recreate all notebooks** listed in `register.json` in the new Google account, using the
   canonical `name`, `description`, and `access` from each register entry.
2. **Repopulate each notebook** from the digital library (`G:\My Drive\Library`) using the
   source files that correspond to each notebook's topics and `content_types`. Use the
   `library-management` skill to identify which files belong to which notebook.
3. **Update `register.json`** — replace the stale URL for each entry with the new notebook URL.
   Do not change any other register fields (name, description, topics, access, content_types,
   use_cases). Update `added` date only if a notebook is newly created with no prior history;
   preserve the original `added` date for all migrated notebooks.

---

## Notebooks to Recreate (from `register.json`)

All 24 notebooks. Work in access-tier order: `open` notebooks first, then `advisory-board-only`.

| ID | Name | Access |
|---|---|---|
| `engineering-standards` | Engineering Standards | open |
| `ground-engineering-magazine` | Ground Engineering Magazine | open |
| `geotechnical-baseline-reports` | Geotechnical Baseline Reports (GBR) | open |
| `geotechnical-report-workflows` | Geotechnical Engineering Report Workflows and Standard Procedures | open |
| `risk-assessment-engineering` | Risk Assessment in Engineering | open |
| `ai-system-engineering` | AI System Engineering | open |
| `software-architecture-ddd` | Software Architecture & Domain-Driven Design | open |
| `business-process-management` | Business Process Management | open |
| `product-roadmapping` | Product Roadmapping | open |
| `writing-specs` | Writing Painless Product and Functional Specifications | open |
| `technical-communication` | Engineers' Guide to Technical Communication | open |
| `information-architecture-km` | Information Architecture and Knowledge Management | open |
| `product-design-ux` | Product Design & UX | open |
| `org-design-team-topologies` | Organisational Design & Team Topologies | open |
| `professional-services-firm-management` | Professional Services Firm Management | open |
| `govcon-systems-engineering` | Government Contracting, Proposal Management & Systems Engineering | open |
| `legal-ai-startup` | Legal AI Startup | open |
| `geotechnical-checklists` | Geotechnical Engineering Checklists | open |
| `software-dev-methodology-eng-org` | Software Development Methodology & Engineering Organisation | open |
| `llm-token-optimisation-agentic-workflows` | LLM Token Optimisation — Agentic VS Code Copilot Workflows | open |
| `strategy-competitive-advantage` | Strategy & Competitive Advantage | open |
| `claude-max-20x-developer-workflow-research` | Claude Max 20x — Developer Workflow Adaptation Research | open |
| `founder-memos` | Redline Founder Memos | advisory-board-only |
| `monetizing-scaling-innovation` | Monetizing & Scaling Innovation | advisory-board-only |
| `entrepreneurship-startup-strategy` | Entrepreneurship & Startup Strategy | advisory-board-only |
| `digital-marketing-social-selling` | Digital Marketing & Social Selling | advisory-board-only |

---

## Definition of Done

- [ ] Founder confirms NotebookLM MCP CLI is installed and authenticated (prerequisite gate)
- [ ] All 22 `open` notebooks recreated in new account with correct names and descriptions
- [ ] All 4 `advisory-board-only` notebooks recreated with correct names and descriptions
- [ ] Each notebook repopulated with sources from `G:\My Drive\Library` matching its topic area
- [ ] `register.json` updated — all 26 entries have live URLs pointing to the new account
- [ ] No other register fields modified (names, descriptions, topics, access levels preserved)
- [ ] Linda confirms completion to Mark with a source-count summary per notebook
