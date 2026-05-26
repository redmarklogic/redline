# ADR-011: Hook-first Enforcement

## Summary

For every project rule that can be expressed as a deterministic pattern check, a pre-commit
hook is the required enforcement mechanism. An instruction in `AGENTS.md` or a skill
document alone is insufficient for architectural invariants (accepted 2026-05-26). The hard
constraint: an invariant is not enforced until a hook enforces it. Instructions and hooks are
complementary — instructions guide the generation phase; hooks guarantee the committed
artifact complies.

**Status**: Accepted
**Date**: 2026-05-26
**Deciders**: Peter (architecture), Kabilan (engineering)

---

## Decision

For every project rule that can be expressed as a deterministic pattern check, a pre-commit
hook is the required enforcement mechanism. An instruction in `AGENTS.md` or a skill
document alone is insufficient for architectural invariants.

---

## Context

This project uses `AGENTS.md`, `.github/instructions/*.instructions.md`, and skill files
under `.agents/skills/` to communicate rules to the AI agent during code generation. These
mechanisms are probabilistic: the agent reads them, reasons about them, and attempts to
comply. Under deadline pressure, context-window limits, or ambiguous prompts, the agent may
not apply the rule. The rule is then violated silently and only surfaces during human code
review.

Pre-commit hooks (Python scripts under `hooks/`, wired into `.pre-commit-config.yaml`) are
deterministic. A hook either passes or blocks the commit. The agent's reasoning is
irrelevant.

Over time the project accumulated a body of hooks alongside corresponding instructions. The
relationship between the two layers was implicit. This ADR makes it explicit.

Note: "hooks" in this ADR refers exclusively to pre-commit checks under `hooks/`. Any future
agent lifecycle hooks system would be a separate concern and should be addressed in its own
ADR.

---

## Principles

### P1 — Prefer hook over instruction when the rule is checkable

If a rule can be expressed as a regex, file-scan, or AST check, it should have a pre-commit
hook. An instruction in `AGENTS.md` or a skill document is a complement, not a substitute.

Rationale: instructions target the generation phase (what the agent writes); hooks target the
artifact phase (what enters the repository). A rule enforced only by instruction is a polite
request.

### P2 — Layered defence for architectural invariants

For high-stakes constraints — Single Source of Truth violations, dependency-direction rules,
domain model constraints — use both an instruction and a hook. The instruction helps the
agent avoid the violation during generation. The hook is the safety net.

Lower-stakes style preferences (line length, naming conventions) may rely on a linter or
formatter alone; a custom hook is not required.

### P3 — Instructions for intent; hooks for invariants

Instructions explain why a rule exists and shape agent reasoning. They belong in `AGENTS.md`
or skills when the "why" matters for generation quality. Hooks enforce that the committed
artifact complies. These are complementary roles, not competing ones.

### P4 — Hook bodies must be generic; project-specific values live in configuration

Hook scripts must not contain project-specific literals: names, file paths, team-member
names, or domain values. Project-specific values are passed as CLI args declared in
`.pre-commit-config.yaml`. This prevents the hook from becoming an SSOT violation and makes
it reusable across projects.

This principle is enforced deterministically by `check-banned-words.py`, which scans all
hook scripts for forbidden project-specific terms provided via CLI args.

### P5 — Inline suppression over central allowlists

When a legitimate exception to a hook rule exists, suppress it at the point of use with a
magic comment (`# ssot: allow`, `<!-- ssot: allow -->`). Central exception lists in
configuration are forbidden. The exception must be visible at the line it applies to and
reviewable in the diff.

### P6 — Every hook is self-documenting executable documentation

Every hook script that enforces a principle with a corresponding ADR must:

1. Include a module docstring stating the rule being enforced and the reason.
2. Reference the governing ADR by number (e.g. `See ADR-001`).
3. Emit the ADR reference in its error message so the developer has a direct link to the
   decision rationale.

Hooks that enforce purely technical constraints without a governing ADR (e.g. malformed YAML
detection, stale file warnings) are exempt from the ADR-reference requirement, but must still
carry a docstring explaining the rule.

### P7 — Catch at commit, not at review

Rules that can be automated must be caught at `pre-commit`. Human code review is not an
acceptable substitute for a hook that could exist. The cost of fixing a violation is lowest
at commit time.

### P8 — Dependency-direction rules are architectural invariants

Rules of the form "X must not reference Y" (skills must not reference agent names; hooks must
not contain project-specific literals) are dependency-direction invariants. They must be
enforced by hooks, not just stated in instructions, because direction violations accumulate
silently and are the hardest class of architectural erosion to recover from.

---

## Options Considered

- **Option A — Instructions only.** Accept that agent-expressed rules are probabilistic.
  Rejected: violations accumulate silently; the only detection point is human review, which
  is unreliable under deadline pressure.

- **Option B — Hooks only, no instructions.** Remove instructions and rely entirely on hooks.
  Rejected: instructions guide the generation phase. An agent that has never been told the
  rule will violate it on every attempt and learn only at commit time. The loop is: generate
  → commit → fail → fix → commit → pass. Instructions shorten this to: generate (guided) →
  commit → pass. Removing instructions makes hooks noisier.

- **Option C — Layered: instruction for intent, hook for invariant (chosen).** The instruction
  targets generation quality; the hook guarantees repository integrity. Both are required for
  invariants; hooks alone are sufficient for purely technical constraints that the agent does
  not need to reason about.

---

## Decision Rationale

Option C acknowledges that the agent and the hook enforce the same rule at different phases
with different failure modes. Instructions are cheapest to write and reduce generation-time
noise. Hooks are the only reliable enforcement gate. Neither alone is sufficient for
architectural invariants.

---

## Consequences

- Every new architectural rule added to `AGENTS.md` or a skill must be accompanied by a hook
  if the rule is pattern-checkable. The PR description should explain why a hook was not
  added if one was omitted.

- New hooks enforcing decisions documented in ADRs must reference the ADR in their docstring
  and in their error output.

- `check-banned-words.py` enforces P4 for all hooks in the `hooks/` directory. It must
  reference this ADR (ADR-011) in its docstring per P6.

- Existing hooks that enforce ADR-backed rules but lack docstring ADR references are in
  violation of P6 and should be updated incrementally.

---

## References

- [ADR-001](adr-001-single-source-of-truth.md) — Single Source of Truth (SSOT violations are
  a primary target for hook enforcement; P2, P5 examples)
- [ADR-010](adr-010-dependency-inversion-principle-for-skills-agents-boundary.md) — Dependency
  Inversion Principle for Skills/Agents Boundary (P8 example: skills must not reference agent
  names)
