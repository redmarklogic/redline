# Discovery Interview Guide — KR2 Conversations

**Status**: Draft v1. **Owner**: Mark (uses); Ron (custodian).
**Anchored to**: `okrs/2026-h2.md` KR2 (15 qualified discovery conversations in 90 days)
and `jtbd.md`.

> This guide exists because the H2 plan commits to founder-led discovery conversations
> without specifying *how* to run one. The structure below is grounded in two
> methodologies — Christensen / Moesta "Switch" interviews and Steve Blank Customer
> Development — adapted to a solo founder targeting NZ/AU geotechnical engineers.

## Two Methodologies, One Guide

| Source | What it gives us |
| --- | --- |
| Christensen / Moesta "Switch" interview | The *story* — uncover the real Job by tracing the customer's switch timeline. |
| Steve Blank — Customer Development | The *posture* — founder-only, no pitching, validate the problem before the solution. |

## Hard Rules (Do Not Violate)

1. **The founder runs the interview.** Not delegated to advisors, not delegated to Mark
   in early KR2 cycles. Customer Development requires the person with authority to pivot
   to be in the room (Blank).
2. **Do not pitch the solution.** Discussing Pre-Review features in the first half of
   the interview invalidates the data. Customers will give polite affirmation rather
   than reveal real pain (Christensen / Moesta).
3. **Do not ask what they want.** Ask what they *did* the last time they faced this
   situation. Demonstrated behaviour beats stated preference.
4. **Founder talks ≤ 30% of the time.** If the founder is talking more than the
   engineer, the founder is pitching, not discovering (Blank).
5. **Record the four forces, not just the quotes.** Push, Pull, Anxiety, Habit (Moesta).
   See "Force Field Capture" below.

## Interview Structure (45 minutes)

### Part 1 — Set the frame (3 minutes)

> "I'm not selling anything today. I'm trying to understand how engineers in NZ/AU
> actually work through a GBR draft. I want to hear about the *last time* you wrote
> one — what happened, what worked, what frustrated you. There are no wrong answers."

This frame matters. It removes the customer's pitch-defence reflex and licenses
honest answers.

### Part 2 — The Switch Timeline (25 minutes)

Trace the customer's last GBR or GIR draft using the five Switch steps (Moesta):

1. **First thought.** "Think back to the last GBR you drafted. When did you first
   realise you needed help — that the senior-review round was going to be painful?
   What was happening that week?"
2. **Passively looking.** "Did you start noticing things — tools, articles, peer
   comments — about how others handle this? What did you notice?"
3. **Actively looking.** "Did you go look for a tool, ask a peer, search for a
   template? Walk me through it. What did you try? What did you reject and why?"
4. **Deciding.** "How did you decide what to do? Who else was involved? What was the
   moment you committed to the path you took?"
5. **Consuming.** "How did it actually go? What did you do over the following days
   and weeks? Were you satisfied?"

Probe each step. Silence is your friend. The interesting data lives in the pause.

### Part 3 — Four Forces (10 minutes)

Map the customer's words into the four forces. Ask explicitly if not surfaced:

- **Push** (frustration with status quo): "What was the most frustrating part of how
  you handled it?"
- **Pull** (attraction of an alternative): "What would the *ideal* outcome have looked
  like? What kept pulling at you?"
- **Anxiety** (fear of switching): "When you considered trying something new — like
  ChatGPT or another tool — what stopped you?"
- **Habit** (allegiance to status quo): "What about the way you currently do it would
  you actively miss if it changed?"

A real switch happens only when (Push + Pull) > (Anxiety + Habit). If Anxiety and
Habit dominate, the JTBD is real but the buying moment is not.

### Part 4 — Workflow context (5 minutes)

Operational discovery — feeds Sprint 1 PRD acceptance criteria:

- "Walk me through the tooling you use — Word, what add-ins, what templates, what
  reference standards do you keep open?"
- "What does your firm's internal review process look like, end to end?"
- "If you used a quality tool, would you tell your senior reviewer? Your Principal?
  Why or why not?" (This is the Bet-4 / Switzerland-neutral test.)

**Document-native review probe** *(updated 2026-05-03, Robin/Legora/Microsoft
comparable)*: This tests whether Redline needs a Word task pane, high-fidelity DOCX
round-trip, or a browser review loop with Word-compatible output. Adjacent evidence from
legal AI shows that document-native, playbook-driven review matters in high-liability
professional workflows. Graeme's boundary note adds the domain constraint: Redline may
surface flags, citations, comments, tracked changes, and audit evidence, but must not
author engineering judgement or arbitrate reviewer decisions.

- "The last time you handled senior-review comments, where did the real work happen:
   Word comments, tracked changes, PDF markup, a review meeting, email, or a separate
   checklist?"
- "If Redline returned a DOCX with comments, tracked changes, source links, and preserved
   formatting, would that fit your workflow, or would the review need to happen inside
   Word itself?"
- "What would make browser upload unacceptable: confidentiality, formatting risk, version
   control, upload friction, IT policy, or something else?"
- "Which parts of the document must survive perfectly: numbering, tables, figure
   references, comments, tracked changes, headers/footers, appendices, or template styles?"
- "Would you trust a source-linked comment more than a plain suggestion? What source
   would need to be linked: clause reference, firm rule, prior report pattern, or reviewer
   rationale?"

**Generic LLM usage probe** *(added 2026-05-03, John)*: This tests whether Redline is
wrapping an existing drafting behaviour rather than competing with it.

- "What do you already use ChatGPT, Claude, Copilot, or internal prompt libraries for in
   report work?"
