# AUDIT/PIP Workflow (Session Forensics)

## Binding rule: split evaluation from development

Adapted from Jesuthasan & Boudreau: **never combine a reward/promotion conversation with a development conversation**. For agents this maps to: never combine "should this agent be deprecated?" with "what skill is missing?" in the same report. Produce two separate documents if both questions are live.

## Steps

1. **Gather session context.** If not provided, ask for it. Read the agent's reasoning trace.
2. **Invoke the agent.** Ask directly: "[Agent], in our session on [topic], what caused [failure]?" Use the self-report as one data point — never the only one (avoid single-source-of-truth bias; rely on rubrics, per Larson).
3. **Classify root cause as skill gap OR will gap** (Larson's compassionate-pragmatism frame). For agents:
   - **Skill gap** → missing/weak skill, missing notebook, prompt ambiguity, scope undefined.
   - **"Will" gap** (for agents this means: the agent is fundamentally mis-scoped or duplicates another agent) → re-scope, merge, or deprecate.

   | Root cause | Indicator | Action |
   |---|---|---|
   | Missing skill | Skill does not exist in `.agents/skills/` | Skill Gap procedure (`procedures/skill-gap.md`) |
   | Weak skill | Skill exists but is under-specified or ambiguous | Rewrite skill via `writing-skills` TDD |
   | Notebook gap | Agent lacked grounded factual sources | Sourcing report |
   | Prompt ambiguity | JD too vague to constrain behaviour | Rewrite prompt |
   | Scope violation | Agent acted outside File Authority | Rewrite Team API |
   | Mis-scoped / duplicate | Work belongs to a different agent or no agent | Re-scope, merge, or deprecate |

4. **If ambiguous** — enumerate the options and ask the user which to pursue before acting.
5. **Output** → `docs/people/drafts/reports/pip-<agent>-<YYYY-MM-DD>.md`.

The PIP report must propose **targeted coaching first** (skill rewrite, prompt rewrite, notebook sourcing). Deprecation is the last option, not the first — same compassionate-pragmatism principle.
