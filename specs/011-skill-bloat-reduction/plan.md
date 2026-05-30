# Implementation Plan: Skill Bloat Reduction

**Feature**: 011-skill-bloat-reduction
**Created**: 2026-05-30
**Source**: `docs/architecture/skill-bloat-diagnostic-approach.md`
**Scope**: 87 custom skills across 9 `rl.*` agents and 6 `speckit.*` agents

## Baseline

| Metric | Current |
|---|---|
| Total custom skills | 87 |
| Kabilan's routed skills | ~51 |
| Known orphans | 3 (mental-models, python-crewai, ceremony-monthly-editorial-session) |
| SUPERSEDED stubs | 2 (executing-plans, writing-plans) |
| Candidate merge clusters | 7 |
| Vendor-framework skills (excluded) | ~13 (Superpowers) + 4 (SpecKit extensions) |

## Candidate Clusters for Investigation

| Cluster | Skills | Action |
|---|---|---|
| Python design | python-function-design, python-class-design, python-module-structure | Evaluate MERGE |
| Python quality | python-linting, python-static-checks, python-typing | Evaluate MERGE |
| EDA group | eda-codebook, eda-qa, eda-interpreting-data, eda-visual-design | Evaluate MERGE |
| NotebookLM group | notebooklm-mcp, notebooklm-index, notebooklm-deep-research | Evaluate MERGE |
| Git group | git-push-batched, git-hooks-create, version-control, finishing-a-development-branch | Evaluate MERGE |
| MCP tools | miro-mcp, cce-mcp, notebooklm-mcp, python-mcp-tools | Evaluate: rename only (mcp-* prefix) |
| PM overlaps | pm-problem-framer, pm-hypothesis-builder, pm-prd-builder | Evaluate MERGE |

## Prefix Convention (Phase 5)

| Prefix | Scope | Examples |
|---|---|---|
| `mcp-` | MCP server integrations | mcp-miro, mcp-cce, mcp-notebooklm |
| `python-` | Python language/stack | python-style, python-testing-unit |
| `eda-` | Exploratory data analysis | eda-codebook, eda-visual-design |
| `pm-` | Product management | pm-roadmap, pm-prioritization |
| `git-` | Version control operations | git-push-batched, git-hooks-create |
| `marketing-` | Marketing domain | marketing-content-big-5, marketing-social-selling-linkedin |
| `speckit-` | SpecKit extensions | speckit-shaping-gate-check (no rename, vendor-managed) |
| `qmd-` | Quarto/reporting | qmd-narrative-design, qmd-tables |
| `arch-` | Architecture/engineering | arch-engineering (from engineering-architecture) |
| `ceremony-` | Periodic rituals | ceremony-agent-topology-sync |

## Phases

| Phase | Description | Tasks | Dependencies |
|---|---|---|---|
| 1 | Build agent-skill reachability graph | T-001 -- T-003 | None |
| 2 | Classify skills by source layer | T-004 -- T-005 | Phase 1 |
| 3 | Orphan detection + deletion | T-006 -- T-008 | Phase 2 |
| 4 | Cluster evaluation + merge execution | T-009 -- T-015 | Phase 3 |
| 5 | Prefix rename | T-016 -- T-019 | Phase 4 |
| 6 | Visualization + final audit | T-020 -- T-022 | Phase 5 |

## Task Breakdown

### Phase 1: Build Agent-Skill Reachability Graph

**T-001**: Parse agent JD files
- Scan `.github/agents/rl.*.agent.md` for skill routing tables
- Scan `.github/agents/speckit.*.agent.md` for skill references
- Extract agent -> skill edges into `agent_skill_graph.json`
- Output: `agent_skill_graph.json` with agent nodes and degree-1 edges

**T-002**: Parse cross-skill references
- Scan all `.agents/skills/*/SKILL.md` for skill name mentions
- Add degree-2 edges (skill -> skill) to graph
- Scan `AGENTS.md` for additional skill mentions
- Output: updated `agent_skill_graph.json` with degree-2 edges

**T-003**: Compute transitive closure + orphan list
- Compute full reachability from agent nodes
- Produce orphan list: skills with zero in-degree after closure
- Output: `orphan_candidates.md` with each candidate + reasoning

### Phase 2: Classify Skills by Source Layer

**T-004**: Auto-classify by heuristics
- Vendor-Framework: skills matching Superpowers manifest (brainstorming, test-driven-development, etc.)
- SpecKit-Extension: skills with `speckit-` prefix or `author: github-spec-kit` metadata
- Remaining: classify by prefix pattern (python-* -> Language/Stack, pm-* -> Domain/Ops, etc.)
- Output: `skill_classification.json` mapping each skill to its layer

**T-005**: Manual review of ambiguous classifications
- Review skills that don't match prefix heuristics
- Confirm/override auto-classification
- Output: finalized `skill_classification.json`

### Phase 3: Orphan Detection + Deletion

**T-006**: Review orphan candidates with domain owners
- `mental-models`: confirm with Harriet (no agent routes to it)
- `python-crewai`: confirm with Kabilan (CrewAI not in active use)
- `ceremony-monthly-editorial-session`: confirm with John (should it be in his JD?)
- Output: approved deletion list

