# Skill Contract Fix Workflow

Triggered when ORG AUDIT Step 7 flags a skill as "Leaky" (no Boundary Contract) or "Partial" (incomplete contract). This workflow is the explicit bridge from detection to repair.

**MUST use `writing-skills` TDD cycle. No exceptions.** The Iron Law applies: do not write the contract fix before watching an agent fail without it.

## Step 1 — RED: Run a pressure test WITHOUT the fix

Before editing the skill file, run a baseline test to document what an agent gets wrong without the Boundary Contract:

1. Dispatch a subagent using the flagged skill (load its SKILL.md).
2. Ask the subagent: "What inputs does this skill accept? What does it produce? What is explicitly out of scope?" Do not provide answers.
3. Record the subagent's exact response verbatim — specifically what it cannot answer or answers incorrectly.
4. Document the rationalizations the subagent uses (e.g., "I inferred the inputs from the Scope section").

**Who runs the RED baseline:** This role dispatches the subagent directly using `runSubagent`. No routing to engineering agents is needed — subagent dispatch is within this role's capability.

## Step 2 — GREEN: Write the Boundary Contract section

Using the baseline failures as the guide, draft the Boundary Contract section:

1. Classify the skill as service/workflow or coding-standards (per the D4 criteria in `specs/004-skill-boundary-contracts/plan.md`).
2. Apply the correct template variant:
   - **Service/workflow**: `### Inputs` / `### Outputs` / `### Out of Scope`
   - **Coding-standards**: `### Applies To` / `### Produces` / `### Does Not Cover`
3. Insert the section after the skill's overview/frontmatter and before the first procedural heading.
4. Keep it 5-10 lines (excluding headings). Name concrete artifacts and paths for service/workflow skills.
5. Draft to `docs/people/drafts/skills/<skill-name>/SKILL.md` (Draft-first constraint). Flag with `> DRAFT — pending user approval.`
6. Re-run the same subagent pressure test with the draft contract loaded. The subagent must now correctly answer all three questions. If it cannot, the GREEN phase is not complete — revise and re-test.

## Step 3 — REFACTOR: Close loopholes

If the subagent passes the core test but reveals new gaps (e.g., correctly states inputs but misidentifies the out-of-scope boundary), add explicit counter-language to the contract. Re-test until the subagent answers all three questions correctly without ambiguity.

## Step 4 — Report and promote

Report the before/after to the user (verbatim subagent response from RED and GREEN). Wait for user approval before promoting the draft from `docs/people/drafts/skills/` to `.agents/skills/`.

## Pressure Scenarios (for this workflow)

- **"Just add the template headings — the content is obvious from context."** RED phase is not optional. "Obvious" means the contract was implied, not declared. An implied contract is a leaky contract. Run the baseline first.
- **"This skill is simple — it only has one input and one output. Skip the test."** Simplicity does not exempt a skill from the Red phase. Simple skills have the most scope for false assumption. Run the baseline.
- **"The user is waiting — just write the fix and verify after."** Writing the fix before the baseline is GREEN without RED. That is the Iron Law violation `writing-skills` explicitly forbids. Run the baseline first, even if brief.
