# Backlog Cultivation Principles

**Status**: Draft v1 for founder review. **Author**: Mark (PM). **Date**: 2026-06-12.
**Companion document**: `backlog-grooming-skill-design.md` (the repeatable mechanism
that applies these principles).

> Written for the uninitiated. Every framework term is defined on first use. Every
> principle is either cited to a source in the Redline knowledge base (queried via
> NotebookLM on 2026-06-12; raw query transcripts in
> `.agents/tmp/backlog-cultivation-2026-06-12/`) or explicitly flagged as Redline-specific
> judgment where the knowledge base has no grounded material.

---

## Diagnosis

*(Required preamble per my operating constraints: what stage are we at, and which
constraints actually bind?)*

**(a) Current stage.** Redline is a pre-launch, solo-founder company. The founder has
been full-time since 2026-06-01. Sprint 3 is in flight. Bet 1 (the free Skeleton
Generator wedge) carries a launch backstop of 2026-07-31 and a 90-day kill criterion
from Launch Day. The work-tracking system is a single GitHub Projects board
(`redmarklogic`, project 1).

**(b) Constraints that bind right now.**
- **Founder attention is the scarce resource.** Every open backlog item is something
  the founder (and the sprint-planning skill) must re-read, re-judge, and re-dismiss
  at every planning pass.
- **The board is measurably cluttered.** Snapshot 2026-06-12: 106 items total; 69 in
  Backlog; 52 open items with no sprint assigned. The backlog is roughly twice the
  size of everything ever completed (35 Done).
- **Direction has already changed under the backlog.** 26 Architecture Decision
  Records (ADRs — documents that record a binding technical decision and its
  rationale) exist in `docs/adr/`, several bets have been revised (see
  `docs/product/strategy/strategic-bets.md`), and at least one issue (#75) has
  already been closed as superseded. Items written before those decisions may now be
  wrong, redundant, or misdirected.
- **The kill clock is running.** Anything that slows sprint planning or buries
  Bet-1-critical work is a direct cost to survival.

**(c) Constraints that are theoretical only.** Most of the agile literature's
machinery for backlog refinement exists to coordinate *many people*: shared
estimation, stakeholder negotiation, cross-team dependency visibility. At
solo-founder scale those costs barely exist. We should take the literature's
*pruning* discipline and leave most of its *ceremony*.

**Surviving the Round test.** Does backlog cultivation help Redline survive the
current phase? On a **short runway (3–6 months)**: yes — a small, current backlog
keeps sprint planning fast and prevents launch-critical items being "lost in all the
noise" (Continuous Delivery's exact warning, see Principle 1), *provided the
cultivation mechanism itself is cheap and timeboxed*. On a **long runway (2+
years)**: also yes, with more elaborate options available (metrics dashboards,
automated staleness bots). Those elaborate options are justified **only** under the
long-runway assumption, so they are explicitly descoped — see "What we are NOT
doing" at the end.

---

## What is a backlog, and what is "cultivation"?

A **backlog** is the ordered list of work items (features, fixes, infrastructure
tasks, design sessions) that have been captured but not yet started. At Redline this
is the set of GitHub Projects board items in status `Backlog`.

**Backlog refinement** (older name: "grooming") is the recurring activity of keeping
that list honest: re-ordering it, rewriting items as understanding improves, and —
the part most teams skip — **removing items that no longer deserve to exist**. I use
"cultivation" for the whole discipline: a gardener both plants and prunes.

---

## The principles

### Principle 1 — A backlog item is a liability, not an asset

Every item you keep has a carrying cost: it must be re-read, re-judged, and
re-dismissed at every planning pass, and it dilutes attention from what matters.

- *Continuous Delivery* (Humble & Farley) describes exactly our failure mode:
  deferring work creates a "huge list" — a "slippery slope" where some items "will
  never be fixed, some are no longer relevant since the functionality of the
  application has changed, and some are critical... but have been lost in all the
  noise."
- Lean process literature (BPM Common Body of Knowledge and related sources in the
  `business-process-management` notebook) classifies **inventory** and **waiting**
  among the seven wastes — a backlog is an inventory of unstarted work, and it should
  be measured and actively reduced, not accumulated.
- *Software Engineering at Google* (deprecation chapter) states the premise for code,
  which transfers by analogy: "code is a liability, not an asset," and "some of the
  best modifications to a codebase are actually deletions." *(Flagged: the book says
  this about code and systems, not backlog items. The analogy is mine.)*

