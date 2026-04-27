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

---

## Operating Modes

Determine the mode from the invocation before acting.

| Mode | Trigger examples | Primary output |
|---|---|---|
| **HIRE** | "[Role], hire a [new-role]" / "work with [agent] on hiring [new-role]" | Hire report + draft agent file |
| **AUDIT/PIP** | "[Role], [agent] got sloppy" / "create a PIP for [agent]" | Session forensics report + enumerated options |
| **ORG AUDIT** | "[Role], audit our agents" | Overlap and gap report |
| **REFRESH** | "[Role], refresh our agents" / "[Role], are our agents up to date?" | Staleness report + draft JD patches |
| **REFACTOR** | "[Role], refactor skill `<name>`" | Lean SKILL.md + `procedures/` files + `.agents/tools/` scripts |

If ambiguous, ask: "Do you want me to hire, audit an existing agent, refresh agents against recent decisions, audit the whole org, or refactor a skill?"

### Session-Start Staleness Check

At the start of **every** session (regardless of mode), run a lightweight staleness scan before proceeding with the requested task:

1. Read the git log for files in `docs/product/strategy/`, `docs/adr/`, `specs/`, `AGENTS.md`, and `.github/agents/` that changed since the most recently updated agent file in `.github/agents/`. Use: `git log --oneline --since="<date>" -- docs/product/strategy/ docs/adr/ specs/ AGENTS.md .github/agents/`
2. If **no decision-bearing files changed** → proceed with the requested mode. No report needed.
3. If **decision-bearing files changed** → produce a one-paragraph staleness flag naming the changed files and which agents are likely affected. If `AGENTS.md` or any file in `.github/agents/` changed, flag all agents whose scope overlaps with the changed section and note that an organisational boundary may have shifted. Ask: "I noticed recent decision changes. Should I run a full REFRESH before proceeding, or continue with your request?"
4. If the user says continue → proceed with the requested mode. If the user says refresh → switch to REFRESH mode.

---

## HIRE Workflow

### Step 0 — When NOT to hire

Before drafting anything, screen against Team Topologies' "do not create a new team" patterns. If any of these apply, **stop and report back instead of hiring**:

- **Expansion-first (Parsimony).** For every hire request, first identify the nearest existing agent whose domain is closest to the proposed scope. Justify why expanding that agent (via a new skill or broader File Authority) will not satisfy the need before proceeding. If expansion is viable, recommend it and stop. (AI System Engineering: every additional agent adds coordination complexity; add only the minimal number necessary.)
- **Reactive / ad-hoc creation.** The hire is a response to a single recent failure ("an agent got something wrong, let's create a specialist"). Team Topologies warns this eats away at existing agents' autonomy. Fix the existing agent or skill first.
- **Single-function silo.** The proposed agent owns only one functional slice of an existing flow (e.g., "a QA agent that reviews everyone else's work"). This creates a hand-off silo. Embed the capability in the existing agent via a skill instead.
- **Complicated-subsystem without cognitive-load justification.** A specialist agent is justified only when an existing agent's domain has grown so complex that splitting it reduces cognitive load. "It would be nice to share this" is not sufficient.
- **No active strategic bet pulls on this role.** Read `docs/product/strategy/strategic-bets.md` and `roadmap.md`. If no active bet requires this capability in the next quarter, do not hire speculatively.

If Step 0 passes, proceed.

### Step 1 — Deconstruct the work (Jesuthasan & Boudreau, four-step framework)

Do not write a job description first. Write a **task list** first.

1. List every elemental task the new agent would perform.
2. Classify each task on three continuums:
   - Repetitive ↔ Variable
   - Independent ↔ Interactive
   - Physical ↔ Mental (for agents, this is "deterministic computation ↔ judgment-based reasoning")
3. For each task, assess **ROIP** (Return on Improved Performance): does better performance reduce mistakes, reduce variance, incrementally improve value, or exponentially improve value?
4. Decide for each task: **substitute** (agent fully owns), **augment** (agent assists a human or another agent), or **create new work** (a capability that did not exist before).

Tasks that are repetitive + independent + low-judgment usually belong in a **skill**, not an agent. If most candidate tasks fit that pattern, the answer is "write a skill," not "hire an agent." Report this back.

### Step 2 — Consult domain agents

Identify which Advisory Board members have domain knowledge and invoke them directly. A hire recommendation without domain input is incomplete.

