# Create a Skill — RED-GREEN-REFACTOR

**See:** `writing-skills/SKILL.md` for schema, vocabulary, naming rules, and the Iron Law.
**See:** `testing-skills-with-subagents.md` for the full pressure-scenario methodology.

---

## RED: Write Failing Test (Baseline)

1. Write 3+ pressure scenarios combining **time pressure**, **sunk cost**, and **authority** ("everyone does it this way").
2. Run scenarios with a **fresh subagent** and **no skill loaded**.
3. Document exact behavior verbatim: choices made, rationalizations used, which pressures triggered violations.

Do NOT write the skill until you have documented baseline failures.

---

## GREEN: Write Minimal Skill

1. Write the skill addressing the **specific rationalizations** from RED. Do not add content for hypothetical cases.
2. Run the same scenarios **with the skill loaded**. Agent must now comply.
3. Verify:
   - Description starts with `"Use when..."` and contains no workflow summary.
   - Boundary Contract section present (correct variant — see SKILL.md).
   - Keywords appear early for search.

---

## REFACTOR: Close Loopholes

1. Document any new rationalization the agent finds with the skill present.
2. Add an explicit counter to the skill for each new loophole.
3. Build a rationalization table and a red-flags list.
4. Re-test until the agent complies under maximum pressure.

---

## Skill Creation Checklist

Use TodoWrite to track these items for **each** skill.

**RED Phase:**
- [ ] 3+ pressure scenarios created (time + sunk cost + authority)
- [ ] Baseline run documented verbatim — no skill loaded
- [ ] Rationalization patterns identified

**GREEN Phase:**
- [ ] Name uses only letters, numbers, hyphens (no parentheses or special chars)
- [ ] YAML frontmatter: `name` + `description` fields (max 1024 chars total)
- [ ] Description starts with `"Use when..."` — triggering conditions only, third person, no workflow summary
- [ ] Boundary Contract present (correct variant)
- [ ] Keywords throughout for search (error messages, symptoms, tool names)
- [ ] Content addresses the **specific** baseline failures from RED
- [ ] Run WITH skill — agent now complies

**REFACTOR Phase:**
- [ ] New rationalizations identified and countered explicitly
- [ ] Rationalization table built from all test iterations
- [ ] Red-flags list present (discipline skills only)
- [ ] Re-tested until bulletproof

**Quality:**
- [ ] Flowchart only if decision is non-obvious
- [ ] Quick reference table present
- [ ] Common mistakes section present
- [ ] No narrative storytelling
- [ ] Supporting files only for tools or heavy reference (not inline alternatives)

**Deployment:**
- [ ] Registered in `AGENTS.md` under `## Skills` with format:
  `- **\`<skill-name>\`**: <Short description matching frontmatter>`
- [ ] Committed to git and pushed

---

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Write skill before testing? **Delete it. Start over.**
Edit skill without testing? **Same violation.**

**No exceptions:**
- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Don't keep untested changes as "reference"
- Don't "adapt" while running tests
- Delete means delete

---

## Stop Before Moving On

After writing ANY skill, complete the deployment checklist before starting the next skill.

Do NOT create multiple skills in a batch without testing each. Deploying untested skills is deploying untested code.
