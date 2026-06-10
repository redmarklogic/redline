# SRP Violations List — Topology Sync 2026-06-10

**Scan scope:** all 119 `SKILL.md` files under `.agents/skills/` (frontmatter `name:` and `description:` fields), per `hr-sync-agent-topology/procedures/srp-scan-procedure.md`.
**Facilitator:** Harriet. **SRP** = Single Responsibility Principle.

| Skill Name | Field Flagged | Pattern Matched | Disposition |
|---|---|---|---|
| `prek-find-and-fix` | name | "find-and-fix" (structural conjunction in name) | **new-violation** |
| `test-find-and-fix` | name | "find-and-fix" (structural conjunction in name) | **new-violation** |
| `sonarqube-find-and-fix` | name + description | "find-and-fix" / "find-and-fix cycle" | known-exception |
| `hr-sync-agent-topology` | description | "reflects using their assigned knowledge bases and proposes JD patches" | known-exception *(skip-list lists the old name `sync-agent-topology` — see Note 2)* |
| `ceremony-monthly-editorial-session` | description | "content and product signals" | known-exception |
| `library-management` | description | "updating the Excel index, and renaming files" | known-exception |
| `linkedin-social-selling` | name | n/a (no "and"; "social selling" is a domain compound noun) | false-positive |
| `agile-sprint-planning` | description | "identify dependencies and parallelism, and output a sprint plan" | false-positive (Category B — sequential steps of one ceremony) |
| `adr-constitution-sync` | description | "needs updating and executes the sync procedure" | false-positive (Category B — one pipeline) |
| `notebooklm-deep-research` | description | "then index the notebook and return a handoff package" | false-positive (Category B) |
| `create-adr` | description | "structural and link-graph compliance" | false-positive (Category B — compound modifier) |
| `verification-before-completion` | description | "running verification commands and confirming output" | false-positive (Category B) |
| `using-git-worktrees` | description | "smart directory selection and safety verification" | false-positive (Category B) |
| `finishing-a-development-branch` | description | "all tests pass, and you need to decide" | false-positive (Category B — grammatical) |
| `sonarqube-scan` | description | "scan ... and wait for the compute-engine task" | false-positive (Category B — one pipeline) |
| `sonarqube-review` | description | "triage them, and record false positives" | false-positive (Category B — one review cycle) |
| `tool-selection` | description | "GitHub, Google Workspace, and GCP operations" | false-positive (Category B — serial list) |
| `notebooklm-cli` | description | "installation, login, available commands, and diagnostics" | false-positive (Category B — coverage list) |
| `rag-prompting` | description | "structured extraction schemas, and hallucination scoping" | false-positive (Category B — coverage list) |
| `define-ai-policy` | description | "the DORA AI capabilities map, and the team's acceptable-use stance" | false-positive (Category B — coverage list) |
| `mermaid-diagrams` | description | "when-to-diagram rules, and quality standards" | false-positive (Category B — coverage list) |
| `marketing-product-led-seo` | description | "handing an SEO idea off to product and engineering" | false-positive (Category B — audience compound) |
| `task-defer` | description | "creates a structured file ... and updates the index" | false-positive (Category B — one pipeline) |
| `using-superpowers` | description | "how to find and use skills" | false-positive (Category B — grammatical) |
| `speckit-analyze` | description | "consistency and quality analysis" | false-positive (Category B; Layer-0 vendor file) |
| `speckit-clarify` | description | "clarification questions and encoding answers back into the spec" | false-positive (Category B; Layer-0 vendor file) |
| `speckit-red-team-gate` | description | "qualifies for red team, and block /speckit.plan" | false-positive (Category B — one gate concern; vendor extension) |
| `speckit-critique-run` | description | "specification and plan"; "product strategy and engineering risk perspectives" | false-positive (Category B — objects of one dual-lens review; vendor extension) |
| `engineering-architecture` | description | "shaped work and SpecKit output" | false-positive (Category B — objects of one compliance review) |
| `arch-engineering` | description | "shaped work and SpecKit output" | false-positive on SRP *(flagged separately as a duplicate skill — see Note 3)* |

Disposition key:

- `new-violation` — requires resolution before the next topology sync
- `known-exception` — skill is in the Known Exception Skip-List in `srp-scan-procedure.md`
- `false-positive` — grammatical "and" or domain compound noun; no action required

## Notes

1. **New violations (2).** `prek-find-and-fix` and `test-find-and-fix` exactly mirror the approved `sonarqube-find-and-fix` pattern (`justified-orchestrator`: all steps serve one end-to-end quality-gate concern) but are **not** in the Known Exception Skip-List, so they classify mechanically as new-violations. **Proposed resolution:** founder approves adding both to the skip-list as `justified-orchestrator`. Harriet cannot edit `srp-scan-procedure.md` directly (Draft-first constraint on `.agents/skills/`); the table extension is staged as a founder action in the Topology Sync Report.
2. **Skip-list rename housekeeping.** The skip-list entry `sync-agent-topology` refers to a folder renamed to `hr-sync-agent-topology` (uncommitted rename, working tree 2026-06-10). Propose updating the skip-list entry to the new name in the same founder-approved edit as Note 1.
3. **Duplicate skill (not an SRP violation, recorded for the overlap analysis).** `arch-engineering` (frozen since commit `acba676`, 2026-05-31) and `engineering-architecture` (updated 2026-06-07 and 2026-06-09; routed to by Peter's JD) have near-identical trigger descriptions. `arch-engineering` additionally claims "writing ADRs", which overlaps `create-adr`'s declared single-source-of-truth scope. Proposed resolution in the Topology Sync Report: deprecate `arch-engineering`.
4. **Stale skip-list entries with no current match.** `spec-kit`, `mcp-cce`, `resolving-pr-issues`, and `pm-product-strategist` remain skip-listed but their current frontmatter contains no qualifying " and " pattern (descriptions have been cleaned since listing). No action required; entries are harmless.
5. **Vendor pointer files.** `speckit-shaping-gate-check`, `speckit-source-reconciliation-run`, `speckit-static-checks-run`, and `speckit-verification-gate-run` under `.agents/skills/` are pointers into `.specify/extensions/`. Their resolved frontmatter (`description: 'Spec-kit workflow command: <name>'`) contains no qualifying pattern. Clean.