**T-007**: Delete approved orphans
- Remove skill directories for approved deletions
- Update `skills-lock.json`
- Run `prek run -a` to verify no breakage

**T-008** [P]: Delete SUPERSEDED stubs
- Check `executing-plans` and `writing-plans` for any remaining references
- If zero references: delete directories
- If references remain: verify stubs redirect correctly, keep as-is
- Update `skills-lock.json`

### Phase 4: Cluster Evaluation + Merge Execution

**T-009**: Evaluate Python design cluster
- Compare `python-function-design`, `python-class-design`, `python-module-structure`
- Decision: MERGE into single `python-design` or KEEP with boundary clarification
- If MERGE: consolidate SKILL.md content, move procedures, delete sources
- Update Kabilan's JD routing table

**T-010**: Evaluate Python quality cluster
- Compare `python-linting`, `python-static-checks`, `python-typing`
- Decision: MERGE or KEEP
- If MERGE: consolidate into `python-quality` or similar
- Update Kabilan's JD routing table

**T-011** [P]: Evaluate EDA cluster
- Compare `eda-codebook`, `eda-qa`, `eda-interpreting-data`, `eda-visual-design`
- Decision: MERGE or KEEP
- Update Kabilan's JD routing table

**T-012** [P]: Evaluate NotebookLM cluster
- Compare `notebooklm-mcp`, `notebooklm-index`, `notebooklm-deep-research`
- Decision: MERGE or KEEP
- Update Linda's / Peter's / Graeme's / Harriet's JD routing tables

**T-013** [P]: Evaluate Git cluster
- Compare `git-push-batched`, `git-hooks-create`, `version-control`, `finishing-a-development-branch`
- Decision: MERGE or KEEP
- Update Kabilan's JD routing table

**T-014** [P]: Evaluate PM cluster
- Compare `pm-problem-framer`, `pm-hypothesis-builder`, `pm-prd-builder`
- Decision: MERGE or KEEP
- Update Mark's JD routing table

**T-015**: Update all cross-references after merges
- Search all agent JDs for deleted skill names
- Update `skills-lock.json`
- Update `AGENTS.md` mentions
- Update any cross-skill references in remaining SKILL.md files
- Run `prek run -a`

### Phase 5: Prefix Rename

**T-016**: Generate rename map
- For each surviving custom skill, determine target name per prefix convention
- Exclude Vendor-Framework and SpecKit-Extension skills
- Validate uniqueness (no collisions)
- Output: `rename_map.json` mapping `old_name -> new_name`

**T-017**: Execute renames
- Rename skill directories: `mv .agents/skills/old_name .agents/skills/new_name`
- Update SKILL.md frontmatter `name:` field in each renamed skill
- Update SKILL.md `description:` field if it references own name

**T-018**: Update all references
- Update all agent JD routing tables
- Update `skills-lock.json`
- Update `AGENTS.md`
- Update cross-skill references in all SKILL.md files
- Update any hook scripts that reference skill names

**T-019**: Validate rename
- Run `prek run -a` -- must pass clean
- Run `grep -r "old_name"` for each renamed skill -- must return zero matches (excluding git history)
- Verify no broken references in any `.agent.md` file

### Phase 6: Visualization + Final Audit

**T-020**: Rebuild agent-skill graph post-changes
- Re-run graph builder on the updated codebase
- Output: updated `agent_skill_graph.json`

**T-021**: Generate topology visualization
- Produce Mermaid diagram from final graph
- Verify all nodes are connected (zero orphans)
- Place in `docs/architecture/`

**T-022**: Final audit report
- Count skills before/after by layer
- Confirm SC-001 through SC-007 pass
- Produce summary table for Harriet's records
- Output: audit report in `docs/architecture/`

## Architecture Notes

- All changes are file operations on Markdown files (SKILL.md, agent JDs, AGENTS.md) plus JSON (`skills-lock.json`, graph outputs)
- No Python source code changes in `src/rl/` or `tests/`
- Graph builder: Python script in `scripts/` or inline subagent work (not a permanent tool)
- Each phase should be a separate commit or PR for reversibility
- Phase 5 (rename) should be a separate branch/PR from Phases 1-4 to contain blast radius

## File Structure

```
docs/architecture/
  skill-bloat-diagnostic-approach.md    # Source document (existing)
  agent-skill-topology.md               # Final Mermaid graph (T-021)
  skill-bloat-audit-report.md           # Final audit (T-022)

scripts/
  build_skill_graph.py                  # Graph builder script (T-001/T-002)

output/
  agent_skill_graph.json                # Intermediate artifact
  orphan_candidates.md                  # Phase 3 input
  skill_classification.json             # Phase 2 output
  rename_map.json                       # Phase 5 input
```

## Risk Mitigations

| Risk | Mitigation |
|---|---|
| Merge drops content silently | Each merge requires content diff review; no skill section deleted without explicit KEEP/MOVE |
| Rename breaks hooks or CI | `prek run -a` gate after every rename batch; grep for old names |
| Vendor skill accidentally modified | FR-008: hard classification gate prevents MERGE/DELETE/RENAME on vendor skills |
| False orphan deletion | Two-step: graph flags candidates, domain owner confirms before deletion |
| Rename collision | FR-013: uniqueness validation on rename map before execution |
