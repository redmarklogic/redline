# Occam's Razor

## What it is

Occam's Razor is the principle that among competing explanations or solutions, the one with the fewest assumptions and moving parts is most likely correct. Named after the medieval philosopher William of Ockham.

## Core principle

Do not multiply entities beyond necessity. Simpler explanations are more testable, more maintainable, and less likely to contain hidden errors.

## When to invoke

- Choosing between competing solutions that explain the same behaviour
- Reviewing code and deciding whether added complexity is justified
- Diagnosing a bug where multiple hypotheses exist
- Evaluating whether a refactor adds genuine value or just moves complexity around

## How to apply

1. List the candidate explanations or solutions
2. Count the assumptions and moving parts each one requires
3. Prefer the simplest one that adequately explains the observed facts
4. Only add complexity when the simpler option demonstrably fails to account for the evidence

## Anti-patterns

- **Confusing simple with simplistic** -- the razor selects the simplest *adequate* explanation, not an oversimplification that ignores real evidence
- **Using it to dismiss complexity** -- some problems genuinely require complex solutions; the razor says do not add complexity *without evidence*, not to avoid it entirely
- **Over-engineering first, then razoring** -- better to start simple and add complexity only when forced by evidence

## Source

*The Great Mental Models: General Thinking Concepts* (vol. 1) -- Shane Parrish