- "Before an AI-assisted draft reaches a senior reviewer, what do you still check
   manually?"
- "What would make you trust or reject a source-linked quality flag: the cited source,
   the wording, the Word comment format, the reviewer workflow, or something else?"

**House Rules / starter playbook probe** *(added 2026-05-03, Mark + Graeme)*:

- "Does your firm have review rules that everyone is expected to follow but that are not
   reliably written down?"
- "Who owns those rules today: Technical Director, Project Director, senior reviewer,
   project controller, QA manager, or nobody?"
- "If Redline shipped 20-30 starter rules, which would your firm keep, change, or delete?"
- "How much senior time would your firm spend configuring House Rules before it became
   too much effort?"
- "Would founder-assisted setup feel useful, or would it feel like outsourced engineering
   review?"

**Workflow expansion boundary probe** *(added 2026-05-03, Graeme)*:

- "Where would multi-document consistency matter first: RFP to LOE, LOE to GIR, GIR to
   appendices, GBR to specification, or report bundle to limitations clauses?"
- "Is that a H2 need, or only useful after Pre-Review already works on a single document?"
- "Which review rules are safe to encode as checks, and which should always stay with a
   senior engineer's judgement?"
- "Would a senior reviewer trust Redline more if every flag said 'review required' rather
   than 'fix this'?"

Provenance: `docs/research/20260426-legal-ai-adjacent-market-signal.md`,
`docs/research/20260503-microsoft-word-legal-agent-robin-ai-legora-signal.md`, and
`docs/knowledge/geotechnical/contracts-and-risk/ai-workflow-expansion-boundaries.md`.

**Structural completeness probe** *(added 2026-04-23)*: This question validates
whether intermediate engineers recognise the content-vs-packaging gap in their own
report reviews. If they do, structural completeness rules get high priority in
Pre-Review's initial rule library. If they don't, the rule category may be a
senior-reviewer concern only (still valid, but changes priority).

- "Think about the last time a senior reviewer sent a draft back — was the issue that
  your technical content was wrong, or that it wasn't presented clearly enough? For
  example, did they ask for a decision matrix, a severity classification, or a worked
  example that you hadn't included, even though you knew the answer?"

### Part 5 — Pricing module (Van Westendorp, 2 minutes)

Only at the very end, after the JTBD is mapped. See `pricing-methodology.md` Step 1.

**Note**: Part 5 may be dropped if the conversation runs long, the interviewee lacks
budget authority (e.g. a junior with no purchasing role), or the rapport would be
damaged by shifting to pricing questions. The pricing-methodology gate requires
Van Westendorp completion in >= 10 of 15 KR2 conversations — not all 15. Skipping
Part 5 in a given interview is acceptable; skipping it habitually is not.

Four anchor questions:

- At what monthly price would this be so cheap you'd doubt the quality?
- At what price would you consider it a bargain?
- At what price would you start to think it's expensive but worth considering?
- At what price would it be too expensive to consider?

### Part 6 — Wrap (manage the network) (1 minute)

> "Who else in your firm or your network would be useful for me to talk to about this?"

Compounding referrals is the only way a solo founder hits 15 interviews in 90 days
inside a small geographic niche.

## What Counts as a "Qualified" Conversation (KR2 Definition)

Per `okrs/2026-h2.md`, KR2 requires:

- ≥ 30 minutes (the Switch timeline alone consumes 25);
- Work-email-verified;
- Employed at an NZ or AU geotechnical consultancy;
- Drafted at least one GBR/GIR in the last 12 months.

Add: the conversation must produce a documented Switch timeline and a Four-Forces
map. A 30-minute call that did not surface either is not yet "qualified" — it is
rapport-building, which is fine but does not count toward KR2.

## Earlyvangelist Filter (Blank)

Of the 15, identify how many are *earlyvangelists* — engineers who:

1. Know they have the problem;
2. Are actively looking for a solution;
3. Have built or hacked together a workaround (a personal checklist, a shared spreadsheet,
   a private LLM prompt library);
4. Have or can quickly access budget for a Pro-tier seat.

Earlyvangelists convert to KR3 paid; non-earlyvangelists are intelligence and
referral sources, not buyers. Track the ratio. If 0/15 are earlyvangelists, the
funnel hypothesis is broken even if KR2 hits 15.

## Watering Holes (Where to Find the 15)

Blank's "get out of the building" for a solo NZ/AU founder is not literal door-knocking;
it is finding the digital and physical watering holes where intermediate engineers
naturally congregate:

- NZGS (NZ Geotechnical Society) regional chapter meetings.
- AGS (Australian Geomechanics Society) branch events.
- LinkedIn — direct outreach via the cadence in `gtm/content-engine.md`.
- Founder's existing network — peer lunches with introductions traded for insights.
- Quota-exhausted free-tier users — the highest-intent watering hole there is.

## Velocity Tension (Flagged)

Blank's methodology assumes 10–15 interviews per week. KR2 commits to 15 in 90 days
(roughly 1/week). This is acknowledged as a velocity gap; see `decisions/parked-decisions.md`
P-017. The mitigation is qualification depth: each KR2 conversation must produce a
Switch timeline and Four-Forces map, raising signal-per-interview to compensate for
the low count.

## Provenance

Switch timeline and Four Forces grounded in Christensen / Moesta literature
(`docs/research/` queries against the entrepreneurship-startup-strategy notebook,
2026-04-18). Customer Development posture grounded in Steve Blank, same notebook.
Watering-hole framing is Blank's; specific NZ/AU venue selection is Ron's adaptation.
