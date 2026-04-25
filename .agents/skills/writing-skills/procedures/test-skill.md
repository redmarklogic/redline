# Test a Skill — Strategy by Type

**See:** `writing-skills/SKILL.md` for boundary contract and schema.
**See:** `testing-skills-with-subagents.md` for how to write and run pressure scenarios.

---

## Test Strategy by Skill Type

### Discipline-Enforcing Skills
*Examples: TDD, verification-before-completion, designing-before-coding*

| Test type | What to run |
|---|---|
| Academic | Does the agent understand the rules? |
| Pressure | Does it comply under time + sunk cost + authority? |
| Combined | Run all pressures together |

**Success:** Agent follows the rule under maximum pressure.

### Technique Skills
*Examples: condition-based-waiting, root-cause-tracing*

| Test type | What to check |
|---|---|
| Application | Can the agent apply the technique to a new scenario? |
| Variation | Does it handle edge cases? |
| Gap | Are there missing-information holes in the instructions? |

**Success:** Agent applies technique correctly to an unfamiliar scenario.

### Pattern Skills
*Examples: reducing-complexity, flatten-with-flags*

| Test type | What to check |
|---|---|
| Recognition | Does the agent identify when the pattern applies? |
| Application | Can it use the mental model correctly? |
| Counter-examples | Does it know when NOT to apply? |

**Success:** Agent correctly identifies when and how to apply the pattern.

### Reference Skills
*Examples: API docs, syntax guides, graphviz-conventions*

| Test type | What to check |
|---|---|
| Retrieval | Can the agent find the right information? |
| Application | Does it use what it found correctly? |
| Gap | Are common use cases covered? |

**Success:** Agent finds and correctly applies reference information.

---

## Common Rationalizations to Pre-empt

| Excuse | Reality |
|---|---|
| "Skill is obviously clear" | Clear to you ≠ clear to other agents. Test it. |
| "It's just a reference" | References can have gaps, unclear sections. Test retrieval. |
| "Testing is overkill" | Untested skills have issues. Always. 15 min testing saves hours. |
| "I'll test if problems emerge" | Problems = agents can't use the skill. Test BEFORE deploying. |
| "Academic review is enough" | Reading ≠ using. Test application scenarios. |
| "No time to test" | Deploying untested skill wastes more time fixing it later. |

---

## Bulletproofing Discipline Skills

### Close Every Loophole Explicitly

State the rule, then forbid specific workarounds by name:

```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Delete means delete
```

### Address "Spirit vs Letter" Arguments

Add this line near the top of the skill's enforcement section:

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

This cuts off an entire class of "I'm following the spirit" rationalizations.

### Create a Red Flags List

```markdown
## Red Flags — STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

All of these mean: Delete. Start over.
```

### Update the Description for Violation Symptoms

The description should include symptoms of when the agent is *about to violate* the rule — not just when the skill applies in general.

```yaml
# Triggers the skill when the agent is on the verge of skipping TDD
description: Use when implementing any feature or bugfix, before writing implementation code
```

### Rationalization Table

After each test iteration, capture every excuse the agent used verbatim. Add an explicit counter for each:

```markdown
| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "Tests after achieve same goals" | Tests-after = what does this do? Tests-first = what should this do? |
```

The table grows with each REFACTOR iteration until the agent finds no new loopholes.
