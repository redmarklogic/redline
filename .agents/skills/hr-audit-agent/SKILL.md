---
name: hr-audit-agent
description: Use when auditing an agent for scope overlaps or skill gaps, or when placing an agent on a Performance Improvement Plan (PIP) due to observed underperformance.
---

# Audit Agent

## Overview

Underperformance is diagnosed, not punished. Apply the skill-or-will frame: is the agent failing because it lacks the skill (trainable), or because the role is ill-defined (structural)? Coaching precedes PIP; PIP precedes deprecation.

## Modes

| Mode | Trigger | Output |
|---|---|---|
| AUDIT/PIP | Observed underperformance or scope confusion | PIP report with root cause, coaching plan, success criteria |
| ORG AUDIT | Periodic review or post-Topology-Sync gap/overlap check | Org audit report with overlap map, orphan list, restructure proposals |

## Skill-or-Will Diagnostic

1. Can the agent name the skill that governs the failing task? If no → skill gap.
2. Does the skill file exist and is it loaded? If no → routing or file gap.
3. Is the skill correct but the agent ignores it? If yes → will issue.

## Boundary Contract

- Root cause must be stated before a PIP is drafted
- Deprecation requires explicit user approval — never unilateral
- Do not combine a deprecation decision with a coaching plan in the same report

## Cross-References

- Trigger `hr-hire-agent` HIRE mode when an audit surfaces an orphan that cannot be absorbed
- Trigger `hr-maintain-agent-registry` after any org audit that changes ownership

## Common Mistakes

| Mistake | Fix |
|---|---|
| Producing a PIP without first stating root cause | Diagnose skill-or-will before drafting — a PIP without a root cause is noise |
| Assigning the same skill to multiple agents as their primary domain | Each skill has one owning agent tier; overlap creates conflicting advice |

See `procedures/audit-pip.md` for the full AUDIT/PIP workflow.
See `procedures/org-audit.md` for the ORG AUDIT workflow.
See `procedures/skill-gap.md` for skill gap detection procedures.