**Practical meaning for Redline:** the default question at review time is not "is
there any chance this is useful?" (almost everything passes) but "does keeping this
open earn its carrying cost right now?" (most things fail).

### Principle 2 — Items are placeholders, not commitments

- *Clean Agile* (Robert C. Martin): user stories are "placeholders, not
  requirements." They "must start out cheap because a lot of them are going to be
  **modified, split, merged, or even discarded**."
- *Extreme Programming Explained* (Kent Beck): "a plan is an example of what could
  happen, not a prediction of what will happen." The product manager continuously
  adapts stories "to what is really happening now."

**Practical meaning:** there is no sunk cost in a backlog item. Dropping, merging, or
rewriting one is the system working as designed, not an admission of planning
failure. (The exception — a task carried across a sprint boundary without being
split — *is* a planning failure per our Sprint Conventions in `cadences.md`; that is
about committed sprint work, not the backlog.)

### Principle 3 — Dropping is safe, because important ideas come back

- *Shape Up* (Basecamp) is the strongest voice here: they keep **no backlog at all**,
  calling backlogs "big time wasters" where grooming stale ideas "actively prevents
  the team from moving forward on timely projects that matter right now." Their
  operating principle: "**really important ideas will come back to you**" — a real
  problem will resurface through a customer, a bug, or a person who cares enough to
  re-pitch it. "If an idea is only heard once and never again, it probably wasn't a
  real problem to begin with."
- Redline-specific reinforcement *(my judgment, not literature)*: dropping is a
  **reversible decision** — a "two-way door" in the reversible-vs-irreversible
  framework ([Reversible Vs Irreversible](../../../.agents/skills/mental-models/strategic_decisions/reversible-vs-irreversible.md)).
  Closing a GitHub issue does not delete it; it stays searchable and reopenable.
  Reversible decisions deserve a fast, lightweight process, not agonising.

**Practical meaning:** when in doubt between keep and drop, drop. The cost of a wrong
drop is one reopened issue; the cost of systematic wrong keeps is a board nobody
trusts.

### Principle 4 — One backlog, tested against strategy

Two halves to this principle:

**One list.** *Accelerate* (Forsgren, Humble, Kim) and *Continuous Delivery* both
insist on a **single backlog** that unifies features, technical debt, and operational
work — "work is work"; separate piles hide the true queue. Redline already complies
(one board, type expressed via labels). Protect this; never spawn a second tracker.

**Strategy is the membership test.** A backlog item earns its place by serving the
current strategy, not by having once seemed like a good idea:

- *INSPIRED* / *EMPOWERED* (Marty Cagan): backlogs and roadmaps fail when they are
  lists of outputs rather than outcomes; weak teams "just plod through the roadmap
  they've been assigned." Items should trace to an outcome (for us: an active
  strategic bet or OKR — Objectives and Key Results, our quarterly goal framework in
  `docs/product/strategy/okrs/`).
- *The Lean Product Playbook* (Dan Olsen): "ruthless prioritization" so the backlog
  "always reflects the current product strategy"; "items that were considered
  important at one point in time become less important."
- Lean/BPM sources: periodically run a **gap analysis** of current work against
  strategic themes, and work "not delivering on the required strategic themes...
  should be **immediately stopped**." The standing question: "Are we doing the right
  projects in the right order to deliver our strategy?"

**Practical meaning for Redline:** every backlog item must either (a) link to an
active bet in `strategic-bets.md`, (b) be a named dependency of a bet-linked item
(infrastructure, tooling), or (c) carry an explicit founder-stated reason. Items
linked to a *killed or revised-away* bet are presumptive drops.

