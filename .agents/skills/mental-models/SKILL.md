---
name: mental-models
description: Use when a structured thinking framework is needed for decision-making, root cause analysis, strategic planning, self-awareness, risk evaluation, or communication.
---

# Mental Models

The single source of truth for reusable thinking frameworks. Other skills reference this skill's files rather than defining models inline - preventing redundant definitions from drifting out of sync. Each entry maps a trigger condition to a model and its reference file.

## Architecture

```
[Other skills]        <-- consumers (e.g. resolving-pr-issues)
        |
[mental-models/]      <-- THIS SKILL (bottom layer, no outbound references)
```

## When to Use

Match the trigger column to the current situation, then load the referenced file.

When writing or updating another skill that needs a mental model, reference a file from this skill rather than embedding the definition inline.

## Quick Reference

| Category | Model | Trigger | File |
|---|---|---|---|
| General Thinking | Circle of Competence | Deciding whether to act independently or defer to an expert | `general_thinking/circle-of-competence.md` |
| General Thinking | Inversion | Stuck on a problem; flip it and ask how to guarantee failure | `general_thinking/inversion.md` |
| General Thinking | Second-Order Thinking | Evaluating downstream ripple effects before committing | `general_thinking/second-order-thinking.md` |
| General Thinking | Probabilistic Thinking | Making decisions under uncertainty using base rates and Bayesian updating | `general_thinking/probabilistic-thinking.md` |
| Root Cause Analysis | Five Whys | Postmortem or recurring failure; trace symptoms back to the structural root cause | `root_cause_analysis/five-whys.md` |
| Strategic Decisions | Reversible vs Irreversible | Calibrating how much deliberation a decision deserves | `strategic_decisions/reversible-vs-irreversible.md` |
| Strategic Decisions | OODA Loop | Rapid adaptation needed in a competitive, fast-changing environment | `strategic_decisions/ooda-loop.md` |
| Self-Awareness | Cognitive Biases | Significant choice with limited info; gut-driven decision in unfamiliar domain | `self_awareness/cognitive-biases.md` |
| Self-Awareness | The Feedback Box | Receiving feedback and need to categorise it by actionability, not emotion | `self_awareness/feedback-box.md` |
| Risk Analysis | Black Swan | Evaluating systemic risk or relying on historical data to guarantee future safety | `risk_analysis/black-swan.md` |
| Communication | Third Story | Conflict resolution; need to de-escalate by adopting a neutral observer's perspective | `communication/third-story.md` |
| General Thinking | First Principles | Pattern-matching fails or entering an unfamiliar domain; decompose to foundational truths | `general_thinking/first-principles.md` |
| General Thinking | Occam's Razor | Choosing between competing solutions; prefer the simplest adequate explanation | `general_thinking/occams-razor.md` |
| General Thinking | Map is Not the Territory | Relying on cached assumptions or stale context; models diverge from observed reality | `general_thinking/map-is-not-the-territory.md` |
| General Thinking | Pareto Principle | Scoping work or allocating effort; identify the 20% that drives 80% of value | `general_thinking/pareto-principle.md` |
| General Thinking | Systems Thinking | Editing shared modules or evaluating ripple effects of a change across a codebase | `general_thinking/systems-thinking.md` |
| Strategic Decisions | Backward Reasoning | Planning multi-step implementations; define the end state and work backward to the current state | `strategic_decisions/backward-reasoning.md` |
| Strategic Decisions | Stop Rule | Open-ended search or retries with no natural termination; set a hard cutoff before starting | `strategic_decisions/stop-rule.md` |
| Strategic Decisions | Eisenhower Matrix | Multiple competing tasks; classify by urgency vs importance to prioritise | `strategic_decisions/eisenhower-matrix.md` |
| Strategic Decisions | Technical Debt | Choosing between a quick fix and a proper solution; balance speed with long-term flexibility | `strategic_decisions/technical-debt.md` |
| Risk Analysis | Precautionary Principle | About to perform a destructive or irreversible operation; require safety proof before proceeding | `risk_analysis/precautionary-principle.md` |
| Risk Analysis | Swiss Cheese Model | Designing layered defences or diagnosing how a failure slipped through quality gates | `risk_analysis/swiss-cheese-model.md` |
| Root Cause Analysis | Cargo Cult | Copying patterns or "best practices" without understanding why they work | `root_cause_analysis/cargo-cult.md` |
| Strategic Decisions | Trade-off Analysis | Choosing between options with competing constraints; explicitly price what you are sacrificing | `strategic_decisions/trade-off-analysis.md` |
| Strategic Decisions | Cannibalisation Dynamics | Evaluating whether a company will commercialise an internal capability, or identifying a market gap created by incumbents who rationally refuse to | `strategic_decisions/cannibalisation-dynamics.md` |
| Strategic Decisions | Pre-mortem | Before committing to a plan; assume it has already failed and work backward to surface hidden risks | `strategic_decisions/pre-mortem.md` |
| Strategic Decisions | RICE | Ranking 5-20 initiatives by total impact per time worked when gut-feel prioritisation is insufficient | `strategic_decisions/rice.md` |
| Strategic Decisions | MoSCoW | After prioritisation, to translate a ranked list into unambiguous release-criteria buckets (Must/Should/Could/Won't) | `strategic_decisions/moscow.md` |
| Strategic Decisions | Value-Effort Matrix | Triaging a backlog visually by relative value versus total delivery cost; escalate to ROI Scorecard for large lists | `strategic_decisions/value-effort.md` |
| Strategic Decisions | Kano Model | Classifying features by tier of customer need (Dissatisfier/Satisfier/Delighter) to guide differentiation investment | `strategic_decisions/kano.md` |
| Self-Awareness | Sunk-Cost Fallacy | Tempted to continue a failing effort because of past investment; evaluate only future returns | `self_awareness/sunk-cost-fallacy.md` |
| Self-Awareness | Dunning-Kruger Effect | Feeling confident in unfamiliar territory, or assessing a junior's skill level before assigning independent work | `self_awareness/dunning-kruger.md` |
| General Thinking | Deep Modules | Evaluating whether an abstraction is worth its interface cost; prefer few, powerful modules | `general_thinking/deep-modules.md` |
| General Thinking | Zero-One-Infinity Rule | Adding a hardcoded limit to a system; any specific number other than 0 or 1 is a design smell | `general_thinking/zero-one-infinity.md` |
| General Thinking | Nielsen's 10 Usability Heuristics | Reviewing a UI design or diagnosing a usability problem without access to user testing | `general_thinking/nielsens-heuristics.md` |
| General Thinking | Thematic Grouping | Organising commits, tasks, or review comments; group by logical theme, not by time or file | `general_thinking/thematic-grouping.md` |

## How to Select a Model

Selection is emergent, not algorithmic. Build breadth across the table; without it you default to the familiar regardless of fit (Maslow's Hammer). When facing a specific case, apply these four steps in order:

1. **Gate - Circle of Competence first.** Are you a Lifer (deep experiential knowledge) or a Stranger in this territory? Strangers default to broad models and defer to genuine experts rather than force precision they don't have.
2. **Categorise by objective.** Are you trying to improve yourself, understand yourself, understand others, or improve others? Each maps to a distinct cluster in the table.
3. **Categorise by interaction type** (adversarial situations only). Is the situation sequential (players take turns)? Use decision/game-tree reasoning. Simultaneous (players act without knowing the other's move)? Use payoff-matrix and equilibrium thinking.
4. **Build indicator knowledge through journaling.** Record which model you chose, how you applied it, and the result. Over time the right model surfaces automatically from pattern recognition rather than deliberate search - you won't always choose correctly early on, and that is expected.

## Common Mistakes

- Picking a model by name recognition rather than matching the trigger condition.
- Applying two conflicting models to the same decision without resolving the tension first.
- Defining a mental model inline in another skill rather than referencing this one - creates redundancy and lets definitions drift out of sync.
- Selecting a model before applying the Circle of Competence gate - operating outside your territory without acknowledging it leads to false precision.
