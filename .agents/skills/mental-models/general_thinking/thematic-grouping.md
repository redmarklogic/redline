# Thematic Grouping

## What it is

Thematic grouping is the practice of organising a set of items -- commits, tasks, review comments, or changes -- by logical theme or cohesion rather than by time, author, or file location. Each group should be understandable in isolation and carry a single, coherent intent.

## Core principle

A batch of work is easier to review, revert, and reason about when each unit is internally coherent. Mixing themes in a single unit forces reviewers to mentally separate concerns the author should have separated already.

## When to invoke

- Staging commits for a pull request that touches multiple concerns
- Batching tasks across parallel agents or a sprint
- Structuring review feedback so that related comments are reported together
- Deciding whether to merge two changes into one unit or keep them separate

## How to apply

1. List all individual changes or items in scope
2. Assign each item a theme label (e.g., refactor, bug fix, feature, config, docs)
3. Group items that share a theme and verify each group tells a coherent, self-contained story
4. Sequence groups so that later groups depend on earlier ones (topological order where possible)
5. Split any group that contains items from two distinct themes, even if those items touch the same file

## Anti-patterns

- **Chronological batching** -- grouping by "things done today" rather than by what they mean; the resulting units are only intelligible to the author immediately after writing them
- **Over-splitting** -- one group per change regardless of size; atomic units are valuable but microgroups create noise without improving clarity
- **Theme sprawl** -- allowing a group to grow until it is "mostly" one theme, producing commits that reviewers cannot confidently summarise in a single sentence

## Source

Software engineering practice; described in the *git-push-batched* skill in this repository and the broader version-control community convention of semantic commits