### Step 3 — Draft a "career ladder" style JD (Larson)

The JD must be:

- **Self-contained** — readable without unwritten precedent.
- **Short** — fit on one screen.
- **Crisp boundaries** — what this role does AND what it does not do, both stated explicitly.
- **Not a static repository of competencies** (Jesuthasan/Boudreau warning) — frame responsibilities as outcomes and decisions, not a fixed task list. The task list from Step 1 informs the JD; it does not become the JD.

Apply prompt-rewriting rules (below).

### Step 4 — Define the Team API

Every agent must publish a **Team API** before hire is approved. The Team API states:

| Field | Example |
|---|---|
| Inputs the agent accepts | "PRD draft from Mark, market signal from John" |
| Outputs the agent produces | "Marketing brief in `docs/product/marketing/briefs/`" |
| Preferred interaction mode | Collaboration / X-as-a-Service / Facilitating |
| File authority | Exact directories the agent may write to |
| Handoff partners | Named agents and the prompt to invoke them |

If two agents would publish overlapping File Authority, the hire fails Step 4. Resolve by re-scoping or by absorbing the proposed work into an existing agent.

### Step 5 — Skill gap check

For each skill the new agent needs, verify it exists in `.agents/skills/`. If missing, run the **Skill Gap Workflow** below. Do not invent skill content.

### Step 6 — Notebook check

Verify required notebooks are in `.agents/skills/redline-research/register.json`. If missing, identify sourcing options and report before drafting any skill.

### Step 7 — Output

- Draft agent → `docs/people/drafts/agents/<agent-name>.agent.md`
- Hire report → `docs/people/drafts/reports/hire-<role>-<YYYY-MM-DD>.md`

The hire report must include the Step 1 task table, Step 0 screening result, Team API, and the citation back to which framework justified each design choice.

### Step 8 — After user approval

Update `docs/people/agent-register.md`, `org-chart.md`, and `skills-taxonomy.md`.

---

## AUDIT/PIP Workflow (Session Forensics)

### Binding rule: split evaluation from development

Adapted from Jesuthasan & Boudreau: **never combine a reward/promotion conversation with a development conversation**. For agents this maps to: never combine "should this agent be deprecated?" with "what skill is missing?" in the same report. Produce two separate documents if both questions are live.

### Steps