### Principle 5 — Two backlogs of ideas is fine; two backlogs of work is not

*Continuous Discovery Habits* (Teresa Torres) distinguishes the **development
backlog** (validated, buildable work) from the pile of raw ideas, and warns that
teams are "inundated with too many ideas," producing "endless backlogs." Her
mitigation for valid-but-not-now requests: capture them in a separate "**idea backlog
(not your development backlog)** so that you remember to return to it later." Cagan
agrees from the other side: the development backlog should hold *validated* work —
ideas that survived discovery.

**Practical meaning for Redline:** we already have the idea backlog — it is
`docs/deferred/` (the P-NNN deferred-decision mechanism, each entry with a mandatory
*unfreeze condition* — a specific event or threshold that makes it actionable
again). The board is the development backlog. An idea that is plausible but not
serving a current bet belongs in `docs/deferred/` with an unfreeze condition, **not**
as a board item. This single routing rule is probably the biggest declutter lever we
have. *(Mapping deferred/ to Torres's idea backlog is my judgment; the two-list
distinction itself is hers.)*

### Principle 6 — Cadence: continuously light, periodically structural

- *Clean Agile*: exploration (writing, splitting, re-judging stories) "never stops" —
  it is continuous, not a ceremony.
- *Extreme Programming Explained* prescribes a dual rhythm: a **weekly cycle** (pick
  this week's work) and a **quarterly cycle** (reflect on themes, bottlenecks, and
  "alignment with larger goals").
- *Shape Up*'s warning bounds the cadence from above: grooming must never become a
  standing tax that crowds out timely work.
- *(Gap flagged: no source in our knowledge base prescribes a specific refinement
  ceremony frequency or duration — e.g., the Scrum Guide's refinement guidance is not
  in any notebook. The mapping below is Redline-specific judgment.)*

**Practical meaning for Redline:**

| Rhythm | What happens | Where it already lives |
|---|---|---|
| **Continuous** (every board touch) | Reuse-before-create; route not-now ideas to `docs/deferred/`; write `done_when` at creation | `github-projects` skill, sprint-planning Step 4 |
| **Per sprint** (planning session) | INVEST check on candidates; flag bet-orphans; out-of-scope list | `agile-sprint-planning` skill (already does this for *selected* items only) |
| **Periodic structural pass** (proposed: monthly, ~45 min, timeboxed) | Full-backlog audit: drop / merge / re-parent / update / defer, via the grooming skill | **The gap this initiative fills** — see companion design doc |
| **Quarterly** | Grooming pass runs right after the Strategy Refresh Review, because bet changes are the biggest source of newly-dead items | Aligns with `cadences.md` quarterly review |

### Principle 7 — One owner; the founder decides

