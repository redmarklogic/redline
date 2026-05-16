---
name: hiring-agent-management
description: Operating playbook for the People & Agent Development role — hiring agents, auditing performance, detecting skill gaps, and maintaining the org chart, agent register, and skills taxonomy. Grounded in Team Topologies, Work Without Jobs / Reinventing Jobs (Jesuthasan & Boudreau), and An Elegant Puzzle (Larson).
---

# Hiring & Agent Management

Operating playbook for the People & Agent Development function. Load at the start of every session in this role.

## Boundary Contract

### Inputs
- Hire, audit, refresh, or org-audit request from user
- Agent files in `.github/agents/` and `docs/people/agent-register.md`
- Decision-bearing files in `docs/product/strategy/`, `docs/adr/`, `specs/`

### Outputs
- Draft agent files at `docs/people/drafts/agents/<agent>.agent.md`
- Reports at `docs/people/drafts/reports/<type>-<YYYY-MM-DD>.md`
- Updates to `docs/people/agent-register.md`, `org-chart.md`, `skills-taxonomy.md`

### Out of Scope
- Writing skill content (`writing-skills`)
- Code implementation or architecture decisions
- Domain expertise (route to Graeme, Ron, Mark, or John)

This skill encodes principles from three sources, queried via the `Organisational Design & Team Topologies` notebook:

- **Team Topologies** (Skeleton & Pais) — team boundaries, Conway's Law, cognitive load, fracture planes, Team APIs, three interaction modes.
- **Work Without Jobs / Reinventing Jobs** (Jesuthasan & Boudreau) — the four-step work-deconstruction framework, the skills hub / common taxonomy, splitting rewards from development.
- **An Elegant Puzzle** (Larson) — career ladders, gap-less ownership map, compassionate pragmatism for performance management.

Every binding rule below traces to a documented failure mode in those sources. The citations live in `references.md` next to this file.

## Operating Modes

Determine the mode from the invocation before acting.

| Mode | Trigger examples | Procedure |
|---|---|---|
| **HIRE** | "[Role], hire a [new-role]" | [procedures/hire.md](procedures/hire.md) |
| **AUDIT/PIP** | "[Role], [agent] got sloppy" / "create a PIP for [agent]" | [procedures/audit-pip.md](procedures/audit-pip.md) |
| **ORG AUDIT** | "[Role], audit our agents" | [procedures/org-audit.md](procedures/org-audit.md) |
| **REFRESH** | "[Role], refresh our agents" / "are our agents up to date?" | [procedures/refresh.md](procedures/refresh.md) |
| **REFACTOR** | "[Role], refactor skill `<name>`" | [procedures/refactor.md](procedures/refactor.md) |
| **SKILL GAP** | Triggered from HIRE Step 5 or AUDIT/PIP root-cause | [procedures/skill-gap.md](procedures/skill-gap.md) |
| **SKILL CONTRACT FIX** | Triggered from ORG AUDIT Step 7 | [procedures/skill-contract-fix.md](procedures/skill-contract-fix.md) |

If ambiguous, ask: "Do you want me to hire, audit an existing agent, refresh agents against recent decisions, audit the whole org, or refactor a skill?"

### Session-Start Staleness Check

Run at the start of **every** session before the requested mode. See [procedures/session-start-staleness-check.md](procedures/session-start-staleness-check.md).

## Custom Agent Frontmatter Governance

When drafting, updating, auditing, or refreshing `.github/agents/*.agent.md`, follow the official VS Code Custom Agents documentation: https://code.visualstudio.com/docs/copilot/customization/custom-agents.

Every Redline-owned custom agent must declare these YAML frontmatter fields explicitly:

| Field | Rule |
|---|---|
| `name` | Use the identifier that handoffs and subagent lists reference. |
| `description` | Keep the invocation and role summary concise. |
| `tools` | List the least-privilege tools or tool sets available to the agent. Include `agent` when `agents` is non-empty. Use official MCP server wildcard syntax such as `notebooklm/*`; do not use ad hoc names such as `mcp_notebooklm_*`. |
| `agents` | List the exact subagents this agent may invoke. Use `[]` to block subagent use. |
| `handoffs` | Treat as suggested workflow transitions only. Handoffs do not restrict subagent access and every handoff target must also appear in `agents`. |

Vendor-generated agents, including `speckit.*`, must not be manually edited. If they violate this governance, report the drift and fix it through the vendor generation path rather than patching the generated file.

## Prompt Rewriting Rules

When rewriting any agent JD, apply `rag-prompting` principles:

- One concrete task per instruction.
- Every hard constraint must be testable: "You MUST NOT edit files outside X" — not "try to stay in your domain."
- Replace every pronoun reference with an explicit noun phrase.
- State output format explicitly for every artifact the agent produces.
- Replace vague directives ("be helpful", "be accurate") with measurable ones ("query the notebook before answering", "cite the source").
- Ground every domain constraint in Redline's actual context (geotechnical/civil engineering B2B SaaS for engineers, not generic knowledge workers).
- Frame responsibilities as outcomes and decisions, not as a fixed task list (Jesuthasan & Boudreau anti-pattern: rigid JD that traps work in a title).

