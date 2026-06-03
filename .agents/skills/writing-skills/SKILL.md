---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

## Boundary Contract

### Applies To
- New SKILL.md files in `.agents/skills/<name>/`
- Edits to existing skills
- Supporting procedure, reference, and tool files

### Produces
- `SKILL.md` with frontmatter, boundary contract, and lean reference content
- `procedures/<name>.md` for step-by-step workflows
- Supporting `.md` or script files for heavy reference or reusable tools

### Does Not Cover
- Agent files (use `hiring-agent-management`)
- Project-specific conventions (put in `AGENTS.md`)
- Deciding what to build (use `brainstorming`)

## Boundary Contract
Required. Variants:
- Service/workflow skills: Inputs / Outputs / Out of Scope
- Coding-standards skills: Applies To / Produces / Does Not Cover
Service/workflow contracts must name concrete artifacts (file names, paths).

## When to Use
Bullets with symptoms and use cases; when NOT to use.


See `procedures/writing-skills.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running `check-skill-*` hooks only at commit time, not during drafting. | Run all prek hooks at the end of GREEN phase (before Deployment). Fix violations before proceeding to the next step. |
| Persona names in skill file content (agent names). | Skill files are agent-agnostic. Name capabilities and functions, not people. Run `check-banned-words.py` hook to verify. |
| Not registering the skill in `docs/architecture/skills-architecture.md`. | Every skill must have a layer assignment before the deployment checklist is complete. No layer assignment = not deployed. |
```