- *Clean Agile*: prioritising the backlog is the job of a single accountable role
  (Scrum's "Product Owner"). *XP Explained*: product managers write, pick, adapt, and
  retire stories — continuously, not as a one-time act.

**Practical meaning for Redline:** I (Mark) steward the backlog — I run the passes,
produce the recommendations, and keep the hygiene honest. The **founder** makes every
keep/drop/merge call. I structure decisions; I do not make them unilaterally. This
matches the existing board stewardship note in the `github-projects` skill.

### Principle 8 — Understand before you delete (Chesterton's fence)

*Software Engineering at Google* invokes **Chesterton's fence**: before removing or
changing a thing, understand why it is there. *(Again by analogy — the book applies
it to legacy code.)*

**Practical meaning:** every drop/merge recommendation must carry an *educated
rationale with evidence* — the completed task that superseded it, the ADR that
invalidated it, the bet revision that orphaned it. "Looks old" is not a rationale.
This is why the grooming skill (companion doc) outputs a decision table with an
evidence column, and why low-confidence rows go to consultation (Peter, Graeme, Ron)
before they reach the founder.

### Principle 9 — Freshness is metadata, staleness is a signal — not a verdict

*Software Engineering at Google* attaches "freshness dates" to documentation so that
unreviewed documents announce themselves. *The Lean Product Playbook*'s "water and
ice" image makes the same point for backlogs: the rank order stays frozen most of the
time, and you periodically "melt" it to rearrange or remove items, then refreeze.

**Practical meaning:** an item untouched for a long time is a *flag for review*, not
an automatic drop — age alone never decides (that would violate Principle 8).
*(Gap flagged: no source in our knowledge base gives a numeric staleness threshold.
The proposed convention — flag any Backlog item untouched for 2 sprints with no bet
link — is a Redline invention and needs founder ratification.)*

---

## What healthy looks like for a solo-founder + agent team

*(No grounded literature exists in our knowledge base on backlog hygiene for a
solo-founder-plus-agents organisation — this section is my synthesis of the
principles above filtered through Redline's constraints, and is labelled as such.)*

1. **Small enough to hold in one head.** The founder can read the entire open backlog
   in under ten minutes. As a working heuristic, the Backlog column holds weeks of
   work, not quarters. (69 items at ~5 tasks/sprint is well over a year of inventory
   — far past any defensible buffer.)
2. **Every item answers three questions at a glance:** which bet it serves, what
   "done" looks like (`done_when`), and why it exists (`purpose`). Items that can't
   are either rewritten or routed out.
3. **The board is for work; `docs/deferred/` is for ideas.** Plausible-someday items
   live as P-NNN entries with unfreeze conditions, not as board guilt.
4. **Drops are routine and documented.** A closed-as-groomed issue with a one-line
   rationale and a link to the grooming report is a healthy artifact, not a failure.
5. **The grooming pass is timeboxed** (Stop Rule —
   [Stop Rule](../../../.agents/skills/mental-models/strategic_decisions/stop-rule.md)): a fixed budget per pass,
   processed highest-risk-first; anything unprocessed waits for the next pass. The
   moment grooming becomes a multi-hour ritual, we have recreated the disease Shape
   Up warns about.
6. **Agents follow the same rules.** Agents create tasks through the
   `github-projects` skill with reuse-before-create; no agent closes or rewrites
   board items without founder approval (consistent with guard G5/G7 in that skill).

## What we are NOT doing (descoped under the short-runway test)

- No automated staleness bots, backlog-aging dashboards, or velocity analytics —
  long-runway luxuries.
- No second tracking tool, ever (Principle 4).
- No adoption of Shape Up's "delete the backlog entirely" position. Their argument
  assumes departments full of people who re-surface ideas organically; at solo scale,
  `docs/deferred/` plus a small board is the faithful adaptation, not zero memory.
- No ceremony imported for its own sake (estimation poker, story points): the
  literature's coordination machinery solves problems we do not have.

## Knowledge-base gaps flagged (epistemic honesty)

1. **No numeric staleness threshold** in any notebook source — our "2 sprints
   untouched, no bet link → flag" rule is invented convention, awaiting founder
   ratification.
2. **No Scrum Guide / formal refinement-ceremony mechanics** (e.g., the DEEP
   backlog-quality checklist) in the knowledge base. I have not cited them.
3. **No solo-founder-specific backlog literature** in the knowledge base; the
   "healthy looks like" section is labelled judgment.
4. **Kanban queue-management specifics** (explicit aging policies, queue
   replenishment cadence) are not detailed in the BPM notebook sources — noted by the
   notebook itself in the query response.

## Provenance

Knowledge-base queries run 2026-06-12 via `nlm` CLI against
`software-dev-methodology-eng-org`, `writing-specs`, and
`business-process-management` notebooks (register:
`.agents/skills/redline-research/register.json`). Raw cited transcripts:
`.agents/tmp/backlog-cultivation-2026-06-12/q1–q4*.md`. Board snapshot 2026-06-12 via
`gh project item-list`. Mental models applied: Reversible vs Irreversible Decisions;
Stop Rule.
