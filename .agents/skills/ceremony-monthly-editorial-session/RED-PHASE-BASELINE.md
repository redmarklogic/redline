# RED-Phase Baseline — ceremony-monthly-editorial-session

**Date**: 2026-04-19
**Test type**: Baseline failure analysis (no skill loaded)
**Scenario**: User asks the advisory board to run a monthly editorial session

---

## Failure Mode 1: Invocation Ambiguity

**Failure:** The user has no clear entry point. `cadences.md` lists attendees as
"Founder, John (or media team representative)". But the actual session requires four
agents in a specific sequence: Graeme (NZ/AU filter), Ron (strategic context), Mark
(product signal recipient), and John (editorial calendar owner). A user saying "John,
let's run the monthly editorial session" gets John — but John has no instruction to
orchestrate a multi-agent ceremony. A user saying "let's run the editorial session"
gets no agent at all.

**Why it happens without the skill:** No agent's `.agent.md` file references the
monthly editorial session as a ceremony they own or participate in. John's agent file
defines the monthly signal report ritual but not the editorial session. The cadences
doc is an operations reference, not an agent instruction. The system has no routing
rule that maps "monthly editorial session" to a specific agent or sequence.

**Correct behavior:** A single invocation (e.g., "Run the monthly editorial session
for the [Month] Ground Engineering issue") should trigger a structured multi-agent
ceremony with a defined orchestrator (likely John, as custodian per
`archive-intelligence.md`) who coordinates handoffs to Graeme, references Ron's
strategic context, and files outputs to Mark.

---

## Failure Mode 2: Missing Agenda Structure

**Failure:** The 7-step agenda template in `cadences.md` (lines 56-62) will not be
followed. An agent responding ad hoc will likely attempt a general content-planning
conversation rather than executing the specific sequence: (1) identify notable topics,
(2) resonance query, (3) novelty query, (4) Dream 100 commenting query, (5) Big 5
filter, (6) draft post angles, (7) file product signal note.

**Steps most likely skipped:**
- Step 2 (resonance query) — requires knowing the exact NotebookLM query formulation
  from `archive-intelligence.md` Track A, query 1.
- Step 3 (novelty query) — same dependency on Track A, query 2.
- Step 4 (Dream 100 commenting query) — requires knowing Track A, query 3 exists
  and that it needs active Dream 100 targets as input.
- Step 5 (Big 5 filter with discard rule) — agents may suggest Big 5 mapping but
  won't enforce the "discard anything that does not map" hard rule.
- Step 7 (file product signal to Mark) — without the skill, the session ends with
  post angles and forgets the Mark handoff entirely.

**Why it happens without the skill:** The agenda is documented in `cadences.md`, which
is an operations reference document, not a skill or agent instruction. No agent is
instructed to read `cadences.md` before responding. The agenda exists but is invisible
to the agents at invocation time.

**Correct behavior:** The skill should embed the 7-step agenda as a mandatory sequence.
Each step should be a checkpoint that the orchestrating agent must complete before
advancing. Skipping a step requires explicit user override.

---

## Failure Mode 3: Ground Engineering Archive Queries Not Executed

**Failure:** The session requires querying the `ground-engineering-magazine` NotebookLM
notebook using three specific Track A queries defined in `archive-intelligence.md`:
1. Resonance query (cyclical pattern detection)
2. Novelty query (new developments)
3. Dream 100 commenting intelligence query

Without the skill, agents will not know to use the `notebooklm-mcp` tool to query
this specific notebook, will not know the exact query formulations, and will not know
the query sequence matters (resonance before novelty before commenting).

**Why it happens without the skill:** John's agent file lists `notebooklm-mcp` access
but only to marketing notebooks (`Digital Marketing & Social Selling`, etc.). John's
agent explicitly says "Never query: geotechnical/engineering notebooks (Graeme's
domain)." The `ground-engineering-magazine` notebook is Graeme's domain. This creates
a structural gap: the editorial session is John's ceremony but the archive is Graeme's
notebook. Neither agent is instructed to bridge this gap.

**Correct behavior:** The skill should define who queries the archive (likely the
founder, with the skill orchestrating the queries), the exact query formulations from
Track A, and how the results flow to John for Big 5 filtering and post-angle drafting.

---

## Failure Mode 4: Invisibility Protocol Violations

