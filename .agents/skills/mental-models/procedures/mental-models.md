# Mental Models — Detailed Reference

## How to Select a Model

Selection is emergent, not algorithmic. Build breadth across the table; without it you default to the familiar regardless of fit (Maslow's Hammer). When facing a specific case, apply these four steps in order:

1. **Gate - Circle of Competence first.** Are you a Lifer (deep experiential knowledge) or a Stranger in this territory? Strangers default to broad models and defer to genuine experts rather than force precision they don't have.
2. **Categorise by objective.** Are you trying to improve yourself, understand yourself, understand others, or improve others? Each maps to a distinct cluster in the table.
3. **Categorise by interaction type** (adversarial situations only). Is the situation sequential (players take turns)? Use decision/game-tree reasoning. Simultaneous (players act without knowing the other's move)? Use payoff-matrix and equilibrium thinking.
4. **Build indicator knowledge through journaling.** Record which model you chose, how you applied it, and the result. Over time the right model surfaces automatically from pattern recognition rather than deliberate search - you won't always choose correctly early on, and that is expected.

# Mental Models

The single source of truth for reusable thinking frameworks. Other skills reference this skill's files rather than defining models inline - preventing redundant definitions from drifting out of sync. Each entry maps a trigger condition to a model and its reference file.

## Architecture

```
[Other skills]        <-- consumers (e.g. resolving-pr-issues)
        |
[mental-models/]      <-- THIS SKILL (bottom layer, no outbound references)
```


## Full Model Catalog

| Category | Model | Trigger | File |
|---|---|---|---|
| General Thinking | Circle of Competence | Deciding whether to act independently or defer to an expert | \general_thinking/circle-of-competence.md\ |
| General Thinking | Inversion | Stuck on a problem; flip it and ask how to guarantee failure | \general_thinking/inversion.md\ |
| General Thinking | Second-Order Thinking | Evaluating downstream ripple effects before committing | \general_thinking/second-order-thinking.md\ |
| General Thinking | Probabilistic Thinking | Making decisions under uncertainty using base rates and Bayesian updating | \general_thinking/probabilistic-thinking.md\ |
| General Thinking | First Principles | Pattern-matching fails or entering an unfamiliar domain; decompose to foundational truths | \general_thinking/first-principles.md\ |
| General Thinking | Occam Razor | Choosing between competing solutions; prefer the simplest adequate explanation | \general_thinking/occams-razor.md\ |
| General Thinking | Map is Not the Territory | Relying on cached assumptions or stale context; models diverge from observed reality | \general_thinking/map-is-not-the-territory.md\ |
| General Thinking | Pareto Principle | Scoping work or allocating effort; identify the 20% that drives 80% of value | \general_thinking/pareto-principle.md\ |
| General Thinking | Systems Thinking | Editing shared modules or evaluating ripple effects of a change | \general_thinking/systems-thinking.md\ |
| General Thinking | Deep Modules | Evaluating whether an abstraction is worth its interface cost | \general_thinking/deep-modules.md\ |
| General Thinking | Zero-One-Infinity Rule | Adding a hardcoded limit; any specific number other than 0 or 1 is a design smell | \general_thinking/zero-one-infinity.md\ |
| General Thinking | Nielsen 10 Usability Heuristics | Reviewing a UI design or diagnosing a usability problem | \general_thinking/nielsens-heuristics.md\ |
| General Thinking | Thematic Grouping | Organising commits, tasks, or review comments by logical theme | \general_thinking/thematic-grouping.md\ |
| Root Cause Analysis | Five Whys | Postmortem or recurring failure; trace symptoms back to structural root cause | oot_cause_analysis/five-whys.md\ |
| Root Cause Analysis | Cargo Cult | Copying patterns or best practices without understanding why they work | oot_cause_analysis/cargo-cult.md\ |
| Strategic Decisions | Reversible vs Irreversible | Calibrating how much deliberation a decision deserves | \strategic_decisions/reversible-vs-irreversible.md\ |
| Strategic Decisions | OODA Loop | Rapid adaptation in a competitive, fast-changing environment | \strategic_decisions/ooda-loop.md\ |
| Strategic Decisions | Backward Reasoning | Planning multi-step implementations; define end state and work backward | \strategic_decisions/backward-reasoning.md\ |
| Strategic Decisions | Stop Rule | Open-ended search or retries with no natural termination; set a hard cutoff | \strategic_decisions/stop-rule.md\ |
| Strategic Decisions | Eisenhower Matrix | Multiple competing tasks; classify by urgency vs importance | \strategic_decisions/eisenhower-matrix.md\ |
| Strategic Decisions | Technical Debt | Choosing between a quick fix and a proper solution | \strategic_decisions/technical-debt.md\ |
| Strategic Decisions | Trade-off Analysis | Choosing between options with competing constraints; explicitly price the sacrifice | \strategic_decisions/trade-off-analysis.md\ |
| Strategic Decisions | Cannibalisation Dynamics | Evaluating whether a company will commercialise an internal capability | \strategic_decisions/cannibalisation-dynamics.md\ |
| Strategic Decisions | Pre-mortem | Before committing to a plan; assume it failed and surface hidden risks | \strategic_decisions/pre-mortem.md\ |
| Strategic Decisions | RICE | Ranking 5-20 initiatives by total impact per time worked | \strategic_decisions/rice.md\ |
| Strategic Decisions | MoSCoW | Translating a ranked list into release-criteria buckets | \strategic_decisions/moscow.md\ |
| Strategic Decisions | Value-Effort Matrix | Triaging a backlog visually by relative value versus delivery cost | \strategic_decisions/value-effort.md\ |
| Strategic Decisions | Kano Model | Classifying features by tier of customer need | \strategic_decisions/kano.md\ |
| Self-Awareness | Cognitive Biases | Significant choice with limited info; gut-driven decision in unfamiliar domain | \self_awareness/cognitive-biases.md\ |
| Self-Awareness | Feedback Box | Receiving feedback; categorise by actionability, not emotion | \self_awareness/feedback-box.md\ |
| Self-Awareness | Sunk-Cost Fallacy | Tempted to continue a failing effort because of past investment | \self_awareness/sunk-cost-fallacy.md\ |
| Self-Awareness | Dunning-Kruger Effect | Feeling confident in unfamiliar territory | \self_awareness/dunning-kruger.md\ |
| Risk Analysis | Black Swan | Evaluating systemic risk or relying on historical data to guarantee future safety | isk_analysis/black-swan.md\ |
| Risk Analysis | Precautionary Principle | About to perform a destructive or irreversible operation | isk_analysis/precautionary-principle.md\ |
| Risk Analysis | Swiss Cheese Model | Designing layered defences or diagnosing how a failure slipped through | isk_analysis/swiss-cheese-model.md\ |
| Communication | Third Story | Conflict resolution; de-escalate by adopting a neutral observer perspective | \communication/third-story.md\ |
