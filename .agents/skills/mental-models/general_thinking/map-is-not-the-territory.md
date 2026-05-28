# Map is Not the Territory

## What it is

The principle that all models, abstractions, and representations of reality are necessarily incomplete simplifications. The map (your mental model, cached context, type system, documentation) is useful but never identical to the territory (the actual system, data, or runtime behaviour).

## Core principle

Use models as guides but never mistake them for reality. Constantly update your models based on real-world feedback, and always expect the territory to contain details the map omits.

## When to invoke

- Relying on cached assumptions, stale context, or summarised representations
- Making decisions based on documentation, type signatures, or test coverage alone
- A model's predictions diverge from observed behaviour
- Entering a codebase or domain where your mental model is necessarily incomplete

## How to apply

1. Acknowledge what your current "map" is -- the abstraction, summary, or model you are using
2. Identify what it necessarily omits -- edge cases, runtime state, user behaviour, environmental differences
3. Validate against reality -- run the code, check the actual data, test the assumption
4. Update the map when the territory contradicts it, not the other way around

## Anti-patterns

- **Trusting the map over evidence** -- ignoring test failures, runtime errors, or user reports because "the model says it should work"
- **Never building maps** -- the point is not to avoid abstraction but to hold abstractions lightly and update them
- **Confusing high-fidelity maps with the territory** -- even very detailed models (100% test coverage, full type safety) still omit aspects of production reality

## Source

*The Great Mental Models: General Thinking Concepts* (vol. 1) -- Shane Parrish