**Failure:** The `archive-intelligence.md` Invisibility Protocol has five binding rules:
1. Never cite the magazine as a personal corpus
2. Do cite specific publicly available articles when it adds credibility
3. Frame as pattern observation
4. Let Graeme be the credibility source
5. Use the archive to ask better questions, not provide answers

Without the skill, agents drafting post angles may produce content that says "according
to Ground Engineering magazine..." or "a 2019 Ground Engineering article showed..."
which reveals systematic multi-year coverage. The invisibility protocol is documented
in `archive-intelligence.md` but no agent is instructed to load this document during
content drafting.

**Why it happens without the skill:** The invisibility protocol lives in a marketing
reference document, not in any agent's hard rules. John's agent has "Never fabricate
market or domain claims" but nothing about the Ground Engineering invisibility
constraint. Graeme's agent has no mention of the invisibility protocol at all. The
protocol is a cross-cutting concern that no single agent owns.

**Correct behavior:** The skill should embed the invisibility protocol as a hard
constraint on all outputs. Every post angle must be checked against the five rules
before approval. The skill should enforce Rule 3 (frame as pattern observation) and
Rule 4 (Graeme is the credibility source) as output formatting requirements.

---

## Failure Mode 5: Output Format Gaps

**Failure:** The session should produce exactly three deliverables (per
`archive-intelligence.md` Track A session outputs):
1. 2-3 approved post angles queued in `editorial-calendar.md`
2. 1-paragraph product signal note filed to Mark (Track B input)
3. Updated Dream 100 commenting notes

Without the skill, agents will likely produce a general content discussion and may
produce post angle suggestions, but will miss the product signal note to Mark
(deliverable 2) and the Dream 100 commenting notes update (deliverable 3). Even
deliverable 1 will lack the required format for `editorial-calendar.md` entries.

**Why it happens without the skill:** No agent has a checklist of required session
outputs. John's agent defines signal report outputs but not editorial session outputs.
The three deliverables are documented in `archive-intelligence.md` under "Session
outputs" but this document is not in any agent's mandatory pre-session reading list.

**Correct behavior:** The skill should define all three deliverables as mandatory
session outputs with specific format templates. The session should not be considered
complete until all three are produced and the user confirms them.

---

## Failure Mode 6: Big 5 Filter Not Enforced as Kill Gate

**Failure:** `cadences.md` step 5 and `content-engine.md` hard constraint 5 both state:
"Every post must map to one of the five Big 5 categories. If it does not map, it does
not go out. No exceptions." Without the skill, agents may suggest Big 5 categories as
a nice-to-have annotation rather than enforcing it as a kill gate. Topics that don't
map to a Big 5 category will survive into the final post angles.

The five Big 5 categories (from `content-engine.md`):
1. Pricing & Costs
2. Problems
3. Versus & Comparisons
4. Reviews
5. Best in Class

**Why it happens without the skill:** John's agent lists `marketing-content-big-5` as
a loadable skill, but loading it requires the agent to recognize the editorial session
as a Big 5 context. Without the ceremony skill triggering the Big 5 skill, John may
skip it. Even if loaded, the Big 5 skill is designed for planning content topics
generally, not for filtering Ground Engineering archive query results specifically.

**Correct behavior:** The skill should make Big 5 filtering a mandatory gate at step 5.
Every topic surfaced by the resonance and novelty queries must be explicitly mapped to
a Big 5 category. Topics that don't map are discarded with a logged reason. The mapping
should be visible in the output so the user can verify it.

---

## Failure Mode 7: Graeme's NZ/AU Applicability Filter Missing

**Failure:** Ground Engineering is a UK-focused publication. `archive-intelligence.md`
explicitly states: "Nothing moves from a query result into a product hypothesis or
Pre-Review rule without Graeme's NZ/AU applicability confirmation." The NZ/AU coverage
caveat lists specific unreliable areas: NZ/AU-specific standards (NZS 3910, AS 4000,
NZGS guidance), NZ/AU contract law, and NZ/AU regulatory environment.

Without the skill, the editorial session may surface UK-specific topics (e.g., Eurocode
7 compliance patterns, UK CDM regulations, CIRIA guidance) and draft post angles for
a NZ/AU audience without Graeme validating relevance.

