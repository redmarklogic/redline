# Tasks: Skill Compliance Remediation

**Feature**: 010-skill-compliance-remediation  
**Generated**: 2026-05-30

---

## Phase 0 â€” Setup & Vendor Exclusion

### T-001 â€” Document vendor exclusion for speckit-* skills
- **File**: `specs/010-skill-compliance-remediation/vendor-exclusions.md`
- Create a brief record noting the 4 speckit-* skills are vendor-managed symlinks excluded from remediation scope
- Skills: `speckit-shaping-gate-check`, `speckit-source-reconciliation-run`, `speckit-static-checks-run`, `speckit-verification-gate-run`
- Status: [X]

---

## Phase 1 â€” Quick Wins

### T-002 â€” Fix hardcoded paths in `library-management` [P]
- **File**: `.agents/skills/library-management/SKILL.md`
- Replace all occurrences of `G:\My Drive\Library` with `<library-root>`
- Add configuration note: "Set `<library-root>` to the absolute path of your library root before using this skill."
- Status: [X]

### T-003 â€” Fix hardcoded paths in `notebooklm-index` [P]
- **File**: `.agents/skills/notebooklm-index/SKILL.md`
- Replace all occurrences of `G:\My Drive\Library\index-notebooklm.xlsx` with `<library-root>/index-notebooklm.xlsx`
- Status: [X]

### T-004 â€” Fix hardcoded paths in `notebooklm-mcp` [P]
- **File**: `.agents/skills/notebooklm-mcp/SKILL.md`
- Replace hardcoded drive-letter or UNC paths with project-relative or placeholder equivalents
- Status: [X]

### T-005 â€” Add `## Boundary Contract` to `mental-models`
- **File**: [mental-models/SKILL.md](../../.agents/skills/mental-models/SKILL.md)
- Add section with: Applies To, Produces, Does Not Cover
- Place after Overview/intro section
- Status: [X]

---

## Phase 2 â€” Description Rewrites (39 skills)

All descriptions must start with `"Use when"` and contain no workflow summary. Keep under 500 chars. Write in third person.

### T-010 â€” Rewrite descriptions: Python skills batch A [P]
Failing skills: `python-class-design`, `python-crewai`, `python-data-ingestion`, `python-deptry`, `python-documentation`, `python-domain-modeling`, `python-error-handling`, `python-function-design`
- Rewrite each `description:` field in frontmatter to "Use when [triggering condition]"
- Status: [X]

### T-011 â€” Rewrite descriptions: Python skills batch B [P]
Failing skills: `python-linting`, `python-mcp-tools`, `python-module-structure`, `python-paths`, `python-patterns`, `python-performance`, `python-pins-data-version-control`, `python-plot-colors`
- Rewrite each `description:` field
- Status: [X]

### T-012 â€” Rewrite descriptions: Python skills batch C [P]
Failing skills: `python-script`, `python-script-numbering`, `python-static-checks`, `python-style`, `python-testing-api`, `python-testing-unit`, `python-typing`, `python-usethis`
- Rewrite each `description:` field
- Status: [X]

### T-013 â€” Rewrite descriptions: EDA & data skills [P]
Failing skills: `data-tidy`, `eda-codebook`, `eda-interpreting-data`, `eda-qa`, `eda-visual-design`, `qmd-narrative-design`, `qmd-tables`
- Rewrite each `description:` field
- Status: [X]

### T-014 â€” Rewrite descriptions: remaining skills [P]
Failing skills: `brainstorming`, `dev-environment`, `doc-updater`, `git-hooks-create`, `git-push-batched`, `hiring-agent-management`, `security`, `version-control`
- Rewrite each `description:` field
- Status: [X]

---

## Phase 3 â€” Common Mistakes Sections (56 skills)

Add `## Common Mistakes` section with at least one structured mistakeâ†’fix pair. Place after `## Core Pattern` / `## Quick Reference` or equivalent, before the last section. Derive from inline examples in the skill or domain knowledge.

### T-020 â€” Add Common Mistakes: Python skills batch A [P]
Skills: `python-class-design`, `python-crewai`, `python-data-ingestion`, `python-deptry`, `python-documentation`, `python-domain-modeling`, `python-error-handling`, `python-function-design`
- Add `## Common Mistakes` section to each
- Status: [X]

### T-021 â€” Add Common Mistakes: Python skills batch B [P]
Skills: `python-linting`, `python-mcp-tools`, `python-module-structure`, `python-paths`, `python-patterns`, `python-performance`, `python-pins-data-version-control`, `python-plot-colors`
- Status: [X]

