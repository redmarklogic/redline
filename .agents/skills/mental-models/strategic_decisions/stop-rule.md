# Stop Rule

## What it is

A Stop Rule is a hard, unconditional, pre-committed boundary that halts deliberation or exploration automatically when a threshold is reached -- preventing endless search, analysis paralysis, or runaway retry loops.

## Core principle

Set a nonnegotiable limit before you start and act on it mechanically when triggered. The cost of over-exploring almost always exceeds the cost of stopping slightly early.

## When to invoke

- Searching for information, files, or solutions and unsure when "enough" is enough
- Retrying a failing approach and need a cutoff to switch strategies
- Exploring alternative implementations and risk going down a rabbit hole
- Any open-ended task where there is no natural termination signal

## How to apply

1. Before starting, define the stop condition -- a count (e.g. "3 search attempts"), a time budget, or a quality threshold
2. Execute the task normally
3. When the stop condition is met, stop immediately -- do not renegotiate the threshold mid-task
4. Summarise what you found, act on the best available option, or escalate

## Anti-patterns

- **Moving the goalposts** -- adjusting the stop threshold because "one more try" feels productive; this defeats the entire purpose
- **No stop rule at all** -- unbounded exploration in agentic workflows leads to wasted context, token bloat, and circular reasoning
- **Overly tight thresholds** -- setting the limit so low that you never gather enough information to act; calibrate the threshold to the stakes of the decision

## Source

*The Decision Book: 50 Models for Strategic Thinking* -- Mikael Krogerus and Roman Tschappeler
