# Backward Reasoning

## What it is

Backward Reasoning (also called "look forward and reason backward") is the practice of defining the desired end state first, then working backward step by step to determine what must be true at each preceding stage to reach that outcome.

## Core principle

Start from where you want to end up and deduce the chain of preconditions. This reveals the critical path and exposes hidden dependencies that forward planning often misses.

## When to invoke

- Planning multi-step implementations, migrations, or refactors
- Need to identify the minimal set of changes required to reach a target state
- Forward planning produces too many branching possibilities to evaluate
- Designing a test strategy -- start from the desired assertion and work backward to the setup

## How to apply

1. Define the desired end state precisely
2. Ask "what must be true immediately before this state?" and note the precondition
3. Repeat -- for each precondition, ask what must be true before *that*
4. Continue until you reach the current state
5. The resulting chain is your implementation plan in reverse order

## Anti-patterns

- **Vague end state** -- if the goal is fuzzy, backward reasoning produces fuzzy steps; define the target concretely first
- **Ignoring side-effects** -- backward reasoning focuses on the critical path but may miss collateral impacts; combine with systems thinking for complex changes
- **Only reasoning backward** -- some problems benefit from meeting in the middle; use forward and backward reasoning together when the problem space is large

## Source

*The Art of Strategy: A Game Theorist's Guide to Success in Business and Life* -- Avinash K. Dixit and Barry J. Nalebuff
