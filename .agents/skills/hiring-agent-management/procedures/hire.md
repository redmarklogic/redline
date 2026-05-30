# HIRE Workflow

## Step 0 — When NOT to hire

Before drafting anything, screen against Team Topologies' "do not create a new team" patterns. If any of these apply, **stop and report back instead of hiring**:

- **Expansion-first (Parsimony).** For every hire request, first identify the nearest existing agent whose domain is closest to the proposed scope. Justify why expanding that agent (via a new skill or broader File Authority) will not satisfy the need before proceeding. If expansion is viable, recommend it and stop. (AI System Engineering: every additional agent adds coordination complexity; add only the minimal number necessary.)
- **Reactive / ad-hoc creation.** The hire is a response to a single recent failure ("an agent got something wrong, let's create a specialist"). Team Topologies warns this eats away at existing agents' autonomy. Fix the existing agent or skill first.
- **Single-function silo.** The proposed agent owns only one functional slice of an existing flow (e.g., "a QA agent that reviews everyone else's work"). This creates a hand-off silo. Embed the capability in the existing agent via a skill instead.
- **Complicated-subsystem without cognitive-load justification.** A specialist agent is justified only when an existing agent's domain has grown so complex that splitting it reduces cognitive load. "It would be nice to share this" is not sufficient.
- **No active strategic bet pulls on this role.** Read `docs/product/strategy/strategic-bets.md` and `roadmap.md`. If no active bet requires this capability in the next quarter, do not hire speculatively.

If Step 0 passes, proceed.

## Step 1 — Deconstruct the work (Jesuthasan & Boudreau, four-step framework)

Do not write a job description first. Write a **task list** first.

1. List every elemental task the new agent would perform.
2. Classify each task on three continuums:
   - Repetitive ↔ Variable
   - Independent ↔ Interactive
   - Physical ↔ Mental (for agents, this is "deterministic computation ↔ judgment-based reasoning")
3. For each task, assess **ROIP** (Return on Improved Performance): does better performance reduce mistakes, reduce variance, incrementally improve value, or exponentially improve value?
4. Decide for each task: **substitute** (agent fully owns), **augment** (agent assists a human or another agent), or **create new work** (a capability that did not exist before).

Tasks that are repetitive + independent + low-judgment usually belong in a **skill**, not an agent. If most candidate tasks fit that pattern, the answer is "write a skill," not "hire an agent." Report this back.

## Step 2 — Consult domain agents

Identify which Advisory Board members have domain knowledge and invoke them directly. A hire recommendation without domain input is incomplete.

## Step 3 — Draft a "career ladder" style JD (Larson)

The JD must be:

- **Self-contained** — readable without unwritten precedent.
- **Short** — fit on one screen.
- **Crisp boundaries** — what this role does AND what it does not do, both stated explicitly.
- **Not a static repository of competencies** (Jesuthasan/Boudreau warning) — frame responsibilities as outcomes and decisions, not a fixed task list. The task list from Step 1 informs the JD; it does not become the JD.

Apply the Prompt Rewriting Rules from the main SKILL.md.

## Step 4 — Define the Team API

Every agent must publish a **Team API** before hire is approved. The Team API states:

| Field | Example |
|---|---|
| Inputs the agent accepts | "PRD draft from Mark, market signal from John" | <!-- hook: allow -->
| Outputs the agent produces | "Marketing brief in `docs/product/marketing/briefs/`" |
| Preferred interaction mode | Collaboration / X-as-a-Service / Facilitating |
| File authority | Exact directories the agent may write to |
| Handoff partners | Named agents and the prompt to invoke them |

If two agents would publish overlapping File Authority, the hire fails Step 4. Resolve by re-scoping or by absorbing the proposed work into an existing agent.

## Step 5 — Skill gap check

For each skill the new agent needs, verify it exists in `.agents/skills/`. If missing, run the Skill Gap procedure (`procedures/skill-gap.md`). Do not invent skill content.

## Step 6 — Notebook check

Verify required notebooks are in `.agents/skills/redline-research/register.json`. If missing, identify sourcing options and report before drafting any skill.

## Step 7 — Output

- Draft agent → `docs/people/drafts/agents/<agent-name>.agent.md`
- Hire report → `docs/people/drafts/reports/hire-<role>-<YYYY-MM-DD>.md`

The hire report must include the Step 1 task table, Step 0 screening result, Team API, and the citation back to which framework justified each design choice.

## Step 8 — After user approval

Update `docs/people/agent-register.md`, `org-chart.md`, and `skills-taxonomy.md`.
