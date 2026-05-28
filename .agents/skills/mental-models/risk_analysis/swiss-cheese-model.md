# Swiss Cheese Model

## What it is

The Swiss Cheese Model visualises a system's defences as multiple layers (slices of cheese), each with shifting vulnerabilities (holes). A catastrophic failure occurs only when the holes in every layer happen to align, allowing a hazard to pass through all defences simultaneously.

## Core principle

No single defence layer is perfect. Systemic failures require multiple independent safeguards to fail at the same time. Robust systems stack diverse, overlapping defences so that a hole in one layer is caught by the next.

## When to invoke

- Designing error handling, validation, or safety layers in code
- Reviewing CI/CD pipelines, pre-commit hooks, or quality gates
- Conducting a postmortem to understand how a failure slipped through
- Evaluating whether a "belt and suspenders" approach is warranted for a critical path

## How to apply

1. Identify the defensive layers in your system (type checking, unit tests, integration tests, code review, pre-commit hooks, monitoring, alerting)
2. For each layer, identify the known holes -- what classes of error does it miss?
3. Check for alignment -- are there failure modes that pass through all layers undetected?
4. Add or strengthen layers specifically where alignment gaps exist
5. Diversify the types of defence -- layers that use the same detection method share the same blind spots

## Anti-patterns

- **Single layer reliance** -- trusting one defence (e.g. only unit tests, only type checking) and assuming it catches everything
- **Identical layers** -- adding more layers of the same kind does not reduce alignment risk; diversity matters
- **Ignoring layer degradation** -- defences rot over time (skipped tests, disabled hooks, stale alerts); holes grow silently

## Source

*Super Thinking: The Big Book of Mental Models* -- Gabriel Weinberg and Lauren McCann; James Reason's accident causation model
