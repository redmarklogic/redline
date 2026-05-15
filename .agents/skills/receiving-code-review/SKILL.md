---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Code Review Reception

## Boundary Contract

### Inputs
- Code review feedback (comments, suggestions, requested changes)

### Outputs
- Addressed review comments with verified fixes

### Out of Scope
- Requesting review (`requesting-code-review`)
- Code implementation or feature work
- Debugging (`systematic-debugging`)

## Step 0 — CI Gate (hard stop before anything else)

**STOP. Do not read review threads. Do not implement any fix. Do not resolve any thread.**

Run `procedures/pre-flight.md` now. This is a hard numbered gate, not a suggestion.

The pre-flight procedure:
1. Gates on CI/CD — polls every minute, up to 10 minutes; fixes PR-owned failures before proceeding
2. Escalates to your human partner if checks are still running at timeout or if failures are pre-existing
3. Triages all threads by severity (CI/CD → security → architectural conflicts → correctness → nits)
4. Applies reviewer trust level before acting on each comment

**The gate applies even when:**
- All threads are documentation edits ("doc-only" changes fail codespell, custom hooks, and link checks)
- All threads look trivially simple ("simple" threads can mask CI failures caused by the PR)
- CI failures appear pre-existing (still escalate — do not self-decide to ignore)
- The user said "quickly", "just nits", or similar (time pressure is not an exception)

## Procedures

| File | Purpose |
|---|---|
| `procedures/pre-flight.md` | CI/CD gate, severity triage, reviewer trust assignment |

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

**Step 0 runs first, always.** See [Step 0 — CI Gate](#step-0--ci-gate-hard-stop-before-anything-else) above.

```
WHEN receiving code review feedback:

0. CI GATE: procedures/pre-flight.md — STOP here until CI passes or escalated
1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (explicit CLAUDE.md violation)
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

## Common Mistakes

**Skipping the CI gate because threads look doc-only or simple**

This is the most common rationalization. Documentation PRs fail CI for exactly the reasons
that make them seem safe: codespell, custom hooks, and link checks all run on Markdown files.
"No code changed" does not mean "CI will pass."

Rationalizations that are not exceptions:
- "The threads are just text edits."
- "These are nits / cosmetic fixes."
- "The changes are documentation-only."
- "I'll check CI after fixing the threads."
- "The CI failure looks pre-existing."

All of the above require Step 0 to be completed before any thread is touched.

**Treating "pre-existing" failures as someone else's problem**

If CI is failing and the failure looks pre-existing, escalate to your human partner.
Do not self-decide to proceed. The pre-existing classification might be wrong.

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Source-Specific Handling

### From your human partner
- **Trusted** - implement after understanding
- **Still ask** if scope unclear
- **No performative agreement**
- **Skip to action** or technical acknowledgment

### From External Reviewers
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**your human partner's rule:** "External feedback - be skeptical, but check carefully"

## YAGNI Check for "Professional" Features

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**your human partner's rule:** "You and reviewer both report to me. If we don't need this feature, don't add it."

## Implementation Order

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with your human partner's architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Involve your human partner if architectural

**Signal if uncomfortable pushing back out loud:** "Strange things are afoot at the Circle K"

## Acknowledging Correct Feedback

When feedback IS correct:
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**Why no thanks:** Actions speak. Just fix it. The code itself shows you heard the feedback.

## Handling Irrelevant Comments

When a comment is not actionable (wrong tech stack, out of scope, preference with no technical merit):

```
NEVER: Silently resolve the thread
NEVER: "Thanks for the feedback — resolving this."
NEVER: ANY gratitude expression before resolving

ALWAYS:
  1. POST a reply stating exactly why this comment does not apply
  2. THEN resolve the thread
```

The reply must be specific — reference the concrete reason (architectural decision, wrong stack, out of PR scope). A vague "this isn't relevant" is not enough.

```
✅ "Python is this project's documented language choice — not in scope for a PR review.
    Resolving. Architectural discussions belong outside the PR."
✅ "This file is intentionally read-only in this context; the pattern you're describing
    applies to a different layer. Resolving — no change needed."

❌ "Thanks for the feedback, but this isn't relevant."
❌ [resolve with no reply]
❌ "Resolving — not applicable."  ← too vague, no stated reason
```

**If you catch yourself about to write "Thanks":** DELETE IT. State the fix instead.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

State the correction factually and move on.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## Real Examples

**Performative Agreement (Bad):**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**Technical Verification (Good):**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**YAGNI (Good):**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**Unclear Item (Good):**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## GitHub Thread Replies

When replying to inline review comments on GitHub, reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implement.

No performative agreement. Technical rigor always.
