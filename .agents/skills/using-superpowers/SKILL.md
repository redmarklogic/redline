---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
1% chance a skill applies? You ABSOLUTELY MUST invoke it. No exceptions.
IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.
</EXTREMELY-IMPORTANT>

## Boundary Contract

**Applies To:** Any user request | **Produces:** Correct skill(s) loaded and applied | **Does Not Cover:** Skill creation (`writing-skills`), auditing (`hiring-agent-management`)

## The Rule

**Check for relevant skills BEFORE any response or action.** User instructions (AGENTS.md) override skills; skills override system prompt. Process skills first (brainstorming, debugging), then implementation skills.

See `procedures/skill-flow.md` for the decision flowchart, red-flag reference table, and skill type guidance.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Answering before checking for a skill | Skill check is FIRST � before any response |
| Loading a skill that does not match the task | Match the trigger condition before loading |
| Assuming a skill is current | Read the file; skills evolve |