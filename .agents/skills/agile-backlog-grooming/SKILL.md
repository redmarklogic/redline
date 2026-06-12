---
name: agile-backlog-grooming
description: Use when the user asks to groom the backlog, run a backlog audit, run a grooming pass, or declutter the GitHub Projects board. Audits every backlog item against completed work, ADRs, bets, and docs; produces a per-row decision table; executes only user-approved rows. PM-owned, user-gated, on-demand only.
---

# Backlog Grooming — Founder-Gated Board Audit

Operationalises `docs/product/operations/backlog-cultivation-principles.md`.
Full design rationale: `docs/product/operations/backlog-grooming-skill-design.md`.
Read both before the first pass in a session.

**Owner:** Mark (steward). <!-- hook: allow --> **Decision-maker:** user, per row, verbally in session.
**Trigger:** on-demand only — user-initiated ("groom the backlog", "backlog audit",
"run a grooming pass", "declutter the board"). Never self-scheduled, never run as a
side effect of another skill.

**What this is not.** Not sprint planning (`agile-sprint-planning`), not task
creation (`github-projects`), not strategy review (Ron). <!-- hook: allow --> Grooming decides the
*existence and structure* of items, not their rank order.

---

## Founder-ratified conventions (2026-06-12)

| Convention | Ratified value |
|---|---|
| Cadence | **On-demand only.** User triggers; no calendar entry. |
| Drop semantics | **Delete the issue** (`gh issue delete`), not close. See Drop protocol below — irreversible, so archive-before-delete is mandatory. |
| Approval interface | **Verbal per row in session.** Mark walks the table row by row; user says approve / reject / modify; Mark records each verdict into the USER DECISION column immediately. The report file is the durable audit trail. | <!-- hook: allow -->
| Staleness flag | Untouched ≥ **2 sprints** AND no active-bet link → flag for review (C7). Signal, not verdict. |
| Report home | `docs/product/operations/backlog-grooming/YYYY-MM-DD-grooming-report.md` |
| Defer routing | Valid-but-no-active-bet ideas route to `docs/deferred/` P-NNN via `task-defer` — they do not live on the board. |
| First pass | One-off double budget: 90 min / 160 items. Subsequent passes: standard budget. |

## Preflight guards (abort with a clear error if any fails)

- **G1** `gh auth status` shows `project` scope (same guard as `github-projects`).
- **G2** `project_config.json` fresh (≤ 24 h).
- **G3** `docs/product/strategy/strategic-bets.md` has ≥ 1 active bet. Without a live
  strategy there is no alignment test — escalate to Ron instead of grooming. <!-- hook: allow -->
- **G4** Not mid-sprint-planning. Never run concurrently with `agile-sprint-planning`
  (both mutate the same board fields).
