---
id: P-038
type: question
date_deferred: 2026-05-31
status: open
deferred_by: peter
owner_at_retrieval: "Peter re-evaluates; founder decides"
unfreeze_condition: >-
  Founder has activated Claude Code subscription (on or after 2026-06-02)
revisit_by: 2026-06-02
artifact_ref: "docs/research/framework-analysis-superpowers-speckit.md"
---

# cc-spex Adoption Decision

## Why deferred

Evaluated cc-spex (a Claude Code plugin combining SpecKit + Superpowers with quality gates,
deep review, worktree isolation, and collaborative PR workflows) as a candidate to replace
or supplement our current custom SpecKit extension design. Current recommendation is **do not
adopt** due to platform mismatch (cc-spex requires Claude Code; we run VS Code + Copilot) and
loss of our domain-specific agent topology (shaping gate, source reconciliation, constitution
governance). Decision parked pending migration to Claude subscription.

## Unfreeze condition

Founder has activated a Claude Code subscription (target: 2026-06-02). At that point,
re-evaluate whether the platform mismatch blocker is lifted and whether selective adoption of
cc-spex extensions (spex-gates, spex-deep-review, spex-worktrees) is worthwhile alongside
our existing custom extensions, or whether a parallel Claude Code workflow is viable.

## Owner at retrieval

Peter re-evaluates the platform mismatch against the active Claude Code runtime. Founder
makes the final adopt/reject call.
