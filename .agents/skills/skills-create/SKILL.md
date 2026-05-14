---
name: skills-create
description: Instructions for creating a new GitHub Copilot skill file and registering it in this repo.
---

# Create Skill

This skill is only for creating a brand-new skill folder and `SKILL.md` file.

For modifying/refactoring existing skills, edit the `SKILL.md` file directly.
For diagnostic compliance checks, run `uv run pre-commit run --all-files` before committing.

## Boundary Contract

### Inputs
- Skill idea or requirement for a new skill

### Outputs
- New skill directory at `.agents/skills/<name>/` with `SKILL.md`

### Out of Scope
- Skill content authoring and TDD cycle (`writing-skills`)
- Agent hiring or auditing (`hiring-agent-management`)
- Code implementation

## Workflow

Follow these steps when asked to create a new skill.

### 1. Choose Name and Path

All skills must use a directory-based structure.

Apply the hierarchical prefix naming principle:

- Use a domain prefix first, then the action/topic.
- Skill governance/meta skills use `skills-*` (for example: `skills-create`).
- Keep names kebab-case and specific to one responsibility.
- **NEVER name a skill after an agent.** Skills are agent-agnostic. Agent names must never appear in a skill name or anywhere in skill content. Agents know which skills to load; skills do not know which agent uses them. Use function or domain prefixes instead (e.g., `hiring-`, `strategy-`, `marketing-`).

To create a skill:

1. Ensure `.agents/skills` exists.
2. Create a new subdirectory using `kebab-case`.
3. Create `SKILL.md` in that directory.

**Path**: `.agents/skills/<kebab-case-skill-name>/SKILL.md`

**NEVER use a backslash (`\`) in the skill directory name or file path.** On Linux, a backslash is a valid filename character and will produce an invalid flat file (e.g., `api-testing\SKILL.md`) rather than the intended subdirectory. Such paths cannot be checked out on Windows and are not rendered correctly on GitHub. Always use a forward slash (`/`) as the path separator.

### 2. Create Initial Content

> **STOP. Before writing any content, load and follow `writing-skills` (specifically
> `procedures/create-skill.md`). The Iron Law is non-negotiable: no skill content may
> be written before baseline failure is documented. If you have already written content
> without running RED-phase tests, delete the content and start the TDD cycle from
> scratch.**

**Skills must not reference `docs/lessons/` files.** Lessons are ephemeral observations
for humans; skills are authoritative, durable instructions for the agent. Embed any
required guidance directly in the skill body rather than linking to a lesson.

**Never hard-code the project's package name.** Use generic placeholders such as
`src/<package>/`, `<package>`, or `<package>.<submodule>` wherever a package or module
name would otherwise appear. This keeps the skill transferable across projects. When a
skill references a specific module path (e.g., `src/<package>/domain/constants.py`),
also state whether that file is expected to already exist or must be created, and explain
its purpose — never silently assume it exists.

**Never use ambiguous pronouns in skill directives.** Each rule or instruction
must be self-contained and unambiguous when read in isolation. Use explicit
noun phrases instead of pronouns (`"the skill file"`, not `"it"`;
`"the canonical skill"`, not `"that one"`).

**Cross-referencing other skills is encouraged.** When a skill relies on behaviour
defined in a peer skill, reference it by name rather than duplicating the guidance:

```markdown
For function design rules, use the `python-function-design` skill.
```

Use the following template for the `SKILL.md` file. Ensure strict adherence to the YAML frontmatter.

````markdown
---
name: <skill-name-kebab-case>
description: <Short description of what the skill does (max 1024 chars)>
---

# <Skill Title>

<Detailed description of the context and purpose of this skill.>

## Context & Guidelines

- **Scope**: When should this skill be applied?
- **Constraints**: specific libraries to use/avoid, naming conventions, etc.
- **File Placement**: Where should generated files be placed?

## Procedure

1.  Step-by-step instructions for the task.
2.  ...

## Examples

### Good Example

```<language>
<code snippet>
```

### Bad Example (Optional)

```<language>
<code snippet>
```
````

### 3. Registration

After creating the skill file:

1. Open `AGENTS.md`.
2. Locate the `## Skills` section and find the appropriate `###` subsection for the skill's
   domain prefix (e.g. `### Python --- Core` for `python-*` skills). Add one line in this format:

   ```markdown
   - **`<skill-name>`**: <Short description matching the frontmatter description>
   ```

   If no suitable subsection exists, create a new `###` heading and add the entry beneath it.
   Do not paste detailed checklists into `AGENTS.md`; keep the skill as
   the canonical source of truth.

3. Stage **both** files together:

```powershell
git add .agents/skills/<skill-name>/SKILL.md AGENTS.md
```

## References

For inspiration and best practices on writing skills, consult these resources:

- [Agent Skills Standard & Registry](https://agentskills.io/home)
- [VS Code Copilot Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Awesome Copilot Skills](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
