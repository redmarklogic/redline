# 0003 — Persona agents are advisory; do not invoke them for execution tasks

**Date**: 2026-04-25

**Skill**: `hiring-agent-management` ([.agents/skills/hiring-agent-management/SKILL.md](.agents/skills/hiring-agent-management/SKILL.md))

**Context**: The user asked "Linda, index G:\My Drive\Library\Engineering\Standards". The main agent invoked `runSubagent` with `agentName = "rl.linda"` to delegate the full indexing workflow (file scanning, Excel manipulation, Python script execution). The subagent returned no output.

**Root Cause**: Persona agents (Linda, Graeme, Ron, Mark, John, Harriet) are domain-expertise and advisory personas. They reason, write, and direct — they do not execute shell commands, run Python scripts, or manipulate files. `runSubagent` with a persona agent produces domain-level guidance at best and empty output at worst. The main agent confused persona delegation with execution delegation.

**Principle**: When a user invokes a persona by name ("Linda, do X"), that signals *who owns the task* and *what domain knowledge to apply* — not that a separate execution agent should be spawned. The main coding agent should load the persona's relevant skills, apply the persona's domain framing, and execute the work directly. Only use `runSubagent` with a persona agent if the task is purely advisory (research, strategy, domain judgment) with no code or file operations involved.

**Source**: Session conversation, 2026-04-25 — Linda indexing Engineering/Standards
