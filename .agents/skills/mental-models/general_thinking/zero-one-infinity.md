# Zero-One-Infinity Rule

## What it is

The Zero-One-Infinity (ZOI) rule is a design principle stating that a system should permit zero instances of a thing, exactly one instance, or any number of instances. Any other specific limit -- two, five, 256 -- is an arbitrary magic number that constrains users without principled justification.

## Core principle

Arbitrary fixed limits are a design smell. A constraint should either be absolute (zero: forbidden; one: singular) or unlimited (infinity: unrestricted). Any specific number in between is almost always the designer's current convenience masquerading as a system boundary.

## When to invoke

- Deciding how many of something a system should allow (connections, retries, parents, arguments, tabs)
- Reviewing code that contains a hardcoded limit such as `MAX_ITEMS = 3` or `if len(args) > 2`
- Designing an API that accepts a single value where a list would be more honest
- Evaluating whether a "two of these" assumption will survive future requirements

## How to apply

1. Identify the limit being proposed or enforced
2. Ask: is this a principled absolute constraint (zero or one), or just "more than one feels messy right now"?
3. If it is not zero or one, default to allowing N and let external factors (storage, rate limits, validation rules) impose the real ceiling
4. Encode real external ceilings explicitly and visibly -- not as hidden magic numbers buried in business logic
5. Use type systems and data structures (list vs optional) to make zero/one/many intent visible at the interface boundary

## Anti-patterns

- **Magic-number limits** -- `MAX_RETRIES = 3`, `MAX_PARENTS = 2` copy-pasted indefinitely without the author ever questioning the value; these invariably break when a new use case emerges
- **Premature singularity** -- designing a system that only works with one instance because that is all that was needed today; this forces a painful rewrite when the second instance appears
- **Infinity without guard rails** -- removing a cap without providing any resource-based ceiling, causing unbounded growth to exhaust memory or connections in production

## Source

*Zero-One-Infinity Rule* -- attributed to Willem van der Poel (1960s); independently formulated by Bruce MacLennan in *Principles of Programming Languages* (1983)
