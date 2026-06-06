# Data Model: NotebookLM Account Migration (Spec 015)

---

## Entities

### NotebookManifestEntry

The unit of agreement produced by Phase 1 consultations. One entry per proposed notebook.

| Field | Type | Source |
| --- | --- | --- |
| `id` | string | Preserved from `register.json` (or new kebab-case slug for new notebooks) |
| `name` | string | Confirmed by owner agent during consultation |
| `description` | string | Confirmed by owner agent (or revised during consultation) |
| `topic_area` | string | Preserved from `register.json` |
| `access` | string | `"open"` or `"advisory-board-only"` — confirmed by owner agent |
| `primary_agent` | string | Agent who owns this notebook |
| `secondary_agents` | string[] | Agents who consume but do not own |
| `projected_source_count` | int | Rough estimate produced in Phase 1 by querying `library-index.xlsx` — for risk-flagging only; exact count is established in Phase 2 |
| `split_of` | string \| null | If this entry was split from a prior notebook, the original `id` |
| `split_rationale` | string \| null | Why the split was made (e.g., "100-source limit") |
| `status` | string | `draft` → `approved` → `created` → `populated` |

**State transitions**:

```
draft (Phase 1 output)
  → approved (Founder approves manifest at Phase 1 review gate)
  → created (Phase 3: notebook exists in new account; URL recorded)
  → populated (Phase 4: all sources added; count confirmed)
```

---

### RegisterEntry

The canonical record in `.agents/skills/redline-research/register.json`. Schema is fixed
(see research.md). The migration touches only the `url` field per entry. No other fields
are modified.

**Mutation during migration**:

- Phase 3: `url` updated from stale old-account URL to new-account URL
- All other fields: preserved verbatim from prior entry

---

### SourceFileRecord

Produced during Phase 2 for each notebook. Maps a notebook to its physical source files.

| Field | Type | Notes |
| --- | --- | --- |
| `notebook_id` | string | FK → `NotebookManifestEntry.id` |
| `file_path` | string | Absolute path under `G:\My Drive\Library` |
| `file_name` | string | Canonical filename as stored in library |
| `content_type` | string | From library metadata (e.g., `"standard"`, `"book"`, `"magazine"`) |
| `upload_status` | string | `pending` → `uploaded` → `failed` |

---

## Draft Artifacts (Phase Outputs)

| Phase | File | Contents |
| --- | --- | --- |
| 1 | `docs/people/drafts/015-proposed-notebook-manifest.md` | `NotebookManifestEntry` records in Markdown table; one row per proposed notebook |
| 2 | `docs/people/drafts/015-notebook-design-plan.md` | `SourceFileRecord` list per notebook; notebook-to-agent mapping table |
| 3–4 | `docs/people/drafts/015-register-draft.json` | Full `register.json` array with live URLs replacing stale ones |

---

## Notebook-to-Agent Mapping (current, pre-consultation)

This table reflects the pre-consultation state from `register.json`. It will be revised
in Phase 1 and finalised in Phase 2. Columns: notebook ID, primary agent, secondary
agents (consumers, not owners).

| Notebook ID | Primary Agent | Secondary Agents |
| --- | --- | --- |
| engineering-standards | Graeme | — |
| ground-engineering-magazine | Graeme | — |
| geotechnical-baseline-reports | Graeme | — |
| geotechnical-report-workflows | Graeme | — |
| risk-assessment-engineering | Graeme | — |
| geotechnical-checklists | Graeme | — |
| ai-system-engineering | Peter | — |
| software-architecture-ddd | Peter | — |
| software-dev-methodology-eng-org | Peter | — |
| llm-token-optimisation-agentic-workflows | Peter | — |
| claude-max-20x-developer-workflow-research | Peter | — |
| business-process-management | Mark | — |
| product-roadmapping | Mark | — |
| writing-specs | Mark | Peter (consumer) |
| product-design-ux | Matt | Mark |
| org-design-team-topologies | Mark | Peter (consumer) |
| professional-services-firm-management | Mark | Graeme (TBC in consultation) |
| govcon-systems-engineering | Mark | — |
| legal-ai-startup | Mark | Ron (consulted on GTM framing) |
| strategy-competitive-advantage | Ron | Mark |
| information-architecture-km | Linda | — |
| technical-communication | Linda | — |
| founder-memos | Ron | — |
| monetizing-scaling-innovation | Ron | — |
| entrepreneurship-startup-strategy | Ron | — |
| digital-marketing-social-selling | John | — |

_Note: `strategy-competitive-advantage` primary owner listed as Ron pending Phase 1 confirmation with Ron and Mark._
