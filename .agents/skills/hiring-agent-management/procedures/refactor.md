# REFACTOR Workflow

**Trigger:** User says "Harriet, refactor skill `<skill-name>`" — or asks to restructure, modularise, or split a skill.

## What "refactor" means

A skill refactor extracts embedded content into its canonical home:

| Content type | Move to |
|---|---|
| Step-by-step procedures (workflow phases, numbered how-to steps) | `procedures/<name>.md` next to the SKILL.md |
| Reusable Python scripts, shell scripts, utilities | `.agents/tools/<domain>/` |
| Heavy reference (100+ line tables, full API docs) | Supporting `.md` file next to SKILL.md |

The resulting SKILL.md is a **lean reference** — schema, vocabulary, naming rules, a phase-map table pointing to the procedures, and a tools reference table. It does not contain inline code that belongs in a tool, and does not contain step-by-step prose that belongs in a procedure.

## Mandatory TDD Gate (behavioral changes)

If the refactor adds, removes, or changes a behavioral constraint — a "NEVER do X" guardrail, an escalation rule, a boundary, a prohibited action — the TDD gate below is **mandatory before proceeding to Steps 1-5**. Structural-only moves (extracting prose to `procedures/`, extracting code to tools) do not require this gate.

**REFACTOR is not complete until GREEN is declared and the test file exists.**

| Step | Action |
|---|---|
| **T1 — Write the test case first** | Create `.agents/skills/<name>/tests/test-<scenario>.md`. Define the pressure prompt (exact wording that would trigger a violation), RED behaviour (what the agent does without the constraint), and GREEN criteria (observable compliant behaviour — minimum three testable signals). |
| **T2 — RED baseline** | Invoke the relevant agent with the pressure prompt *without* applying the proposed constraint edit. Record the verbatim or summarised response. Confirm it fails — GREEN criteria not met. Do NOT proceed to T3 if RED was not demonstrated. |
| **T3 — Make the minimal skill edit** | Edit the SKILL.md with only the change required to achieve GREEN. No scope creep. No opportunistic improvements. |
| **T4 — GREEN verification** | Re-invoke the agent with the same pressure prompt with the edit present. Confirm all GREEN criteria are met. Record the result in the test case file's Result Log table. |
| **T5 — Declare GREEN** | Explicitly state "GREEN declared" before closing the task. If any criterion fails, revise the skill edit and re-run T4. Do NOT declare completion without this statement. |

**Pressure scenario banking:** Store every test case in `.agents/skills/<name>/tests/`. Re-run all tests in that directory after any subsequent edit to the same skill.

## Steps

### Step 1 — Audit the skill

Read the full SKILL.md. Classify every section:
- Phase/workflow content with numbered steps → candidate for `procedures/`
- Python/shell code blocks > ~30 lines, or code that runs standalone → candidate for `.agents/tools/<domain>/`
- Schema tables, vocabulary, naming rules, common mistakes → stays in SKILL.md

### Step 2 — Create tools

For each code block moving to a tool:
1. Create `.agents/tools/<domain>/<script-name>.py` (or `.sh`).
2. Add a module docstring explaining purpose, usage, and CLI args.
3. Where the skill had a monolithic block, split into importable helper functions and a runnable entry point.
4. **Never hardcode user-specific paths** (e.g., `C:\Users\harel\...`). Use relative paths from the repo root, `pathlib.Path(__file__).resolve().parents[N]`, `$env:TEMP` in PowerShell, or `tempfile.gettempdir()` in Python. See the no-hardcoded-paths rule in `writing-skills`. <!-- hook: allow -->

### Step 3 — Create procedures

For each workflow section moving out of SKILL.md:
1. Create `procedures/<name>.md` next to the SKILL.md.
2. Write the procedure as direct imperative steps. Reference tools by relative path from the repo root (e.g., `.agents/tools/library/metadata_extractor.py`), not by absolute path.
3. The procedure file may contain short code snippets (< 30 lines) that are context-specific (i.e., not worth a standalone tool). Keep them inline.

### Step 4 — Rewrite SKILL.md

Replace extracted sections with:
- A **phase/workflow table** (one row per phase) with a link to the procedure file.
- A **tools reference table** (one row per script) with purpose and invocation hint.
- Retain all schema, vocabulary, naming rules, and common mistakes inline.

Verify: no inline code duplicates what a tool already does. No prose step duplicates what a procedure already says.

### Step 5 — No-redundancy check

Cross-read SKILL.md, all procedure files, and all tools. Flag any content that appears in two places. Remove from the less authoritative location.

## Output

- Refactored SKILL.md (lean)
- `procedures/` directory with one `.md` per workflow
- `.agents/tools/<domain>/` files (if code was extracted)
- No draft-first required for skill refactors — write directly to `.agents/skills/<name>/`