- **G5 Stop Rule (pre-committed):** declare the pass budget before Phase A —
  **45 minutes / 80 items**, whichever first (90/160 for pass #1 only). Unprocessed
  items go verbatim into the report's "Not yet reviewed" appendix and lead the next
  pass. The budget is not renegotiated mid-pass.

## Inputs

| Input | Source |
|---|---|
| All board items (every status) | `github-projects` → `list_tasks(config)` |
| Closed issues incl. close reasons | `gh issue list --state closed` |
| Active bets, revisions, kills | `docs/product/strategy/strategic-bets.md` |
| OKRs | `docs/product/strategy/okrs/` |
| Accepted ADRs | `docs/adr/` |
| Strategy decision logs | `docs/product/strategy/decisions/`, `parked-decisions.md` |
| Deferred register | `docs/deferred/_index.md` |
| Open and shipped specs | `specs/NNN-*/`, `specs/shaped/` |
| Roadmap and non-goals | `docs/product/strategy/roadmap.md`, `non-goals.md` |
| Prior grooming reports | `docs/product/operations/backlog-grooming/` — never re-litigate founder-rejected rows |
| CCE session decisions | `session_recall` / `context_search` |
| Current sprint plan | `docs/product/tasks/` — current-sprint items are out of scope |

CCE-first where available; beyond that, evidence comes from the named files above —
do not free-range the repo.

## Workflow

### Phase A — Snapshot

1. `list_tasks(config)` → write full board state to
   `.agents/tmp/backlog-grooming-YYYY-MM-DD/board-snapshot.json`. Analyse the
   snapshot only; live items are re-verified at execution (Phase G step 0).
2. Audit population: status `Backlog`, plus any open item with no sprint or a past
   sprint. Excluded: `Done`, `In Progress`, `To Review`, current-sprint items.
3. Record headline metrics (total, by status, sprint-less count).

### Phase B — Evidence assembly

Three founder-auditable indexes in the tmp folder — every non-keep recommendation
must cite at least one entry:

- `completed-work.md` — Done items + merged-PR titles since last pass (grounds:
  "redundant — already done").
- `direction-changes.md` — accepted ADRs, bet revisions/kills, decision-log entries,
  new non-goals (grounds: "invalidated — direction changed").
- `doc-landscape.md` — open specs, shaped pitches, relevant P-NNN entries (grounds:
  "duplicates an artifact" / "belongs in deferred").

### Phase C — Per-item classification (fixed order)

| Step | Test | Fails → recommendation |
|---|---|---|
| C1 Redundancy | Outcome already delivered by Done task / merged PR / shipped spec? | **drop** |
| C2 Invalidation | Accepted ADR, bet change, or non-goal contradicts the premise? | **drop** (premise dead) or **update** (body stale) |
| C3 Alignment | Links to an active bet, or named dependency of a bet-linked item? | **defer** → P-NNN with unfreeze condition, or **drop** (no plausible trigger) |
| C4 Duplication | Another open item or P-NNN covers the same outcome? | **merge** → better-specified survivor |
| C5 Structure | Structuring Doctrine (`github-projects`) says it belongs under a parent / shards should fold in? | **re-parent** → #Y, or **merge** |
| C6 Size | Won't fit one sprint? | **split** (flag to shaping; not executed in grooming) |
| C7 Hygiene | Missing purpose / done_when / bet ref, or stale (≥ 2 sprints untouched, no bet link)? | **update** |
| Pass all | — | **keep** (one-line reaffirmation) |

Confidence per row: `high` (direct documentary evidence) / `medium` (inference) /
`low` (needs a judgment Mark cannot make). <!-- hook: allow --> **Chesterton's fence:** if you cannot
state why the item exists, the first-pass recommendation is never drop — it is
update-with-a-question, or it goes to consultation. Deletion is irreversible here,
so this rule is strict: **no drop row ships with confidence below high.**

### Phase D — Consultation (low-confidence rows only, dispatch-table-compliant)

One batched dispatch per agent per pass, embedding row context, asking WHAT not HOW:

- **Peter** (feasibility route): "Does ADR-NNN / shipped architecture make #N <!-- hook: allow -->
  redundant or obsolete?" — includes infra/DevOps items (Mark → Brent is not a route). <!-- hook: allow -->
- **Graeme** (domain route, blocking): "Is the domain premise of #N still correct?" <!-- hook: allow -->
- **Ron** (strategy escalation): only when bet linkage is genuinely ambiguous. <!-- hook: allow -->

Never Kabilan (hard rule); no route to Matt/John/Brent/Harriet for grooming. If no <!-- hook: allow -->
permitted route can answer, the row ships marked `low` with the open question stated
— never invent a verdict.

### Phase E — Decision-table report

Write to `docs/product/operations/backlog-grooming/YYYY-MM-DD-grooming-report.md`:

```markdown
# Backlog Grooming Report — YYYY-MM-DD
**Status**: AWAITING FOUNDER REVIEW  (→ APPROVED-PARTIAL / EXECUTED)
**Snapshot**: N total · N backlog · N sprint-less   **Budget used**: Nm / N items

| # | Issue | Title | Age/last-touch | Recommendation | Rationale (1–3 sentences) | Evidence | Consulted | Confidence | USER DECISION |

## Not yet reviewed (stop-rule remainder)
## Archived content of deleted issues   ← filled at execution time
## Open questions for the founder
```

Schema rules: Recommendation ∈ {keep, update, drop, merge → #X, re-parent → #Y,
defer → P-NNN, split}. Merge rows name the survivor and the unique content to
preserve. Defer rows state a candidate unfreeze condition (`task-defer` rejects
deferrals without one). Every non-keep row cites ≥ 1 evidence artifact. FOUNDER
DECISION is empty at handover.

### Phase F — Approval (hard gate, verbal per row)

1. Present a 5-line summary: counts per recommendation type, least-confident rows,
   total proposed board reduction.
2. Walk the table row by row in session. Founder answers `approve` / `reject`
   (+ optional note — recorded so future passes don't re-litigate) / `modify:`
   (replacement action, recorded verbatim). Record each verdict into the FOUNDER
   DECISION column as it is given.
3. Partial approval is the expected case. No default-approval, no silence-as-consent,
   no inferred "approve all". Unreviewed rows stay untouched.

### Phase G — Execution (approved rows only)

**Step 0, every row:** re-fetch the live item. If it changed since the snapshot
(status, sprint, body), skip it, mark `stale — re-audit next pass`, continue.

| Action | Mechanics |
|---|---|
| **drop** | Drop protocol below — archive, reference-check, then delete. |
| **merge → #X** | Fold unique content into #X's body; cross-link comment on #X naming the absorbed issue; then run the Drop protocol on the duplicate. |
| **re-parent → #Y** | `set-parent` procedure from `github-projects` (native sub-issues). |
| **update** | `update-task` + `gh issue edit` (GitHub keeps body edit history). |
| **defer → P-NNN** | Run `task-defer` (creates the P-NNN file + index row with the approved unfreeze condition); then run the Drop protocol on the board item, with the P-NNN path recorded in the report row. |
| **split** | Not executed in grooming — flagged to next sprint-planning/shaping. |
| **keep** | No-op beyond the report row. |

Failures are logged per row and never retried destructively; a failed row reverts to
`pending` for the next pass.

#### Drop protocol (deletion is irreversible — every step is mandatory, in order)

⚠️ `gh issue delete` permanently destroys the issue: number, body, comments, and
history are unrecoverable, and the number is never reused. This is a one-way door.

1. **Archive:** `gh issue view <n> --json number,title,body,labels,comments,createdAt,closedAt`
   → append full content to the report's "Archived content of deleted issues"
   appendix. The report is committed, so the content survives on disk.
2. **Reference check:** search `docs/`, `specs/`, and open issue bodies for `#<n>`.
   Any hit → do NOT delete; surface to the founder in-session and downgrade the row
   to `close` or `skip` per founder's call. A deleted number turns every existing
   `#<n>` reference into a dangling link.
3. **Delete:** `gh issue delete <n> --yes`. Requires admin permission on the repo —
   if the call fails on permissions, fall back to
   `gh issue close <n> --reason "not planned"` + board archive, and note the
   fallback in the report row.

### Phase H — Close-out

1. Report status → `EXECUTED`; append execution log (per-row result) and
   after-metrics (board size before/after, count per action).
2. Persist the pass decision summary to CCE (`record_decision`) so other agents
   inherit what was dropped and why.
3. Commit report + doc changes **on a branch** (`rtk git switch -c chore/backlog-grooming-YYYY-MM-DD`)
   — never to master; founder merges.

## Safety rails

- Founder approval is per-row, verbal, explicit. No autonomous destructive path.
- Deletion only ever follows archive + reference-check; any reference hit blocks it.
- Drop recommendations require `high` confidence — lower confidence becomes
  update/consult.
- Done / In Progress / To Review / current-sprint items are never in scope.
- Stop Rule keeps grooming from becoming the waste it removes.
- Snapshot + re-verify prevents acting on stale state.
- Consultations stay strictly inside Mark's approved dispatch rows; never Kabilan. <!-- hook: allow -->

## Success criteria

1. Open Backlog count falls, then stabilises at a founder-readable size (~10 min read).
2. Sprint planning Steps 2–4 measurably faster.
3. Zero regret events: no deleted item has to be recreated because the rationale was
   wrong (recreation due to genuine direction change is the system working).
4. Every non-keep row spot-checkable against the evidence indexes.
