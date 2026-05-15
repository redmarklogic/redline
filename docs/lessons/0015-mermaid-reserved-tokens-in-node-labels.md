# 0015 — Mermaid reserved tokens break node labels in v8.8.0

**Date**: 2026-05-15

**Skill**: `mermaid-diagrams` (link: `.agents/skills/mermaid-diagrams/SKILL.md`)

**Context**: Writing a flowchart procedure for the `receiving-code-review` skill. Node labels included CLI flag notation (`gh run view --log-failed`), `\n` line breaks inside stadium shapes (`([...])`), and em dash characters (`—`).

**Observation**: Diagram rendered as "Syntax error in graph — mermaid version 8.8.0" with no output. All three problems were present simultaneously, but `--` inside a node label is the most common and least obvious trigger.

**Root Cause**: Mermaid's 8.8.0 lexer tokenises `--` as the start of an edge operator (`-->`, `---`) regardless of whether it appears inside a node label string. The lexer does not distinguish between `--` in a label context and `--` as an edge connector. Em dashes (`—`) and `\n` in non-rectangular node shapes (`([...])`, `{...}`) are separately unreliable under the same version.

**Principle**: Never use `--` inside Mermaid node labels — rephrase CLI flags and double-hyphen constructs as plain text. Avoid `\n` inside non-rectangular shapes (stadium `([...])`, diamond `{...}`); use shorter single-line labels instead. Avoid non-ASCII punctuation (em dash, en dash, curly quotes) in any label. If a label requires any of these, simplify the label — do not try to escape or quote around the problem.

**Source**: `receiving-code-review/procedures/pre-flight.md` — first render attempt, 2026-05-15.
