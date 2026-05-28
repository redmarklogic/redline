# Systems Thinking

## What it is

Systems Thinking is the practice of analysing an entire system holistically to understand the interlocking dependencies, feedback loops, and emergent behaviours that arise from the interaction of its parts -- rather than analysing components in isolation.

## Core principle

Changing one variable ripples through the whole system. You cannot understand or safely modify a component without understanding how it connects to everything else.

## When to invoke

- Editing shared modules, utilities, or domain models that multiple consumers depend on
- Evaluating the side-effects of a proposed change across a codebase
- Debugging emergent behaviour that no single component explains
- Planning a refactor that touches cross-cutting concerns

## How to apply

1. Map the system -- identify the key components and the connections (data flow, dependencies, event chains) between them
2. Identify feedback loops -- reinforcing loops (snowball effects) and balancing loops (self-correcting mechanisms)
3. Trace the proposed change through the map -- follow every connection to predict ripple effects
4. Look for unintended consequences -- especially in balancing loops that may counteract your change
5. Validate by testing the actual system, not just the changed component

## Anti-patterns

- **Reductionism** -- analysing a component in isolation and assuming the system will behave accordingly
- **Ignoring feedback loops** -- making a change that triggers a reinforcing loop you did not anticipate (e.g. a performance fix that increases load, which degrades performance elsewhere)
- **Analysis paralysis** -- mapping the entire universe of connections when only the immediate neighbourhood matters for the change at hand

## Source

*The Art of Thinking in Systems* and *The Great Mental Models Volume 3: Systems and Mathematics* -- Shane Parrish
