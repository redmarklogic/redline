# Technical Debt and Path Dependence

## What it is

Technical Debt is the accumulated cost of past shortcuts, hacks, and expedient decisions that make future changes slower and riskier. Path Dependence is the broader principle that past decisions constrain future options -- the system partially "remembers" its history.

## Core principle

Every shortcut taken now must be repaid later with interest. Past architectural choices narrow the set of feasible future choices. Balance short-term speed with long-term flexibility by preserving optionality wherever possible.

## When to invoke

- Choosing between a quick fix and a proper solution
- Evaluating whether to refactor before adding new functionality
- Making an architectural decision that will be expensive to reverse
- Assessing why a codebase is slow to change despite simple-sounding requirements

## How to apply

1. Identify the shortcut or expedient choice being proposed
2. Estimate the "interest" -- how much harder will future changes be if this debt is taken on?
3. Decide deliberately -- if the debt is cheap to repay later and the time pressure is real, accept it consciously
4. Record the debt -- document what was deferred and why, so it can be repaid intentionally
5. Preserve optionality -- when two approaches have similar short-term cost, prefer the one that leaves more future options open

## Anti-patterns

- **Unconscious debt** -- taking shortcuts without realising they are debt; the cost accrues silently until the system becomes brittle
- **Never accepting debt** -- insisting on the "perfect" solution every time, even when time pressure is genuine and the debt is cheap; this is over-engineering
- **Ignoring path dependence** -- assuming you can freely reverse past decisions; switching costs are almost always higher than expected

## Source

*Super Thinking: The Big Book of Mental Models* -- Gabriel Weinberg and Lauren McCann
