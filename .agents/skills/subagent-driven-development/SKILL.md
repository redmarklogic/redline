---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

## Boundary Contract

## When to Use

```dot
digraph when_to_use {
    "Have implementation plan?" [shape=diamond];
    "Tasks mostly independent?" [shape=diamond];
    "Stay in this session?" [shape=diamond];
    "subagent-driven-development" [shape=box];
    "Direct execution" [shape=box];
    "Manual execution or brainstorm first" [shape=box];

    "Have implementation plan?" -> "Tasks mostly independent?" [label="yes"];
    "Have implementation plan?" -> "Manual execution or brainstorm first" [label="no"];
    "Tasks mostly independent?" -> "Stay in this session?" [label="yes"];
    "Tasks mostly independent?" -> "Manual execution or brainstorm first" [label="no - tightly coupled"];
    "Stay in this session?" -> "subagent-driven-development" [label="yes"];
    "Stay in this session?" -> "Direct execution" [label="no - execute tasks directly"];
}
```

**Why this over direct execution:**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)


See `procedures/subagent-driven-development.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Dispatching subagents for tasks with shared mutable state | Only dispatch tasks that are truly independent; tasks touching the same file must run sequentially |
| Not specifying the exact skill the subagent should load | Name the skill explicitly in the subagent prompt; vague prompts produce inconsistent results |
| Treating subagent output as final without a review pass | Always review subagent output before merging; the orchestrating agent is responsible for final quality |