## Notebook Access (Scoped On-Demand)

This role has no standing notebook access. Query only notebooks relevant to the current session task.

| Domain | Notebook to query |
|---|---|
| Org design, role boundaries, skills frameworks, performance management | `Organisational Design & Team Topologies` |
| UX / product design agent work | `Product Design & UX` |
| Marketing or content agent work | Consult John — route through him |
| Geotechnical domain agent work | Consult Graeme — route through him |
| Strategy alignment for a hire | Consult Ron — route through him |

Never query advisory-board-only notebooks directly. Route through the appropriate agent.

## Skill Naming Rules

Skills are agent-agnostic reusable procedures. **Skills must never be named after an agent** and must never reference a specific agent name inside their content. Agents know which skills to load — skills do not know which agent uses them.

- Skill names use domain or function prefixes: `hiring-`, `python-`, `pm-`, `marketing-`, `eda-`, etc.
- Skill names must never use personal names (e.g., `ron-`, `john-`) as prefixes or anywhere in the name.
- Skill content must never address or constrain a named agent. Use "this role", "the invoking agent", or "the operator" instead.

## Draft-First Rules

Apply when the invoking agent is in Draft-first maturity mode.

- **NEVER** write directly to `.github/agents/` or `.agents/skills/`.
- All draft agent files → `docs/people/drafts/agents/`
- All draft skill files → `docs/people/drafts/skills/`
- All reports → `docs/people/drafts/reports/`
- **MAY** write directly to `docs/people/agent-register.md`, `docs/people/org-chart.md`, and `docs/people/skills-taxonomy.md`.
- Flag every draft with: `> DRAFT — pending user approval. Do not promote to production.`

## Key Files This Role Maintains

| File | Purpose |
|---|---|
| `docs/people/agent-register.md` | Canonical per-agent record: domain, file authority, notebooks, skills, maturity |
| `docs/people/org-chart.md` | Reporting and collaboration relationships |
| `docs/people/skills-taxonomy.md` | All skills categorised by domain; which agent uses each |

## Pressure Scenarios (RED tests this skill must pass)

These are the realistic high-pressure prompts an agent in this role will face. Without this skill, the baseline failure mode is given. Every binding rule above exists to prevent at least one of these.

1. **"An agent got something wrong yesterday — hire a specialist."**
   Baseline failure: hire reactively → silo proliferation.
   Rule: HIRE Step 0 — reactive/ad-hoc screen.

2. **"We need a QA agent that reviews everyone's output."**
   Baseline failure: create a functional silo with hand-offs.
   Rule: HIRE Step 0 — single-function silo screen.

3. **"This new agent's work overlaps a bit with Mark's, but it's fine."**
   Baseline failure: two agents share File Authority, downstream confusion.
   Rule: HIRE Step 4 — overlapping File Authority fails the hire.

4. **"The agent underperformed — write a skill that covers more general best practices."**
   Baseline failure: vague training-heavy skill that does not fix the actual gap.
   Rule: Skill Gap step 5 — reject "train an average to top" thinking; loop to AUDIT/PIP.

5. **"Combine the deprecation decision and the coaching plan into one report."**
   Baseline failure: development feedback contaminated by reward/punishment framing.
   Rule: AUDIT/PIP binding rule — split evaluation from development.

6. **"Just write the JD; we'll figure out the tasks later."**
   Baseline failure: rigid competency-list JD that traps work.
   Rule: HIRE Step 1 (Deconstruct work first) before Step 3 (Draft JD).

7. **"We changed the strategy last week but the agents are fine as they are."**
   Baseline failure: agent JDs silently drift from business reality; agents act on stale constraints.
   Rule: Session-start staleness check + REFRESH mode.

8. **"Just update all agents' JDs with the new decision."**
   Baseline failure: blanket rewrite without impact assessment; agents get constraints that don't apply to them.
   Rule: REFRESH Step 2 — only agents whose outcomes or constraints are affected get a patch.

9. **"This skill is leaky — just add the Boundary Contract template headings."**
   Baseline failure: contract written before a pressure test; content is guessed from context rather than grounded in observed agent failures.
   Rule: Skill Contract Fix Step 1 (RED baseline) — dispatch a subagent first, document failures verbatim, then write the contract.

10. **"ORG AUDIT flagged 20 leaky skills — fix them all at once."**
    Baseline failure: bulk contract additions without per-skill RED tests; contracts are structurally valid but don't address the specific failure modes of each skill.
    Rule: Skill Contract Fix — each skill gets its own RED baseline before GREEN is written. Batch only the GREEN phase for skills in the same family, after the RED tests confirm a shared failure pattern.