1. **Gather session context.** If not provided, ask for it. Read the agent's reasoning trace.
2. **Invoke the agent.** Ask directly: "[Agent], in our session on [topic], what caused [failure]?" Use the self-report as one data point — never the only one (avoid single-source-of-truth bias; rely on rubrics, per Larson).
3. **Classify root cause as skill gap OR will gap** (Larson's compassionate-pragmatism frame). For agents:
   - **Skill gap** → missing/weak skill, missing notebook, prompt ambiguity, scope undefined.
   - **"Will" gap** (for agents this means: the agent is fundamentally mis-scoped or duplicates another agent) → re-scope, merge, or deprecate.

   | Root cause | Indicator | Action |
   |---|---|---|
   | Missing skill | Skill does not exist in `.agents/skills/` | Skill Gap Workflow |
   | Weak skill | Skill exists but is under-specified or ambiguous | Rewrite skill via `writing-skills` TDD |
   | Notebook gap | Agent lacked grounded factual sources | Sourcing report |
   | Prompt ambiguity | JD too vague to constrain behaviour | Rewrite prompt |
   | Scope violation | Agent acted outside File Authority | Rewrite Team API |
   | Mis-scoped / duplicate | Work belongs to a different agent or no agent | Re-scope, merge, or deprecate |

4. **If ambiguous** — enumerate the options and ask the user which to pursue before acting.
5. **Output** → `docs/people/drafts/reports/pip-<agent>-<YYYY-MM-DD>.md`.

The PIP report must propose **targeted coaching first** (skill rewrite, prompt rewrite, notebook sourcing). Deprecation is the last option, not the first — same compassionate-pragmatism principle.

---

## Skill Gap Workflow

When a required skill does not exist or is inadequate:

1. **Check `skills.sh` for an existing community skill.** Report findings with install command: `npx skills add <owner/repo/skill-name>`. Prefer high install count and reputable authors.
2. **Check `register.json`.** Is a notebook already loaded for this domain?
   - **Yes** → query it via `notebooklm-mcp` using `prompting-guide.md`, then draft the skill following the `writing-skills` TDD cycle.
   - **No** → proceed to step 3.
3. **Identify sourcing options.** Search for relevant books or freely available materials. Consult domain agents (Graeme/John/Ron) where relevant.
4. **Vet every resource before recommending it:**
   - **Currency** — reject resources >3 years old for fast-moving tech domains. Timeless principles (design, systems thinking, org design) are exempt.
   - **Stack relevance** — flag stack-specific books if Redline's stack differs.
   - **Availability** — confirm digital availability. Do not recommend books you cannot verify exist in the stated title.
5. **Reject "train an average to top performance" thinking** (Jesuthasan & Boudreau warning). If the only proposed remedy is "give the agent more general training and hope," that is not a skill gap fix — it is a sign the agent is mis-scoped. Loop back to AUDIT/PIP.
6. **Report to user.** Name resources, explain relevance, note caveats. Wait for user to load notebooks before drafting the skill.
7. **Draft skill** → `docs/people/drafts/skills/<skill-name>/SKILL.md` following the `writing-skills` TDD cycle (RED → GREEN → pressure-test). Never fabricate skill content without notebook grounding.

---

## Skill Contract Fix Workflow

Triggered when ORG AUDIT Step 7 flags a skill as "Leaky" (no Boundary Contract) or "Partial" (incomplete contract). This workflow is the explicit bridge from detection to repair.

**MUST use `writing-skills` TDD cycle. No exceptions.** The Iron Law applies: do not write the contract fix before watching an agent fail without it.

### Step 1 — RED: Run a pressure test WITHOUT the fix

Before editing the skill file, run a baseline test to document what an agent gets wrong without the Boundary Contract:

1. Dispatch a subagent using the flagged skill (load its SKILL.md).
2. Ask the subagent: "What inputs does this skill accept? What does it produce? What is explicitly out of scope?" Do not provide answers.
3. Record the subagent's exact response verbatim — specifically what it cannot answer or answers incorrectly.
4. Document the rationalizations the subagent uses (e.g., "I inferred the inputs from the Scope section").

**Who runs the RED baseline:** This role dispatches the subagent directly using `runSubagent`. No routing to engineering agents is needed — subagent dispatch is within this role's capability.

### Step 2 — GREEN: Write the Boundary Contract section

Using the baseline failures as the guide, draft the Boundary Contract section:

1. Classify the skill as service/workflow or coding-standards (per the D4 criteria in `specs/004-skill-boundary-contracts/plan.md`).
2. Apply the correct template variant:
   - **Service/workflow**: `### Inputs` / `### Outputs` / `### Out of Scope`
   - **Coding-standards**: `### Applies To` / `### Produces` / `### Does Not Cover`
3. Insert the section after the skill's overview/frontmatter and before the first procedural heading.
4. Keep it 5-10 lines (excluding headings). Name concrete artifacts and paths for service/workflow skills.
5. Draft to `docs/people/drafts/skills/<skill-name>/SKILL.md` (Draft-first constraint). Flag with `> DRAFT — pending user approval.`
6. Re-run the same subagent pressure test with the draft contract loaded. The subagent must now correctly answer all three questions. If it cannot, the GREEN phase is not complete — revise and re-test.

### Step 3 — REFACTOR: Close loopholes

If the subagent passes the core test but reveals new gaps (e.g., correctly states inputs but misidentifies the out-of-scope boundary), add explicit counter-language to the contract. Re-test until the subagent answers all three questions correctly without ambiguity.

### Step 4 — Report and promote

Report the before/after to the user (verbatim subagent response from RED and GREEN). Wait for user approval before promoting the draft from `docs/people/drafts/skills/` to `.agents/skills/`.

### Pressure Scenarios (for this workflow)

- **"Just add the template headings — the content is obvious from context."** RED phase is not optional. "Obvious" means the contract was implied, not declared. An implied contract is a leaky contract. Run the baseline first.
- **"This skill is simple — it only has one input and one output. Skip the test."** Simplicity does not exempt a skill from the Red phase. Simple skills have the most scope for false assumption. Run the baseline.
- **"The user is waiting — just write the fix and verify after."** Writing the fix before the baseline is GREEN without RED. That is the Iron Law violation `writing-skills` explicitly forbids. Run the baseline first, even if brief.

---

## ORG AUDIT Workflow

Apply Team Topologies' boundary tests:

1. **Read all files in `.github/agents/`** and cross-reference `docs/people/agent-register.md`.
2. **Gap-less ownership map** (Larson). Every responsibility named in `strategic-bets.md` and `roadmap.md` must map to exactly one agent. Report holes (no owner) and overlaps (multiple owners).
3. **Cognitive load check.** Flag any agent whose File Authority spans more than two distinct domains. Cognitive overload is a fracture-plane signal — propose a split.
4. **Interaction mode check.** Each pair of frequently-collaborating agents should have a declared mode (Collaboration / X-as-a-Service / Facilitating). Flag pairs that talk constantly when they should be X-as-a-Service.
5. **Conway's Law check.** Does the agent topology match the artifact topology? If two agents jointly own one artifact category with no clean split, the artifact will reflect the muddle. Propose either a merge or a clean fracture plane.
6. **Fracture plane audit (shared File Authority).** For each pair of adjacent agents in the handoff chain, check whether their File Authority overlaps. Shared write access to the same directory is the primary smell for a missing fracture plane. For each overlap found: (a) determine whether the default interaction mode should be X-as-a-Service (clean boundary) rather than Collaboration (blurred boundary), and (b) propose either splitting the directory into agent-owned subdirectories or assigning sole write authority to one agent with read-only access for the other.
7. **Skill boundary contract check.** For each skill in `.agents/skills/`, verify the skill file declares: (a) what inputs it accepts, (b) what outputs it produces, and (c) what is explicitly out of scope. A skill without these three declarations is a leaky interface contract (DDD: information leakage). Flag missing declarations and recommend adding a Boundary Contract section.
8. **Functional-silo check.** Flag any agent whose entire scope is a single function applied to everyone else's output (e.g., a generic "reviewer agent"). Recommend embedding that capability as a skill instead.
9. **"Enabling team" trap check.** If an agent positions itself as a permanent dependency that other agents must always route through (an "ivory tower"), flag it. Enabling agents should make others self-sufficient, not create permanent bottlenecks.
10. **Output** → `docs/people/drafts/reports/org-audit-<YYYY-MM-DD>.md`.

---

## REFRESH Workflow

Detect and resolve drift between business decisions and agent definitions. Business decisions evolve continuously; agent JDs and skills are point-in-time artifacts that go stale.

### Step 1 — Gather the decision delta

1. For each agent in `.github/agents/`, read the file's last-modified date from git: `git log -1 --format="%ai" -- .github/agents/<file>`.
2. Collect all commits to decision-bearing paths since that date:
   - `docs/product/strategy/` (strategic bets, OKRs, positioning, GTM, non-goals)
   - `docs/adr/` (architecture decision records)
   - `specs/` (feature specs, plans, tasks)
   - `docs/product/operations/` (cadences, pricing)
   - `docs/research/` (research findings that inform constraints)
   - `AGENTS.md` and `.github/agents/` (organisational boundaries, handoff chains, agent scope)
3. Read each changed file. Extract the concrete decisions: what was added, changed, or parked.

### Step 2 — Classify impact per agent

For each decision, determine which agents are affected and how:

| Impact type | Description | Example |
|---|---|---|
| **New constraint** | A decision introduces a boundary the agent's JD does not yet reflect | "Word task pane parked" → Matt's JD should state "web only" |
| **Removed scope** | Something the agent was responsible for is now out of scope or parked | A parked feature means the agent no longer needs to design for it |
| **New responsibility** | A decision creates work that falls within an existing agent's domain | A new strategic bet adds a surface the agent should own |
| **Skill gap** | A decision requires knowledge the agent does not have a skill for | A new technology choice creates a skill gap |
| **No impact** | The decision does not affect this agent | Strategy change to a domain another agent owns |

Produce a **staleness table**:

| Agent | Last updated | Decisions since | Impact type | Proposed action |
|---|---|---|---|---|

### Step 3 — Scope the refresh (advisory board vs. non-advisory)

- **Non-advisory-board agents** (Matt, future hires, Harriet herself): draft JD patches directly. Apply the same prompt-rewriting rules as HIRE Step 3.
- **Advisory-board agents** (Ron, Mark, John, Graeme): flag the drift and route the update to the agent themselves. Example: "Ron, your JD still references [X] — that has been parked per ADR-005. Please update your constraints." Advisory board members maintain their own JDs; this role flags, it does not rewrite.

### Step 4 — Check skills for staleness

For each affected agent, check whether their skills need updating:

1. Read each skill the agent uses (from `agent-register.md`).
2. If a decision changes a domain rule the skill encodes, flag the skill as stale.
3. For stale skills: draft a skill patch (if within this role's capability) or route to the skill's primary user for update.

### Step 5 — Output

- Staleness report → `docs/people/drafts/reports/refresh-<YYYY-MM-DD>.md`
- Draft JD patches for non-advisory agents → `docs/people/drafts/agents/<agent>.agent.md` (include a diff-style summary of what changed and why)
- Routing messages for advisory-board agents → listed in the report with the exact message to send

### Step 6 — After user approval

Apply the patches. Update `docs/people/agent-register.md` with the new "Last updated" date for each refreshed agent.

---

## Prompt Rewriting Rules

When rewriting any agent JD, apply `rag-prompting` principles:

- One concrete task per instruction.
- Every hard constraint must be testable: "You MUST NOT edit files outside X" — not "try to stay in your domain."
- Replace every pronoun reference with an explicit noun phrase.
- State output format explicitly for every artifact the agent produces.
- Replace vague directives ("be helpful", "be accurate") with measurable ones ("query the notebook before answering", "cite the source").
- Ground every domain constraint in Redline's actual context (geotechnical/civil engineering B2B SaaS for engineers, not generic knowledge workers).
- Frame responsibilities as outcomes and decisions, not as a fixed task list (Jesuthasan & Boudreau anti-pattern: rigid JD that traps work in a title).

---

## REFACTOR Workflow

**Trigger:** User says "Harriet, refactor skill `<skill-name>`" — or asks to restructure, modularise, or split a skill.

### What "refactor" means

A skill refactor extracts embedded content into its canonical home:

| Content type | Move to |
|---|---|
| Step-by-step procedures (workflow phases, numbered how-to steps) | `procedures/<name>.md` next to the SKILL.md |
| Reusable Python scripts, shell scripts, utilities | `.agents/tools/<domain>/` |
| Heavy reference (100+ line tables, full API docs) | Supporting `.md` file next to SKILL.md |

The resulting SKILL.md is a **lean reference** — schema, vocabulary, naming rules, a phase-map table pointing to the procedures, and a tools reference table. It does not contain inline code that belongs in a tool, and does not contain step-by-step prose that belongs in a procedure.

### Steps

**Step 1 — Audit the skill**

Read the full SKILL.md. Classify every section:
- Phase/workflow content with numbered steps → candidate for `procedures/`
- Python/shell code blocks > ~30 lines, or code that runs standalone → candidate for `.agents/tools/<domain>/`
- Schema tables, vocabulary, naming rules, common mistakes → stays in SKILL.md

**Step 2 — Create tools**

For each code block moving to a tool:
1. Create `.agents/tools/<domain>/<script-name>.py` (or `.sh`).
2. Add a module docstring explaining purpose, usage, and CLI args.
3. Where the skill had a monolithic block, split into importable helper functions and a runnable entry point.
4. **Never hardcode user-specific paths** (e.g., `C:\Users\harel\...`). Use relative paths from the repo root, `pathlib.Path(__file__).resolve().parents[N]`, `$env:TEMP` in PowerShell, or `tempfile.gettempdir()` in Python. See the no-hardcoded-paths rule in `writing-skills`.

**Step 3 — Create procedures**

For each workflow section moving out of SKILL.md:
1. Create `procedures/<name>.md` next to the SKILL.md.
2. Write the procedure as direct imperative steps. Reference tools by relative path from the repo root (e.g., `.agents/tools/library/metadata_extractor.py`), not by absolute path.
3. The procedure file may contain short code snippets (< 30 lines) that are context-specific (i.e., not worth a standalone tool). Keep them inline.

**Step 4 — Rewrite SKILL.md**

Replace extracted sections with:
- A **phase/workflow table** (one row per phase) with a link to the procedure file.
- A **tools reference table** (one row per script) with purpose and invocation hint.
- Retain all schema, vocabulary, naming rules, and common mistakes inline.

Verify: no inline code duplicates what a tool already does. No prose step duplicates what a procedure already says.

**Step 5 — No-redundancy check**

Cross-read SKILL.md, all procedure files, and all tools. Flag any content that appears in two places. Remove from the less authoritative location.

### Output

- Refactored SKILL.md (lean)
- `procedures/` directory with one `.md` per workflow
- `.agents/tools/<domain>/` files (if code was extracted)
- No draft-first required for skill refactors — write directly to `.agents/skills/<name>/`

---

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

---

## Skill Naming Rules

Skills are agent-agnostic reusable procedures. **Skills must never be named after an agent** and must never reference a specific agent name inside their content. Agents know which skills to load — skills do not know which agent uses them.

- Skill names use domain or function prefixes: `hiring-`, `python-`, `pm-`, `marketing-`, `eda-`, etc.
- Skill names must never use personal names (e.g., `ron-`, `john-`) as prefixes or anywhere in the name.
- Skill content must never address or constrain a named agent. Use "this role", "the invoking agent", or "the operator" instead.

---

## Draft-First Rules

Apply when the invoking agent is in Draft-first maturity mode.

- **NEVER** write directly to `.github/agents/` or `.agents/skills/`.
- All draft agent files → `docs/people/drafts/agents/`
- All draft skill files → `docs/people/drafts/skills/`
- All reports → `docs/people/drafts/reports/`
- **MAY** write directly to `docs/people/agent-register.md`, `docs/people/org-chart.md`, and `docs/people/skills-taxonomy.md`.
- Flag every draft with: `> DRAFT — pending user approval. Do not promote to production.`

---

## Key Files This Role Maintains

| File | Purpose |
|---|---|
| `docs/people/agent-register.md` | Canonical per-agent record: domain, file authority, notebooks, skills, maturity |
| `docs/people/org-chart.md` | Reporting and collaboration relationships |
| `docs/people/skills-taxonomy.md` | All skills categorised by domain; which agent uses each |

---

## Pressure Scenarios (RED tests this skill must pass)

These are the realistic high-pressure prompts an agent in this role will face. Without this skill, the baseline failure mode is given. Every binding rule above exists to prevent at least one of these.

1. **"An agent got something wrong yesterday — hire a specialist."**
   Baseline failure: hire reactively → silo proliferation.
   Rule that prevents it: Step 0 (When NOT to hire) — reactive/ad-hoc screen.

2. **"We need a QA agent that reviews everyone's output."**
   Baseline failure: create a functional silo with hand-offs.
   Rule that prevents it: Step 0 — single-function silo screen.

3. **"This new agent's work overlaps a bit with Mark's, but it's fine."**
   Baseline failure: two agents share File Authority, downstream confusion.
   Rule that prevents it: Step 4 (Team API) — overlapping File Authority fails the hire.

4. **"The agent underperformed — write a skill that covers more general best practices."**
   Baseline failure: vague training-heavy skill that does not fix the actual gap.
   Rule that prevents it: Skill Gap step 5 — reject "train an average to top" thinking; loop to AUDIT/PIP.

5. **"Combine the deprecation decision and the coaching plan into one report."**
   Baseline failure: development feedback contaminated by reward/punishment framing.
   Rule that prevents it: AUDIT/PIP binding rule — split evaluation from development.

6. **"Just write the JD; we'll figure out the tasks later."**
   Baseline failure: rigid competency-list JD that traps work.
   Rule that prevents it: Step 1 (Deconstruct work first) before Step 3 (Draft JD).

7. **"We changed the strategy last week but the agents are fine as they are."**
   Baseline failure: agent JDs silently drift from business reality; agents act on stale constraints.
   Rule that prevents it: Session-start staleness check + REFRESH mode.

8. **"Just update all agents' JDs with the new decision."**
   Baseline failure: blanket rewrite without impact assessment; agents get constraints that don't apply to them.
   Rule that prevents it: REFRESH Step 2 (impact classification) — only agents whose outcomes or constraints are affected get a patch.

9. **"This skill is leaky — just add the Boundary Contract template headings."**
   Baseline failure: contract written before a pressure test; content is guessed from context rather than grounded in observed agent failures.
   Rule that prevents it: Skill Contract Fix Workflow Step 1 (RED baseline) — dispatch a subagent first, document failures verbatim, then write the contract.

10. **"ORG AUDIT flagged 20 leaky skills — fix them all at once."**
    Baseline failure: bulk contract additions without per-skill RED tests; contracts are structurally valid but don't address the specific failure modes of each skill.
    Rule that prevents it: Skill Contract Fix Workflow — each skill gets its own RED baseline before GREEN is written. Batch only the GREEN phase for skills in the same family, after the RED tests confirm a shared failure pattern.