### T-022 â€” Add Common Mistakes: Python skills batch C [P]
Skills: `python-script`, `python-script-numbering`, `python-static-checks`, `python-style`, `python-testing-api`, `python-testing-unit`, `python-typing`, `python-usethis`
- Status: [X]

### T-023 â€” Add Common Mistakes: EDA, data & QMD skills [P]
Skills: `brainstorming`, `data-tidy`, `dev-environment`, `doc-updater`, `eda-codebook`, `eda-interpreting-data`, `eda-qa`, `eda-visual-design`, `qmd-narrative-design`, `qmd-tables`
- Status: [X]

### T-024 â€” Add Common Mistakes: ceremony & process skills [P]
Skills: `ceremony-monthly-editorial-session`, `evaluation-architecture`, `git-hooks-create`, `git-push-batched`, `hiring-agent-management`, `marketing-ai-content-review`, `marketing-content-big-5`, `marketing-product-led-seo`, `marketing-social-selling-linkedin`
- Status: [X]

### T-025 â€” Add Common Mistakes: PM & strategy skills [P]
Skills: `notebooklm-mcp`, `redline-research`, `requesting-code-review`, `security`, `spec-kit`, `version-control`
- Status: [X]

### T-026 â€” Add Common Mistakes: agent workflow skills [P]
Skills: `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `using-superpowers`, `verification-before-completion`
- Status: [X]

---

## Phase 4 â€” Token Efficiency Extraction

Skills exceeding their word-count ceiling must have excess content extracted to `procedures/<skill-name>.md` or sibling reference files. A cross-reference link must remain in SKILL.md.

**Frequently-loaded skills (200w limit):** `using-superpowers` (769w), `cce-mcp` (811w), `dev-environment` (641w)
**Standard skills (500w limit):** all others above 500w

### T-030 â€” Extract frequently-loaded skills to â‰¤200 words [P]
Skills: `using-superpowers`, `cce-mcp`, `dev-environment`
- Move step-by-step workflows and detailed reference tables to `procedures/` files
- Retain Overview, Boundary Contract, When to Use, key Quick Reference, Common Mistakes
- Status: [X]

### T-031 â€” Extract: large Python skills batch A [P]
Skills over 500w: `python-class-design`, `python-crewai`, `python-data-ingestion`, `python-domain-modeling`, `python-function-design`, `python-module-structure`
- Extract procedures and reference tables; add cross-references
- Status: [X]

### T-032 â€” Extract: large Python skills batch B [P]
Skills over 500w: `python-deptry`, `python-documentation`, `python-linting`, `python-paths`, `python-patterns`, `python-performance`, `python-plot-colors`
- Status: [X]

### T-033 â€” Extract: large Python skills batch C [P]
Skills over 500w: `python-script`, `python-testing-api`, `python-testing-unit`, `python-pins-data-version-control`
- Status: [X]

### T-034 â€” Extract: EDA & QMD skills [P]
Skills over 500w: `data-tidy`, `eda-codebook`, `eda-interpreting-data`, `eda-qa`, `eda-visual-design`, `qmd-narrative-design`, `qmd-tables`
- Status: [X]

### T-035 â€” Extract: PM & marketing skills [P]
Skills over 500w: `marketing-ai-content-review`, `marketing-content-big-5`, `marketing-product-led-seo`, `marketing-social-selling-linkedin`, `pm-personas`, `pm-product-strategist`, `pm-roadmap`
- Status: [X]

### T-036 â€” Extract: knowledge management skills [P]
Skills over 500w: `library-management` (4118w), `notebooklm-deep-research`, `notebooklm-index`, `notebooklm-mcp`
- Status: [X]

### T-037 â€” Extract: strategy & architecture skills [P]
Skills over 500w: `ddd-strategic`, `dispatching-parallel-agents`, `engineering-architecture`, `evaluation-architecture` (pass â€” 355w), `strategy-pre-mortem`, `strategy-psf-domain`
- Skip `evaluation-architecture` (355w â€” within limit)
- Status: [X]

### T-038 â€” Extract: agent & ceremony skills [P]
Skills over 500w: `brainstorming`, `ceremony-agent-topology-sync`, `hiring-agent-management`, `mental-models`, `miro-mcp`, `subagent-driven-development`
- Note: `hiring-agent-management` already has `procedures/` â€” extend, don't duplicate
- Status: [X]

### T-039 â€” Extract: workflow & process skills [P]
Skills over 500w: `doc-updater`, `finishing-a-development-branch`, `git-hooks-create`, `git-push-batched`, `rag-prompting`, `resolving-pr-issues`, `shaping`, `spec-kit`
- Note: `resolving-pr-issues` already has `procedures/` â€” extend, don't duplicate
- Status: [X]

### T-040 â€” Extract: remaining skills over limit [P]
Skills over 500w: `ai-acceptable-use-policy`, `mermaid-diagrams` (492w â€” skip, within limit), `security` (188w â€” skip), `systematic-debugging`, `test-driven-development`, `using-git-worktrees`, `verification-before-completion`, `version-control`, `writing-skills`
- Skip `mermaid-diagrams` (492w), `security` (188w)
- Note: `writing-skills` already has `procedures/` â€” extend if needed
- Status: [X]

---

## Phase 5 â€” Final Audit

### T-050 â€” Generate post-remediation compliance audit table
- Run audit across all 82 editable SKILL.md files
- Produce audit table: one row per skill, columns for each of 6 principles (Frontmatter, "Use when" desc, Boundary Contract, Token Efficiency, Common Mistakes, No Hardcoded Paths), âœ…/â„¹ï¸/âŒ per cell
- Target: zero âŒ cells across all 82 skills
- Status: [X]


## Post-Remediation Compliance Audit

**Date**: 2026-05-30  **Audited**: 83  **Passing**: 83  **Failing**: 0

| Skill | Words/Lim | FM | Desc | BC | CM | Paths | Tok | Pass |
|---|---|---|---|---|---|---|---|---|
| ai-acceptable-use-policy | 425/500 | Y | Y | Y | Y | Y | Y | Y |
| brainstorming | 119/500 | Y | Y | Y | Y | Y | Y | Y |
| cce-mcp | 193/200 | Y | Y | Y | Y | Y | Y | Y |
| ceremony-agent-topology-sync | 500/500 | Y | Y | Y | Y | Y | Y | Y |
| ceremony-monthly-editorial-session | 253/500 | Y | Y | Y | Y | Y | Y | Y |
| data-tidy | 159/500 | Y | Y | Y | Y | Y | Y | Y |
| ddd-strategic | 362/500 | Y | Y | Y | Y | Y | Y | Y |
| dev-environment | 166/200 | Y | Y | Y | Y | Y | Y | Y |
| dispatching-parallel-agents | 261/500 | Y | Y | Y | Y | Y | Y | Y |
| doc-updater | 154/500 | Y | Y | Y | Y | Y | Y | Y |
| eda-codebook | 160/500 | Y | Y | Y | Y | Y | Y | Y |
| eda-interpreting-data | 176/500 | Y | Y | Y | Y | Y | Y | Y |
| eda-qa | 160/500 | Y | Y | Y | Y | Y | Y | Y |
| eda-visual-design | 156/500 | Y | Y | Y | Y | Y | Y | Y |
| engineering-architecture | 343/500 | Y | Y | Y | Y | Y | Y | Y |
| evaluation-architecture | 442/500 | Y | Y | Y | Y | Y | Y | Y |
| finishing-a-development-branch | 197/500 | Y | Y | Y | Y | Y | Y | Y |
| git-hooks-create | 134/500 | Y | Y | Y | Y | Y | Y | Y |
| git-push-batched | 429/500 | Y | Y | Y | Y | Y | Y | Y |
| hiring-agent-management | 131/500 | Y | Y | Y | Y | Y | Y | Y |
| library-management | 324/500 | Y | Y | Y | Y | Y | Y | Y |
| marketing-ai-content-review | 168/500 | Y | Y | Y | Y | Y | Y | Y |
| marketing-content-big-5 | 191/500 | Y | Y | Y | Y | Y | Y | Y |
| marketing-product-led-seo | 487/500 | Y | Y | Y | Y | Y | Y | Y |
| marketing-social-selling-linkedin | 459/500 | Y | Y | Y | Y | Y | Y | Y |
| mental-models | 309/500 | Y | Y | Y | Y | Y | Y | Y |
| mermaid-diagrams | 492/500 | Y | Y | Y | Y | Y | Y | Y |
| miro-mcp | 314/500 | Y | Y | Y | Y | Y | Y | Y |
| notebooklm-deep-research | 271/500 | Y | Y | Y | Y | Y | Y | Y |
| notebooklm-index | 195/500 | Y | Y | Y | Y | Y | Y | Y |
| notebooklm-mcp | 130/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-decision-architect | 444/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-hypothesis-builder | 392/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-personas | 469/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-prd-builder | 463/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-prioritization | 444/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-problem-framer | 420/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-product-strategist | 218/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-roadmap | 462/500 | Y | Y | Y | Y | Y | Y | Y |
| pm-structural-integrity-auditor | 375/500 | Y | Y | Y | Y | Y | Y | Y |
| python-class-design | 155/500 | Y | Y | Y | Y | Y | Y | Y |
| python-crewai | 157/500 | Y | Y | Y | Y | Y | Y | Y |
| python-data-ingestion | 165/500 | Y | Y | Y | Y | Y | Y | Y |
| python-deptry | 254/500 | Y | Y | Y | Y | Y | Y | Y |
| python-documentation | 356/500 | Y | Y | Y | Y | Y | Y | Y |
| python-domain-modeling | 287/500 | Y | Y | Y | Y | Y | Y | Y |
| python-error-handling | 489/500 | Y | Y | Y | Y | Y | Y | Y |
| python-function-design | 305/500 | Y | Y | Y | Y | Y | Y | Y |
| python-linting | 420/500 | Y | Y | Y | Y | Y | Y | Y |
| python-mcp-tools | 227/500 | Y | Y | Y | Y | Y | Y | Y |
| python-module-structure | 424/500 | Y | Y | Y | Y | Y | Y | Y |
| python-paths | 445/500 | Y | Y | Y | Y | Y | Y | Y |
| python-patterns | 481/500 | Y | Y | Y | Y | Y | Y | Y |
| python-performance | 283/500 | Y | Y | Y | Y | Y | Y | Y |
| python-pins-data-version-control | 369/500 | Y | Y | Y | Y | Y | Y | Y |
| python-plot-colors | 154/500 | Y | Y | Y | Y | Y | Y | Y |
| python-script | 291/500 | Y | Y | Y | Y | Y | Y | Y |
| python-script-numbering | 337/500 | Y | Y | Y | Y | Y | Y | Y |
| python-static-checks | 223/500 | Y | Y | Y | Y | Y | Y | Y |
| python-style | 275/500 | Y | Y | Y | Y | Y | Y | Y |
| python-testing-api | 301/500 | Y | Y | Y | Y | Y | Y | Y |
| python-testing-unit | 158/500 | Y | Y | Y | Y | Y | Y | Y |
| python-typing | 175/500 | Y | Y | Y | Y | Y | Y | Y |
| python-usethis | 210/500 | Y | Y | Y | Y | Y | Y | Y |
| qmd-narrative-design | 459/500 | Y | Y | Y | Y | Y | Y | Y |
| qmd-tables | 164/500 | Y | Y | Y | Y | Y | Y | Y |
| rag-prompting | 195/500 | Y | Y | Y | Y | Y | Y | Y |
| redline-research | 465/500 | Y | Y | Y | Y | Y | Y | Y |
| requesting-code-review | 311/500 | Y | Y | Y | Y | Y | Y | Y |
| resolving-pr-issues | 293/500 | Y | Y | Y | Y | Y | Y | Y |
| security | 275/500 | Y | Y | Y | Y | Y | Y | Y |
| shaping | 342/500 | Y | Y | Y | Y | Y | Y | Y |
| spec-kit | 167/500 | Y | Y | Y | Y | Y | Y | Y |
| strategy-pre-mortem | 445/500 | Y | Y | Y | Y | Y | Y | Y |
| strategy-psf-domain | 402/500 | Y | Y | Y | Y | Y | Y | Y |
| subagent-driven-development | 246/500 | Y | Y | Y | Y | Y | Y | Y |
| systematic-debugging | 291/500 | Y | Y | Y | Y | Y | Y | Y |
| test-driven-development | 203/500 | Y | Y | Y | Y | Y | Y | Y |
| using-git-worktrees | 122/500 | Y | Y | Y | Y | Y | Y | Y |
| using-superpowers | 199/200 | Y | Y | Y | Y | Y | Y | Y |
| verification-before-completion | 141/500 | Y | Y | Y | Y | Y | Y | Y |
| version-control | 240/500 | Y | Y | Y | Y | Y | Y | Y |
| writing-skills | 161/500 | Y | Y | Y | Y | Y | Y | Y |
