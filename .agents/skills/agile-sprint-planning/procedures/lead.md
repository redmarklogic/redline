# Procedure: Lead

Founder states intent; agent interviews until the goal is falsifiable, then reconciles with the backlog. Internal file of `agile-sprint-planning` — not independently dispatchable. On completion, continue to `procedures/commit.md`.

**REQUIRED SUB-SKILL:** `pm-hypothesis-builder` — owns the hypothesis template, the three non-negotiables (named metric, specific threshold, time boundary), the success-AND-failure-threshold rule, the red-flag language list, and hedge rejection. Apply its bars throughout; do not restate them.

**Interview discipline (Redline conventions):** goal-first, backlog-second — Hard Gate 2. Max 3 questions per turn; after each answer attempt a template restatement with gaps marked `[?]`. The PM steward leads; one-hop advisory questions to the Strategy advisor (bet alignment), the Principal Engineer (feasibility), the Domain Expert (terminology) — no chains.

## Layer 1 — Shape (outcome or activity?)

Open with (2 of the turn's 3-question cap):

1. "What question does this sprint answer? Walk me through what you want to prove — what exists now, what will exist at sprint end, and why it matters."
2. "How would you know in two weeks it failed? Describe the happy path a real person would walk through to confirm success."

Follow up until you hold: current state, target state, who benefits, the technical path, and what the sprint is explicitly not trying to do — enough context to run the risk pass yourself (below) without asking the founder to do it. Red-flag/hedged language → halt and re-probe per `pm-hypothesis-builder`.

**Exit:** outcome-framed goal + failure defined. "We shipped X" fails; "X changed by Y" passes.

## Layer 2 — Specificity (four probes, Redline convention)

1. Definition precision — what counts as success; what explicitly does not?
2. Economic constraint — at what cost is this still a success?
3. Time structure — when does the indicator fire; is there a leading signal?
4. Failure definition — what does failure look like?

**Exit:** all four answered without hedging (hedges are unanswered — re-probe).

## Layer 3 — Falsifiability and the failure tripwire

Fit the goal to the `pm-hypothesis-builder` template, extended with its failure clause. Present the filled template; any `[?]` slot → ask, don't claim exit.

**Failure tripwire (mandatory, replaces the old "Stop Rule" — distinct from `mental-models` stop-rule.md, which is a search-budget concept):** the founder completes, verbatim:

> "If by [day N] we have not seen [X], we will [stop / change course]."

Record it word-for-word in the plan under Sprint Goal → Failure looks like. The interview cannot close without it.

## Risk pass — pre-mortem and inversion

**REQUIRED BACKGROUND:** [Pre-mortem](../../mental-models/strategic_decisions/pre-mortem.md) and [Inversion](../../mental-models/general_thinking/inversion.md) for the concepts. Ceremony-specific application:

- Generate both yourself from Layers 1–3 context. Never ask the founder "what could go wrong?" — answer it first.
- Pre-mortem: 3–5 specific failure modes → present; founder confirms, adjusts, or adds.
- Inversion: 3–5 sabotage moves → **internal only, never shown**; use them to derive the critical path.
- One turn (= 2 of the question cap): failure modes for confirmation + the critical path with the full task plan — Gantt block and task table per `reference/plan-format.md`, founder confirms sequencing.

Full-strength, bet-level stress-tests are `strategy-pre-mortem`'s job, not this ceremony's.

## Backlog reconciliation (only after goal + tripwire confirmed)

1. Read the backlog silently (`github-projects` → list-tasks; no narration).
2. Present three buckets: **Serves the goal** (accept as-is) · **Partially fits** (flag the gap; schedule a refinement pass post-session — never refine in-session) · **Gap — no task exists** (name the new tasks).
3. Duplicate test (Torres) per gap item: different problem, or the same problem framed differently? Same → update the existing task; never create a duplicate.
4. INVEST check (SKILL.md table) on every task before presenting.
5. Agent assignment (below) on every task and sub-task.
6. Present the WBS table (`reference/plan-format.md`). No Gantt here — sequencing was confirmed earlier.
7. Founder confirms the task list → `procedures/commit.md`.

## Agent assignment

**REQUIRED BACKGROUND:** `docs/architecture/layer-responsibilities.md` — infer the owning role for each task and sub-task from the layer it touches. There is no mapping table here to maintain (founder ruling 2026-06-12: ownership is inferred from the architecture file, never restated). Resolve role → agent name via the agent register in `docs/people/`.

The assigned agent is the domain expert who owns the spec/decision/brief — **never the implementation agent** (note the implementer in the description: "— [agent] implements"). Assign per sub-task; a parent may span layers.
