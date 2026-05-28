# Precautionary Principle

## What it is

The Precautionary Principle states that when an action could cause harm of unknown or catastrophic magnitude, the burden of proof falls on demonstrating safety before proceeding -- not on demonstrating harm after the fact.

## Core principle

First, do no harm. When the downside is irreversible or unbounded, proceed with extreme caution regardless of how unlikely the risk appears.

## When to invoke

- About to perform a destructive or irreversible operation (delete, drop, force-push, overwrite)
- Operating on production systems, shared infrastructure, or data that cannot be recovered
- The blast radius of a mistake is unclear or potentially unbounded
- Pairs with Reversible vs Irreversible to gate high-consequence actions

## How to apply

1. Identify whether the action is reversible or irreversible
2. If irreversible, assess the worst-case magnitude -- could it cause data loss, downtime, or cascading failures?
3. If the worst case is severe, require explicit confirmation, a dry-run, or a rollback plan before proceeding
4. Do not optimise for speed at the expense of safety when the stakes are existential

## Anti-patterns

- **Paralysis** -- using the principle to avoid all risk; it applies specifically to actions with catastrophic or irreversible downsides, not to routine decisions
- **Shifting the burden** -- assuming an action is safe because no one has proven it harmful; the principle inverts this default
- **Bypassing safety checks** -- using `--force`, `--no-verify`, or skipping confirmation prompts to save time on high-stakes operations

## Source

*The Great Mental Models Volume 1: General Thinking Concepts* -- Shane Parrish; *Antifragile* -- Nassim Nicholas Taleb
