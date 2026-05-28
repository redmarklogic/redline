# Pareto Principle (80/20 Rule)

## What it is

The observation that roughly 80% of outcomes come from 20% of inputs. In practice, a small fraction of effort, code, tests, or features produces the majority of value.

## Core principle

Identify the high-leverage minority and focus resources there. Do not spread effort uniformly when returns are heavily skewed.

## When to invoke

- Scoping work and need to decide what to build first
- Choosing which tests to write, which bugs to fix, or which files to review
- Optimising performance -- most slowness lives in a small fraction of the code
- Time-constrained and need maximum impact from limited effort

## How to apply

1. List the possible actions, features, or areas of focus
2. Estimate the relative impact of each (even roughly)
3. Rank by impact and identify the top 20% that drive 80% of the value
4. Allocate the majority of effort to those high-leverage items
5. Defer, simplify, or skip the long tail unless explicitly required

## Anti-patterns

- **Perfectionism on the tail** -- spending equal effort on the low-value 80% destroys the efficiency the principle offers
- **Ignoring the tail entirely** -- the remaining 20% of value still matters; the principle guides *sequencing*, not *abandonment*
- **Assuming the ratio is exact** -- 80/20 is a heuristic; the actual split varies but the skew is real

## Source

*The Art of Thinking in Systems* and *Super Thinking: The Big Book of Mental Models* -- Gabriel Weinberg and Lauren McCann