**Why it happens without the skill:** The NZ/AU filter is defined in
`archive-intelligence.md` under Track B (quarterly product intelligence), and the
language is strongest there. Track A (monthly editorial) references Graeme only in
step 6: "Assign to Graeme for technical review if needed" — the weaker "if needed"
qualifier means an agent will likely skip Graeme unless the content is obviously
technical. But geographic applicability is not obviously technical; it's a subtle
domain judgement that Graeme must make.

**Correct behavior:** The skill should make Graeme's NZ/AU applicability check
mandatory for every topic surfaced from the Ground Engineering archive, not just
those that seem "technical." The check should happen before Big 5 filtering (between
steps 4 and 5) so that irrelevant UK-only topics are discarded early.

---

## Failure Mode 8: Handoff Sequence Ambiguity

**Failure:** The handoff chain in `AGENTS.md` is:
```
Graeme (domain facts) -> Ron (vision, bets, positioning)
                          -> Mark (problem, hypothesis, PRD)
                          -> John (content, SEO, social selling)
```

But the editorial session's actual data flow is different:
```
Archive query results
  -> Graeme (NZ/AU applicability filter)
  -> Big 5 filter (John's domain)
  -> Post angle drafting (John)
  -> Technical review (Graeme again, for claims in draft)
  -> Product signal note (filed TO Mark, not FROM Mark)
  -> Dream 100 notes (John)
```

Without the skill, the generic handoff chain will be applied, which means:
- Graeme gets invoked first (correct) but for domain facts generally, not for
  NZ/AU applicability specifically.
- Ron gets invoked next (incorrect — Ron has no role in the monthly editorial
  session, only in the quarterly strategy refresh).
- Mark gets invoked to produce something (incorrect — Mark is a recipient, not a
  producer, in this ceremony).
- John gets invoked last (partially correct — but by then the handoff context is
  muddled).

**Why it happens without the skill:** The generic handoff chain is the only sequence
agents know. There is no ceremony-specific override. The `cadences.md` attendee list
("Founder, John") doesn't match the actual multi-agent involvement, creating further
confusion.

**Correct behavior:** The skill should define a ceremony-specific handoff sequence
that overrides the generic chain for this context. The sequence should be:
1. Founder identifies 3-5 topics from the new issue (pre-session input)
2. Orchestrator runs Track A queries against the archive
3. Graeme filters results for NZ/AU applicability
4. John applies Big 5 filter (discard non-mapping topics)
5. John drafts 2-3 post angles
6. Graeme reviews any technical claims in the drafts
7. John files product signal note to Mark
8. John updates Dream 100 commenting notes
9. Session complete — outputs confirmed

---

## Summary of Structural Gaps

| # | Failure Mode | Root Cause | Severity |
|---|---|---|---|
| 1 | Invocation ambiguity | No agent owns or routes the ceremony | **High** — session cannot start correctly |
| 2 | Missing agenda structure | Agenda in ops doc, not in agent instructions | **High** — session drifts without structure |
| 3 | Archive queries not executed | Notebook ownership conflict (John's ceremony, Graeme's notebook) | **Critical** — core value of session lost |
| 4 | Invisibility protocol violations | Protocol in reference doc, not in agent hard rules | **Critical** — brand/positioning damage |
| 5 | Output format gaps | Deliverables defined in reference doc, not in agent checklist | **High** — incomplete session outputs |
| 6 | Big 5 filter not enforced | Kill-gate semantics not embedded in any agent | **Medium** — off-brand content may pass |
| 7 | NZ/AU filter missing | Track A has weak "if needed" qualifier for Graeme | **High** — irrelevant UK content for NZ/AU audience |
| 8 | Handoff sequence ambiguity | Generic chain doesn't match ceremony-specific flow | **Medium** — wasted agent invocations, confused context |

## Conclusion

Without a dedicated skill, the monthly editorial session has **zero probability** of
executing correctly on first invocation. The most critical gaps are (3) and (4): the
session's core value proposition (archive intelligence) cannot be accessed correctly,
and the invisibility protocol that protects the founder's positioning has no
enforcement mechanism.

The skill must solve: routing (who orchestrates), sequencing (the 7+ step agenda),
tooling (NotebookLM queries with exact formulations), constraints (invisibility
protocol, Big 5 kill gate, NZ/AU filter), outputs (three mandatory deliverables with
formats), and handoffs (ceremony-specific override of the generic chain).
