# Notebooklm Deep Research — Detailed Reference

### Inputs
- One research objective in plain language.
- Optional project context, such as product area, stakeholder, and decision window.
- Optional named reviewer, only if the user explicitly requested reviewer routing before research starts.

### Outputs
- A strict 5 Whys capture: five answered Why questions, or an explicit skip point.
- A search query built from captured intake answers, with audience prefix and source-only scope constraint.
- A selective source import decision with rationale.
- Notebook indexed and registered via `notebooklm-index` after notebook creation and source import.
- A notebook package returned to the user for next-step decision.
- If a named reviewer was explicitly requested earlier: reviewer output plus the same notebook package returned to the user.

### Out of Scope
- CLI setup or authentication (use `notebooklm-mcp`).
- Multi-notebook synthesis orchestration (use `redline-research`).
- Autonomous execution after the notebook package is returned, unless the user gives a new instruction.
- Reviewer routing when no explicit reviewer request was made earlier.

## Non-Negotiable Rules

1. Use only the 5 Whys framework.
2. Ask exactly five Why questions unless the user selects Skip.
3. Every question must start with: `Question X of 5: Why ...`
4. Every question must contain one explicit assumption sentence. Do not use vague terms such as "this", "that", or "current assumptions".
5. Keep wording plain for uninitiated users.
6. Every question must present exactly three predefined options plus `Skip and start search now`.
7. Option labels must not contain manual numbering. The chat user interface already numbers options.
8. Do not include an `Other` option. Keep free-text enabled for custom answers.
9. If Skip is selected at any step, stop questioning and immediately run search with the captured answers.
10. Build the search query from captured answers. If no answers were captured, use the original explicit assumption.
11. Query construction must include the `rag-prompting` audience prefix and a source-only scope constraint.
12. Never fabricate runtime identifiers, including `notebook_id`, `task_id`, and `source_id`.
13. Use `mode="deep"` only with `source="web"`. If `source="drive"`, use `mode="fast"`.
14. Import sources selectively by `source_indices`.
15. Import all sources only with explicit user approval.
16. After notebook creation and import, run `notebooklm-index` before declaring completion.
17. Default endpoint is return-to-user with notebook package, then stop for user decision.
18. Reviewer routing is opt-in only and is allowed only when the user explicitly requested a named reviewer earlier.

## Procedure

1. Capture the user objective and project context.
2. Check whether the user explicitly requested a named reviewer earlier.
3. Record the route now: default return-to-user, or reviewer route only if explicitly requested.
4. Draft the first explicit assumption sentence from the user objective.
5. Ask Question 1 of 5 using the required format and helper text.
6. For each next question, restate the specific assumption from the previous answer and ask the next Why using the same option rules.
7. Continue until Question 5 is answered, or stop immediately if Skip is selected.
8. Compile captured intake answers.
9. If no answers were captured, use the original explicit assumption as the intake basis.
10. Build the research query using `rag-prompting` audience prefix and source-only scope constraint.
11. Validate research mode and source pairing before start: deep with web only, drive requires fast.
12. Start research, poll status to completion, triage discovered sources, and prepare a selective import list with rationale.
13. If import-all is proposed, request explicit user approval before import.
14. Import selected sources by `source_indices`.
15. Run `notebooklm-index` to upsert the notebook in the registry/index.
16. Assemble the notebook package with notebook title, notebook URL, notebook_id, imported source count, imported source list with rationale, index confirmation, and suggested next actions.
17. If reviewer route was explicitly requested earlier, pass the package to the named reviewer, then return reviewer output plus the same package to the user.
18. If reviewer route was not explicitly requested earlier, return the notebook package directly to the user.
19. Stop and wait for the user to choose the next action.
