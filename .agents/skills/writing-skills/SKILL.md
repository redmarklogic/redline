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
What goes wrong + fixes.
```
